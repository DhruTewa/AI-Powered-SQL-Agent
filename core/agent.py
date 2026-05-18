import os
import re
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from core.retriever import retrieve_schema
from core.validator import validate_sql
from core.llm import call_llm

load_dotenv()

def get_engine():
    engine = create_engine(os.getenv("DATABASE_URL"))
    return engine

def build_prompt(question:str,schema:str)-> str:
    prompt = f"""
    You are PostgresSQL expert
    
    DATABASE SCHEMA: 
    {schema}
    
    RULES:
      - Always qualify table names with schema (e.g., sales.salesorderheader)
      - Return only the SQL query — no explanation, no markdown
      - Use only SELECT — never INSERT, UPDATE, DELETE, DROP
      - You are writing PostgreSQL SQL. Never use TOP, use LIMIT instead.
        Correct: SELECT name FROM sales.salesterritory LIMIT 5
        Wrong:   SELECT TOP (5) name FROM sales.salesterritory
      - ALWAYS prefix every table with its schema. No exceptions.
        Correct: FROM sales.salesorderheader
        Wrong:   FROM salesorderheader
     QUESTION : {question}
     
     SQL: 
     
    """
    return prompt

# def call_llm(prompt:str)-> str:
#     model = os.getenv("OLLAMA_MODEL","llama3.2")
#     message = [{"role":"user","content":prompt}]
#     response = ollama.chat(model= model,messages = message)
#     text = response["message"]["content"]
#     return text.strip()


def extract_sql(llm_response: str) -> str:
    match = re.search(r"```(?:sql)?\s*(.*?)```", llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return llm_response.strip()
  
    
def execute_query(sql:str) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        result = pd.read_sql(text(sql),conn)
        
    return result

def run_agent(question:str) ->pd.DataFrame:
    print("Fetching schema...")
    schema  = retrieve_schema(question)     # from schema_context.py
    print("Building prompt...")
    prompt  = build_prompt(question, schema)   # needs question + schema
    print("Calling llm...")
    response = call_llm(prompt)           # needs the prompt
    sql     = extract_sql(response)         # needs the response
    validated_sql = validate_sql(sql)
    print(f"Generated SQL:\n{validated_sql}\n")
    print(f"executing query...")
    try:
        result  = execute_query(validated_sql) 
        final_sql = validated_sql # needs the sql
    except Exception as e:
        print("SQL failed,attempting self correction...")
        correction_prompt = f"""
        The following SQL failed with this error :
        
        SQL :{sql}
        Error : {e}
        
        Fix the SQL and return only the corrected query
        """
        corrected_response = call_llm(correction_prompt)
        corrected_sql = extract_sql(corrected_response)
        validate_sql(corrected_sql)   # add this line
        print(f"Corrected SQL:\n{corrected_sql}\n")
        result = execute_query(corrected_sql)
        final_sql = corrected_sql
    return final_sql,result