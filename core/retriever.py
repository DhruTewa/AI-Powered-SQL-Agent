from core.embedding import get_embedding
import chromadb

def retrieve_schema(question: str, n_results: int = 8) -> str:
    # Connect to the existing ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="schema_tables")

    # Embed the question
    
    vector = get_embedding(question)
    
    # Find the closest table descriptions
    results = collection.query(
        query_embeddings=[vector],
        n_results=n_results
    )


    # Unwrap and join into one string
    tables = results["documents"][0]

    
    return "\n\n".join(tables)