import pymupdf

from chunker import chunk_text


def extract_pdf_chunks(pdf_bytes):
    """
    Extract text from a PDF and split it into chunks
    while keeping track of the page number.
    """

    pdf = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    documents = []

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text()

        if not text.strip():
            continue

        chunks = chunk_text(
            text,
            chunk_size=1000,
            overlap=150
        )

        for chunk in chunks:

            documents.append({
                "text": chunk,
                "page": page_number
            })

    pdf.close()

    return documents