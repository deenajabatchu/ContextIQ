"""
    PdfReader is the predefined class
    PdfReader used to read data from pdf file
"""
import os
from pypdf import PdfReader

"""
    SentenceTransformer is the predefined class
    SentenceTransformer used to implement the emdebbings
"""
from sentence_transformers import SentenceTransformer

# used to connect to vectordb
import chromadb

# Gemini - used to generate output
from google import genai

from dotenv import load_dotenv
load_dotenv()  # <-- reads .env and populates os.environ

# load the model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# create the table (collection)
# client = chromadb.Client()
# collection = client.create_collection("pdf_data")
# client = chromadb.HttpClient(host="localhost", port=8001)
# collection = client.get_or_create_collection("pdf_data")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_data")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("pdf_data")


# read pdf file
def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text

    return text


# chunk
def chunk_text(text):
    chunk_size = 500
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


# embeddings
def create_embeddings(chunks):
    embeddings = embedding_model.encode(chunks)
    return embeddings


# store in db
import uuid

def store_in_chromadb(chunks, embeddings, source_name="unknown"):
    ids = [f"{source_name}-{uuid.uuid4().hex[:8]}-{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids,
        metadatas=[{"source": source_name, "chunk_index": i} for i in range(len(chunks))]
    )
    return "Data Stored Successfully !!!"


# search
def search_query(question):
    query_embedding = embedding_model.encode([question])
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=2
    )
    return results


# generate output
def generate_answer(question, context):
    #✅ Load API key from environment variable (NEVER hardcode it)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Set it in your .env file or system environment."
        )

    gemini_client = genai.Client(api_key=api_key)

    prompt = f"""
    Answer the question using below context only
    Context:
    {context}
    Question:
    {question}
    """
    try:
        response = gemini_client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )
        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        raise

    final_answer = response.text
    return final_answer