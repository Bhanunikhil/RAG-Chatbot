import os
import time
import chromadb
from pathlib import Path
from dotenv import load_dotenv
from chromadb import PersistentClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=api_key)

ROOT = Path(__file__).parent.parent
PERSIST_DIR = ROOT / "chroma_db"
SUPPORT_DIR = ROOT / "data" / "support"
PDF_DIR = ROOT / "data" / "pdf_text"

# 1. Initialize the ChromaDB client with DuckDB+Parquet persistence
client = PersistentClient(path=str(PERSIST_DIR))


# 2. Get or create a single, consistent collection name
collection = client.get_or_create_collection(
    name="angelone_support",
)

# Text splitter for consistent chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500, chunk_overlap=300, length_function=lambda text: len(text.split())
)


def load_txts(directory: Path):
    docs = []
    for txt_file in sorted(directory.glob("*.txt")):
        docs.append((txt_file.stem, txt_file.read_text(encoding="utf-8")))
    return docs


def embed_with_gemini(chunks: list[str]) -> list[list[float]]:
    embeddings_list = []
    for i, chunk in enumerate(chunks):
        print(f"    > Embedding chunk {i+1}/{len(chunks)}...")
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=chunk,
                task_type="RETRIEVAL_DOCUMENT",
            )
            embeddings_list.append(result["embedding"])
        except Exception as e:
            print(f"An error occurred embedding chunk {i}: {e}")
            embeddings_list.append(None)
        time.sleep(1)
    return embeddings_list


def main():
    # 1. Loading all the documents
    print("Loading documents from text files...")
    support_docs = load_txts(SUPPORT_DIR)
    pdf_docs = load_txts(PDF_DIR)
    all_docs = support_docs + pdf_docs
    print(f"Loaded {len(all_docs)} documents.")

    # 2. Split into chunks, assign IDs and metadata
    all_chunks, all_ids, all_metadatas = [], [], []
    for doc_name, text in all_docs:
        chunks = text_splitter.split_text(text)
        for idx, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"{doc_name}__{idx}")
            all_metadatas.append({"source": f"{doc_name}.txt", "chunk_index": idx})

    print(f"\nTotal chunks to process: {len(all_chunks)}")

    # 3. Generating the embeddings
    all_embeddings = embed_with_gemini(all_chunks)

    # 4. Filter out failed embeddings
    valid_indices = [i for i, emb in enumerate(all_embeddings) if emb is not None]
    final_chunks = [all_chunks[i] for i in valid_indices]
    final_ids = [all_ids[i] for i in valid_indices]
    final_embeddings = [all_embeddings[i] for i in valid_indices]
    final_metadatas = [all_metadatas[i] for i in valid_indices]

    if not final_chunks:
        print("No chunks were successfully embedded. Aborting.")
        return

    print("\nAdding all chunks to the database...")
    collection.add(
        ids=final_ids,
        embeddings=final_embeddings,
        metadatas=final_metadatas,
        documents=final_chunks,
    )

    print(
        f"\nSuccessfully indexed {len(final_ids)} chunks into Chroma at '{PERSIST_DIR}'"
    )


if __name__ == "__main__":
    main()
