from document_processor import extract_pdf_chunks


PDF_PATH = r"D:\p\Lecturenotes.pdf"


with open(PDF_PATH, "rb") as file:
    pdf_bytes = file.read()


documents = extract_pdf_chunks(pdf_bytes)


print("Total chunks:", len(documents))


for i, document in enumerate(documents[:5], start=1):

    print("\n==============================")
    print("Chunk:", i)
    print("Page:", document["page"])
    print("Text:")
    print(document["text"])