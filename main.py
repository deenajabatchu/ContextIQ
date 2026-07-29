# ------------------------------------------
# IMPORT LIBRARIES
# ------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile
from fastapi import File
import os
# shutil is the predefined python library
# shutil, used to receive pdf files and save to local path
import shutil
from rag import (
    read_pdf,
    chunk_text,
    create_embeddings,
    store_in_chromadb,
    search_query,
    generate_answer,
    collection
)
# ------------------------------------------
# CREATE FASTAPI APP
# app - get,post,put,delete,head,trace,options,patch
# ------------------------------------------
app = FastAPI()
# ------------------------------------------
# ADD CORS MIDDLEWARE
# ------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------------
# HOME API
# ------------------------------------------
@app.get("/")
def home():
    return {
        "message": "LLM RAG Project Running"
    }
# ------------------------------------------
# PDF UPLOAD API
# ------------------------------------------
'''@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save uploaded PDF
    # Create uploads folder if it doesn't exist
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    # Save uploaded PDF
    pdf_path = os.path.join(UPLOAD_DIR, file.filename)

with open(pdf_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
    # STEP 1 : READ PDF
    text = read_pdf(pdf_path)
    # STEP 2 : CHUNK TEXT
    chunks = chunk_text(text)
    # STEP 3 : CREATE EMBEDDINGS
    embeddings = create_embeddings(chunks)
    # STEP 4 : STORE IN CHROMADB
    store_in_chromadb(chunks, embeddings, source_name=file.filename)
    return {
        "message": "PDF Uploaded Successfully",
        "total_chunks": len(chunks)
    }'''
    
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        pdf_path = os.path.join(UPLOAD_DIR, file.filename)

        print("Saving to:", pdf_path)

        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("PDF Saved Successfully")

        text = read_pdf(pdf_path)

        print("PDF Read Successfully")

        chunks = chunk_text(text)

        print("Chunks:", len(chunks))

        embeddings = create_embeddings(chunks)

        print("Embeddings Created")

        store_in_chromadb(chunks, embeddings, source_name=file.filename)

        print("Stored in ChromaDB")

        return {
            "message": "PDF Uploaded Successfully",
            "total_chunks": len(chunks)
        }

    except Exception as e:
        print(e)
        return {"error": str(e)}
# ------------------------------------------
# ASK QUESTION API
# ------------------------------------------
@app.get("/ask/")
def ask_question(question: str):
    # SEARCH RELEVANT CHUNKS
    results = search_query(question)
    documents = results['documents'][0]
    # CREATE CONTEXT
    context = " ".join(documents)
    # GENERATE FINAL ANSWER
    answer = generate_answer(question, context)
    return {
        "question": question,
        "answer": answer
    }

# ------------------------------------------
# VIEW CHROMADB DATA
# ------------------------------------------

@app.get("/view-data/")
def view_data():
    data = collection.get(
        include=["documents"]
    )
    return {
        "total_chunks": len(data["documents"]),
        "documents": data["documents"]
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)