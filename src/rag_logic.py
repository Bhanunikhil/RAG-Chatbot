import os
from pathlib import Path
from dotenv import load_dotenv

import chromadb
from chromadb import PersistentClient
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment")
genai.configure(api_key=api_key)

ROOT = Path(__file__).parent.parent
PERSIST_DIR = ROOT / "chroma_db"
EMBEDDING_MODEL = "models/embedding-001"
GENERATION_MODEL = genai.GenerativeModel("gemini-1.5-flash-latest")


# setting up the connect for ChromaDB
client = PersistentClient(path=str(PERSIST_DIR))
collection = client.get_or_create_collection(name="angelone_support")


def embed_query(text: str) -> list:
    result = genai.embed_content(
        model=EMBEDDING_MODEL, content=text, task_type="RETRIEVAL_QUERY"
    )
    emb = result.get("embedding")
    if not emb:
        raise RuntimeError("Failed to generate query embedding")
    return emb


# ─── Retrieve top-k relevant chunks ──────────────────────────────────────────────
def retrieve_chunks(query: str, k: int = 5) -> list:
    q_emb = embed_query(query)
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    docs = results.get("documents", [[]])[0]
    return docs


# ─── Answer using RAG + Gemini Chat ─────────────────────────────────────────────
def answer_with_rag(query: str, k: int = 5) -> str:
    chunks = retrieve_chunks(query, k)
    if not chunks:
        return "I Don't know"
    print(f"Retrieved {len(chunks)} relevant chunks for query: '{query}'")

    source_texts = "\n\n---\n\n".join(chunks)
    prompt = (
        "You are a helpful support assistant for Angel One.\n\n"
        "Answer the user's question based *only* on the provided sources below.\n\n"
        "If the information to answer the question is not in the sources, you must respond with: `I Don't know`\n\n"
        f"--- SOURCES ---\n{source_texts}\n\n--- END SOURCES ---\n\n"
        f"User question: {query}\n\n"
    )

    try:
        response = GENERATION_MODEL.generate_content(
            prompt,
        )
        return response.text
    except Exception as e:
        return f"Sorry, an error occurred during generation: {e}"


# ─── Interactive loop for user queries ──────────────────────────────────────────
"""if __name__ == "__main__":
    print("RAG chatbot initialized. Type your question or 'exit' to quit.")
    while True:
        user_q = input("Question: ")
        if not user_q or user_q.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        try:
            ans = answer_with_rag(user_q)
            print(f"Answer: {ans}\n")
        except Exception as e:
            print(f"Error: {e}\n")
            """
