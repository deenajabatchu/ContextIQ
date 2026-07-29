# ContextIQ

**AI-Powered Document Intelligence Chatbot using RAG, Gemini LLM, and Vector Search**

ContextIQ is a Retrieval-Augmented Generation (RAG) chatbot that lets you upload a PDF and ask natural language questions about its contents. Instead of relying purely on an LLM's general knowledge, ContextIQ retrieves the most relevant passages from your document and grounds Gemini's answer in that context — reducing hallucination and keeping responses tied to what's actually in the file.

This project was built as a hands-on way to understand the RAG pattern that powers many real-world AI agents and copilots — going from concept to a fully working, deployed system.

---

## 🚀 Live Demo

- **Linkedin:** [URL]


---

## 🧩 How It Works

```
PDF Upload
   ↓
Text Extraction (pypdf)
   ↓
Chunking
   ↓
Embeddings (Sentence Transformers)
   ↓
Vector Storage (ChromaDB)
   ↓
User Question
   ↓
Similarity Search (ChromaDB)
   ↓
Relevant Chunks → Gemini API
   ↓
Grounded Answer
```

1. **Upload** — A PDF is parsed and split into overlapping text chunks.
2. **Embed** — Each chunk is converted into a vector embedding locally using `sentence-transformers` (no API cost).
3. **Store** — Embeddings and chunk text are stored in a persistent ChromaDB collection.
4. **Ask** — A user's question is embedded the same way, and ChromaDB returns the most semantically similar chunks.
5. **Generate** — The retrieved chunks are passed as context to Google's Gemini API, which generates a final answer grounded in that context.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python) |
| PDF Parsing | pypdf |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) — local, free |
| Vector Database | ChromaDB (persistent local storage) |
| LLM | Google Gemini API (`gemini-2.5-flash`) |
| Frontend | HTML, CSS, Bootstrap, JavaScript (glassmorphism UI) |
| Deployment | Render (Web Service + Static Site) |

---

## 📂 Project Structure

```
ContextIQ/
├── main.py               # FastAPI routes: upload, ask, view-data
├── rag.py                # Core RAG pipeline logic
├── requirements.txt
├── start.sh
├── .env.example          # Template for required environment variables
├── frontend/
│   └── index.html        # Chat UI
├── uploads/              # Uploaded PDFs (not committed)
└── chroma_data/          # Vector DB persistence (not committed)
```

---

## ⚙️ Setup & Local Development

**1. Clone the repository**
```bash
git clone https://github.com/deenajabatchu/ContextIQ.git
cd ContextIQ
```

**2. Create a virtual environment**
```bash
python -m venv venv314
venv314\Scripts\activate      # Windows
source venv314/bin/activate   # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your environment variables**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com).

**5. Run the backend**
```bash
uvicorn main:app --reload
```
Visit `http://127.0.0.1:8000/` — you should see:
```json
{"message": "LLM RAG Project Running"}
```

**6. Open the frontend**

Open `frontend/index.html` directly in your browser, or serve it with any static file server. Make sure the API base URL in the UI points to `http://127.0.0.1:8000`.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/upload-pdf/` | Upload a PDF, chunk it, embed it, and store it in ChromaDB |
| `GET` | `/ask/?question=...` | Ask a question; retrieves relevant chunks and returns a Gemini-generated answer |
| `GET` | `/view-data/` | View all currently indexed chunks |

---

## 🎯 Design Decisions

- **Local embeddings over an embedding API** — using Sentence Transformers keeps embedding generation free and fast, with no per-request API cost, while still integrating cleanly with ChromaDB.
- **Gemini for generation** — chosen for its generous free tier, making the project fully runnable without a paid API key.
- **Persistent ChromaDB storage** — chunks persist across server restarts locally (though Render's free tier disk is ephemeral, so hosted data resets on redeploy — see Limitations below).

---

## ⚠️ Known Limitations

- **No source citation yet** — answers don't currently indicate which page/chunk they came from. (Planned improvement.)
- **Ephemeral storage on Render's free tier** — uploaded PDFs and the vector index reset when the service restarts or redeploys.
- **Single combined knowledge base** — all uploaded documents currently share one ChromaDB collection rather than being isolated per document.
- **Free-tier rate limits** — Gemini's free tier caps requests per minute/day; heavy or concurrent use may hit `429` errors.

---

## 🗺️ Roadmap

- [ ] Add page-level source citation for answers
- [ ] Support multiple isolated document sessions
- [ ] Add basic evaluation of retrieval/answer quality
- [ ] Migrate to a hosted vector DB (Chroma Cloud / Pinecone) for persistence on Render
- [ ] Add automated tests for upload and ask endpoints

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙋 About

Built as a hands-on learning project to understand Retrieval-Augmented Generation (RAG) — the same core pattern behind many production AI agents and copilots — end to end: from PDF parsing to a deployed, working chatbot.
