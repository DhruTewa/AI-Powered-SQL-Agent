from core.embedding import get_embedding
import chromadb
from core.schema_context import fetch_schema,get_engine
from core.descriptions import TABLE_DESCRIPTIONS

def index_schema():
    engine = get_engine()
    schema_dict = fetch_schema(engine)
    
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="schema_tables")
    
    count = 0
    for schema,tables in schema_dict.items():
        for table, columns in tables.items():
            
            key = f"{schema}.{table}"
            description = TABLE_DESCRIPTIONS.get(key, "")
            text = f"Schema:{schema}\nTable:{table}\nDescription:{description}\nColumns:{','.join(columns)}"
            
            
            vector = get_embedding(text)
            
            #Store in ChromaDB
            collection.upsert(
                documents=[text],
                embeddings=[vector],
                ids=[f"{schema}.{table}"],
                metadatas=[{"schema":schema,"table":table}]
            )
            count +=1
    print(f"Indexed {count} tables into ChromaDB")

if __name__=="__main__":
    index_schema()
    