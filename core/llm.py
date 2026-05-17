import os
import ollama
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def call_ollama(prompt:str):
    model = os.getenv("OLLAMA_MODEL","llama3.2")
    response = ollama.chat(model= model, messages = [{"role":"user","content":prompt}])
    return response ["message"]["content"].strip()


def call_openai(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o"
        ,messages=[{"role":"user","content":prompt}]
        )
    return response.choices[0].message.content.strip()


def call_anthropic(prompt):
    client = Anthropic(api_key= os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()
   

def call_llm(prompt):
    provider = os.getenv("LLM_PROVIDER", "ollama")
    if provider == "ollama":
        return call_ollama(prompt)
    elif provider == "openai":
        return call_openai(prompt)
    elif provider == "anthropic":
        return call_anthropic(prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}")
    