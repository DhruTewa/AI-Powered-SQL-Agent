from openai import OpenAI
from dotenv import load_dotenv
import ollama
import os

load_dotenv()

def embed_openai(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
        )
    return response.data[0].embedding


def embed_ollama(text):
    model = os.getenv("OLLAMA_EMBED_MODEL","nomic-embed-text")
    response = ollama.embeddings(model=model, prompt= text)
    return response["embedding"]

def get_embedding(text):
    provider = os.getenv("EMBEDDING_PROVIDER","ollama")
    if provider == "ollama":
        return embed_ollama(text)
    elif provider == "openai":
        return embed_openai(text)
    else:
        raise ValueError(f"Unknown provider: {provider}")
   