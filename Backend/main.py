from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from indexer import index_pdf
from search import ask, reload_index


app = FastAPI(
    title="ForensiQ",
    description="AI-powered digital forensics knowledge assistant",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():

    return {
        "message": "ForensiQ API is running!"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    contents = await file.read()

    result = index_pdf(contents)
    
    reload_index()

    return {
        "filename": file.filename,
        "message": "PDF indexed successfully",
        "documents": result["documents"],
        "embedding_shape": list(result["embedding_shape"])
    }


@app.post("/ask")
def ask_forensic(request: QuestionRequest):

    result = ask(request.question)

    return result