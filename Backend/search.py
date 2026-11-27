import json
import numpy as np
import requests
from sentence_transformers import SentenceTransformer


# ==============================
# Configuration
# ==============================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.2:3b"

EMBEDDINGS_FILE = "embeddings.npy"
DOCUMENTS_FILE = "documents.json"


# ==============================
# Load embedding model
# ==============================

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

def load_index():

    embeddings = np.load(EMBEDDINGS_FILE)

    with open(DOCUMENTS_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    return embeddings, documents


# ==============================
# Load saved embeddings
# ==============================

print("Loading embeddings...")

embeddings = np.load(EMBEDDINGS_FILE)


# ==============================
# Load documents
# ==============================

print("Loading documents...")

with open(DOCUMENTS_FILE, "r", encoding="utf-8") as file:
    documents = json.load(file)
def reload_index():
    global embeddings, documents

    print("\nReloading knowledge base...")

    embeddings = np.load(EMBEDDINGS_FILE)

    with open(DOCUMENTS_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    print("Knowledge base reloaded!")
    print("Number of documents:", len(documents))
    print("Embedding shape:", embeddings.shape)

print("Number of documents:", len(documents))
print("Embedding shape:", embeddings.shape)


# ==============================
# Search function
# ==============================

def search(query, top_k=3, threshold=0.45):

    embeddings, documents = load_index()

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )[0]

    similarities = np.dot(
        embeddings,
        query_embedding
    )

    top_indices = np.argsort(similarities)[::-1][:top_k]
    top_indices = [
    index for index in top_indices
    if similarities[index] >= threshold
]

    results = []

    for index in top_indices:

        results.append({
            "index": int(index),
            "similarity": float(similarities[index]),
            "text": documents[index]["text"],
            "page": documents[index]["page"]
        })

    return results


# ==============================
# Generate answer using Ollama
# ==============================

def generate_answer(query, results):
    if not results:
        return "I could not find this information in the provided documents."
    context = "\n\n".join(
        f"[Page {result['page']}]\n{result['text']}"
        for result in results
    )

    prompt = f"""
You are ForensiQ, an AI-powered digital forensics knowledge assistant.

Answer the user's question using ONLY the information provided
in the context below.

If the answer cannot be found in the context, say:

"I could not find this information in the provided documents."

Do not invent facts.

Context:
{context}

User question:
{query}

Answer clearly and concisely.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]


# ==============================
# RAG pipeline
# ==============================

def ask(query):

    print("\nSearching documents...")

    # Step 1: Retrieve relevant chunks
    results = search(query, top_k=3)

    print("\nRetrieved sources:")

    for result in results:
        print(
            f"- Chunk {result['index']} "
            f"| Page {result['page']} "
            f"| Similarity {result['similarity']:.4f}"
        )

    # Step 2: Generate answer using retrieved context
    print("\nGenerating answer...")

    answer = generate_answer(query, results)

    print("\n==============================")
    print("ForensiQ Answer")
    print("==============================")

    print(answer)

    # Step 3: Show sources
    print("\nSources:")

    for result in results:
        print(
            f"- Page {result['page']} "
            f"(similarity: {result['similarity']:.4f})"
        )

    return {
        "answer": answer,
        "sources": [
            {
                "page": result["page"],
                "similarity": round(result["similarity"], 4)
            }
            for result in results
        ]
    }


# ==============================
# Test
# ==============================

if __name__ == "__main__":

    question = input("\nAsk ForensiQ: ")

    ask(question)