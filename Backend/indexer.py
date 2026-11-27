import json
import numpy as np
import pymupdf
from sentence_transformers import SentenceTransformer

from chunker import chunk_text

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

EMBEDDINGS_FILE = "embeddings.npy"
DOCUMENTS_FILE = "documents.json"

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)


def index_pdf(pdf_bytes):
    """
    Extract text from a PDF, split it into chunks,
    generate embeddings, and save everything.
    """

    print("Reading uploaded PDF...")

    pdf = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    documents = []

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text()

        chunks = chunk_text(text)

        for chunk in chunks:
            documents.append({
                "text": chunk,
                "page": page_number
            })

    pdf.close()

    if not documents:
        raise ValueError("No text could be extracted from the PDF.")

    print("Generating embeddings...")

    texts = [document["text"] for document in documents]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    np.save(EMBEDDINGS_FILE, embeddings)

    with open(DOCUMENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(documents, file, ensure_ascii=False, indent=2)

    print("Indexing complete.")

    return {
        "documents": len(documents),
        "embedding_shape": embeddings.shape
    }