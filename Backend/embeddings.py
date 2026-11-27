import json
import numpy as np
from sentence_transformers import SentenceTransformer

from document_processor import extract_pdf_chunks


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

PDF_PATH = r"D:\p\Lecturenotes.pdf"

EMBEDDINGS_PATH = "embeddings.npy"
DOCUMENTS_PATH = "documents.json"


# -----------------------------
# Load embedding model
# -----------------------------

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)


# -----------------------------
# Read PDF
# -----------------------------

print("Reading PDF...")

with open(PDF_PATH, "rb") as file:
    pdf_bytes = file.read()


# -----------------------------
# Extract chunks + page numbers
# -----------------------------

documents = extract_pdf_chunks(pdf_bytes)

texts = [document["text"] for document in documents]


# -----------------------------
# Generate embeddings
# -----------------------------

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    normalize_embeddings=True
)


# -----------------------------
# Save embeddings
# -----------------------------

np.save(EMBEDDINGS_PATH, embeddings)


# -----------------------------
# Save documents
# -----------------------------

with open(DOCUMENTS_PATH, "w", encoding="utf-8") as file:
    json.dump(
        documents,
        file,
        ensure_ascii=False,
        indent=2
    )


# -----------------------------
# Display information
# -----------------------------

print("\n==============================")
print("Embedding generation complete")
print("==============================")

print("Number of chunks:", len(documents))
print("Embedding shape:", embeddings.shape)

print("\nSaved files:")

print("-", EMBEDDINGS_PATH)
print("-", DOCUMENTS_PATH)

print("\nFirst chunk:")
print(documents[0]["text"])

print("\nFirst chunk page:")
print(documents[0]["page"])