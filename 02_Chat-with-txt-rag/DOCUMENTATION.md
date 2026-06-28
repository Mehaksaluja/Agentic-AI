# Chat With TXT — RAG From Scratch
## Complete Project Documentation

---

## Table of Contents

1. [What Is This Project?](#1-what-is-this-project)
2. [Core Concept: What Is RAG?](#2-core-concept-what-is-rag)
3. [Tech Stack & Why Each Tool Was Chosen](#3-tech-stack--why-each-tool-was-chosen)
4. [Project Folder Structure](#4-project-folder-structure)
5. [Complete Data Flow](#5-complete-data-flow)
6. [File-by-File Breakdown](#6-file-by-file-breakdown)
   - [config.py](#configpy)
   - [models/document.py](#modelsdocumentpy)
   - [utils/logger.py](#utilsloggerpy)
   - [data/notes.txt](#datanotestxt)
   - [loaders/txt_loader.py](#loaderstxt_loaderpy)
   - [preprocessing/cleaner.py](#preprocessingcleanerpy)
   - [preprocessing/splitter.py](#preprocessingsplitterpy)
   - [embeddings/embedding_model.py](#embeddingsembedding_modelpy)
   - [vectordb/chroma_manager.py](#vectordbchroma_managerpy)
   - [retrieval/retriever.py](#retrievalretrieverpy)
   - [prompts/rag_prompt.py](#promptsrag_promptpy)
   - [llm/groq_client.py](#llmgroq_clientpy)
   - [services/rag_service.py](#servicesrag_servicepy)
   - [app.py](#apppy)
7. [Key Concepts Explained](#7-key-concepts-explained)
   - [Embeddings](#embeddings)
   - [Vector Database & Similarity Search](#vector-database--similarity-search)
   - [Chunking & Overlap](#chunking--overlap)
   - [Prompt Engineering in RAG](#prompt-engineering-in-rag)
   - [Why "From Scratch"?](#why-from-scratch)
8. [Configuration Reference](#8-configuration-reference)
9. [How to Run](#9-how-to-run)
10. [Numbered Execution Trace (Example)](#10-numbered-execution-trace-example)

---

## 1. What Is This Project?

This project is a **command-line chatbot** that answers questions about the content of a `.txt` file. It is built using **RAG (Retrieval-Augmented Generation)** entirely from scratch — meaning no high-level framework like LangChain is used. Every pipeline step (loading, cleaning, chunking, embedding, storing, retrieving, prompting, generating) is written explicitly so you can see exactly what happens under the hood.

**What it does in plain English:**
- You have a text file (`notes.txt`) with some content.
- You ask a question in the terminal.
- The app finds the most relevant parts of your file using AI embeddings.
- It passes those parts to an LLM (large language model) and gets an answer grounded only in your document.

---

## 2. Core Concept: What Is RAG?

**RAG = Retrieval-Augmented Generation**

LLMs are trained on huge datasets, but they do not know the contents of *your specific documents*. RAG solves this by:

1. **Indexing** your documents — breaking them into pieces and converting them into vectors (numbers that represent meaning).
2. **Retrieving** the most relevant pieces when you ask a question — by comparing your question's vector to the stored document vectors.
3. **Generating** an answer — by feeding the retrieved pieces as context to the LLM, which then answers *based on your document, not general training data*.

```
[Your Document] → [Chunks] → [Vectors] → [Stored in DB]
                                                  ↓
[User Question] → [Vector] → [Similarity Search] → [Top Chunks] → [LLM] → [Answer]
```

RAG prevents **hallucination** (the LLM making things up) by grounding the answer in real retrieved content.

---

## 3. Tech Stack & Why Each Tool Was Chosen

| Tool | Role | Why |
|---|---|---|
| **Python** | Core language | Universally used for AI/ML |
| **Sentence Transformers** (`all-MiniLM-L6-v2`) | Embedding model | Free, local, fast — produces 384-dim semantic vectors |
| **ChromaDB** | Vector database | Lightweight, file-based, no server needed — great for learning |
| **Groq** (`llama-3.3-70b-versatile`) | LLM inference | Extremely fast inference, free tier available |
| **python-dotenv** | Environment variables | Keeps API keys out of source code |

**No LangChain** — the entire pipeline is handwritten so every line is readable and understandable.

---

## 4. Project Folder Structure

```
02_Chat-with-txt-rag/
│
├── app.py                       ← Entry point. Orchestrates everything.
├── config.py                    ← All configuration in one place.
├── requirements.txt             ← Python package dependencies.
├── .env                         ← (Not committed) API keys.
│
├── data/
│   └── notes.txt                ← The document the chatbot reads.
│
├── models/
│   └── document.py              ← Data class: wraps text + metadata.
│
├── loaders/
│   └── txt_loader.py            ← Reads notes.txt → Document object.
│
├── preprocessing/
│   ├── cleaner.py               ← Removes extra whitespace from text.
│   └── splitter.py              ← Splits text into overlapping chunks.
│
├── embeddings/
│   └── embedding_model.py       ← Converts text/queries to vectors.
│
├── vectordb/
│   └── chroma_manager.py        ← ChromaDB: store & search vectors.
│
├── retrieval/
│   └── retriever.py             ← Glues embedding + vector search.
│
├── prompts/
│   └── rag_prompt.py            ← System prompt + prompt builder.
│
├── llm/
│   └── groq_client.py           ← Calls Groq API to get LLM answer.
│
├── services/
│   └── rag_service.py           ← High-level: retrieve → prompt → generate.
│
└── utils/
    └── logger.py                ← Configures Python's logging module.
```

Each folder is a **domain layer** — a single, focused responsibility. This mirrors production-level Python project structure.

---

## 5. Complete Data Flow

The project has two distinct phases:

### Phase 1 — Indexing (runs once at startup)

This phase processes the document and stores it in the vector database so it can be searched later.

```
data/notes.txt
      │
      ▼
TextLoader.load()
  → reads file, returns Document(page_content, metadata)
      │
      ▼
TextCleaner.clean()
  → collapses all whitespace to single spaces, strips leading/trailing
      │
      ▼
TextSplitter.split()
  → produces overlapping text chunks (500 chars, 100 overlap)
  → e.g. ["Python is a high-level...", "...widely used for AI..."]
      │
      ▼
EmbeddingModel.embed_documents()
  → runs each chunk through all-MiniLM-L6-v2
  → produces a list of 384-dimensional float vectors
      │
      ▼
ChromaManager.add_documents()
  → stores (chunk text + vector + metadata) in chroma_db/ folder on disk
  → only runs if collection is empty (idempotent — won't re-index)
```

### Phase 2 — Query Loop (per user question)

This phase handles every question the user asks interactively.

```
User types: "What is Python?"
      │
      ▼
RAGService.ask(question)
      │
      ├─► Retriever.retrieve(question)
      │         │
      │         ├─► EmbeddingModel.embed_query(question)
      │         │     → converts question to a 384-dim vector
      │         │
      │         └─► ChromaManager.search(query_embedding, top_k=3)
      │               → finds the 3 closest chunks by cosine similarity
      │               → returns ["Python is a high-level...", ...]
      │
      ├─► build_prompt(chunks, question)
      │     → combines the 3 retrieved chunks + the question into a prompt string
      │
      └─► GroqClient.generate(prompt)
            → sends system prompt + user prompt to Groq API
            → receives: "Python is a high-level programming language."
                  │
                  ▼
            printed to terminal as "Assistant: ..."
```

---

## 6. File-by-File Breakdown

---

### `config.py`

**Purpose:** Single source of truth for all configuration values.

```python
class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")        # Read from .env
    MODEL_NAME = "llama-3.3-70b-versatile"           # Groq LLM to use
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"             # Local embedding model
    CHROMA_PATH = "chroma_db"                        # Folder where ChromaDB persists
    COLLECTION_NAME = "notes"                        # Name of the collection in ChromaDB
    CHUNK_SIZE = 500                                 # Max characters per chunk
    CHUNK_OVERLAP = 100                              # Characters shared between adjacent chunks
```

**Why it matters:** Every other file imports from `Config` instead of hardcoding values. To change the LLM model or chunk size, you change it in exactly one place.

`load_dotenv()` is called here, so `.env` values are loaded before any other module reads them.

---

### `models/document.py`

**Purpose:** A simple data container for a loaded document.

```python
@dataclass
class Document:
    page_content: str    # The full raw text of the file
    metadata: Dict       # Extra info, e.g. {"source": "notes.txt"}
```

**Concept — Dataclass:** A `@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__` methods. It is the Python equivalent of a simple struct — just a holder for named fields. No logic lives here.

**Why it matters:** Wrapping the raw text + metadata together keeps the loader's return value clean and self-describing. Any consumer knows exactly what fields to expect.

---

### `utils/logger.py`

**Purpose:** Configures Python's standard `logging` module once, globally.

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)
```

**Output example:**
```
2026-06-28 10:23:45,123 | INFO | Loading document...
```

**Why not `print()`?** `logging` gives you timestamps, log levels (INFO, WARNING, ERROR), and can be redirected to files or monitoring systems. `print()` cannot be filtered or structured.

---

### `data/notes.txt`

**Purpose:** The document the chatbot is built on top of.

```
Python is a high-level programming language.
Python supports Object-Oriented Programming.
Python is widely used for AI, Machine Learning and Data Science.
Lists in Python are mutable.
Tuples are immutable.
Dictionaries store key-value pairs.
Functions are reusable blocks of code.
Classes are blueprints for creating objects.
```

This is a tiny example document. In a real project, this could be a large manual, a knowledge base, or any `.txt` file. The pipeline works the same regardless of file size.

---

### `loaders/txt_loader.py`

**Purpose:** Reads the `.txt` file from disk and returns a `Document`.

```python
class TextLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)    # pathlib.Path for OS-safe paths

    def load(self) -> Document:
        if not self.file_path.exists():
            raise FileNotFoundError(...)    # Fail early with a clear message
        text = self.file_path.read_text(encoding="utf-8")
        return Document(
            page_content=text,
            metadata={"source": self.file_path.name}   # e.g. "notes.txt"
        )
```

**Concept — `pathlib.Path`:** More reliable than plain string paths because it handles Windows vs Linux slash differences automatically and provides methods like `.exists()` and `.read_text()`.

**Why separate from `app.py`?** The loader layer can be swapped. Tomorrow you could add a `PDFLoader` or `CSVLoader` in the same folder with the same interface, and `app.py` would change one line.

---

### `preprocessing/cleaner.py`

**Purpose:** Normalizes raw text before chunking.

```python
class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        text = re.sub(r"\s+", " ", text)   # Replace any whitespace sequence with a single space
        return text.strip()                # Remove leading/trailing whitespace
```

**Concept — `re.sub(r"\s+", " ", text)`:**
- `\s+` is a regex pattern matching one or more whitespace characters: spaces, tabs (`\t`), newlines (`\n`), carriage returns (`\r`).
- This collapses them all to a single space.
- Result: `"Python is a\n\nhigh-level"` → `"Python is a high-level"`

**Why clean?** Embedding models work on word meaning, not layout. Extra newlines add no semantic value and waste chunk space.

**Why `@staticmethod`?** The method has no state — it only transforms its input. A static method signals "this function belongs to the class conceptually but needs no instance."

---

### `preprocessing/splitter.py`

**Purpose:** Splits cleaned text into overlapping chunks.

```python
class TextSplitter:
    def __init__(self, chunk_size=500, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size          # slice end position
            chunks.append(text[start:end])         # extract the chunk
            start += self.chunk_size - self.overlap  # advance with overlap
        return chunks
```

**Concept — Why Overlap?**

Imagine your text is:
```
...sentence A. sentence B. sentence C...
```
If chunk 1 ends mid-sentence B and chunk 2 starts mid-sentence B, the answer to a question about sentence B might be split between two chunks and retrieved poorly. Overlap ensures that sentence B appears fully in *at least one* chunk.

**Example with chunk_size=20, overlap=5:**
```
Text:    "ABCDEFGHIJKLMNOPQRSTU"
Chunk 1: "ABCDEFGHIJKLMNOPQRST"   (0→20)
Chunk 2: "PQRSTUVWXYZ..."         (15→35)  ← "PQRST" is shared
```

**Advance formula:** `start += chunk_size - overlap` = `500 - 100 = 400` — so each new chunk starts 400 characters after the previous one, with 100 characters of shared context.

---

### `embeddings/embedding_model.py`

**Purpose:** Converts text (chunks or queries) into numerical vectors using a local model.

```python
class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(documents, convert_to_numpy=True)
        return embeddings.tolist()    # shape: (N, 384)

    def embed_query(self, query: str) -> list[float]:
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding.tolist()    # shape: (384,)
```

**Concept — What is an embedding?**

An embedding is a list of floating-point numbers (a vector) that represents the *semantic meaning* of a piece of text. Texts with similar meaning have vectors that are numerically close to each other.

Example (simplified):
```
"Python is a language" → [0.23, -0.15, 0.87, ...]   (384 numbers)
"Python programming"   → [0.21, -0.14, 0.85, ...]   (very close)
"I like pizza"         → [-0.5, 0.9, -0.3, ...]     (very different)
```

**`all-MiniLM-L6-v2`:**
- Runs **locally** on your machine — no API call needed for embeddings.
- Produces **384-dimensional** vectors.
- "MiniLM" = Mini Language Model, "L6" = 6 transformer layers, "v2" = version 2.
- Fast and accurate enough for most RAG use cases.

**`convert_to_tensor=False, convert_to_numpy=True`:** Returns a plain NumPy array, which `.tolist()` converts to a Python list of floats — what ChromaDB expects.

**Two methods, not one:**
- `embed_documents` takes a list (batch embedding is faster than one-by-one).
- `embed_query` takes a single string.

---

### `vectordb/chroma_manager.py`

**Purpose:** Interface to ChromaDB — stores and searches document vectors.

```python
class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(name="notes")

    def add_documents(self, chunks, embeddings, metadata):
        ids = [f"doc_{i}" for i in range(len(chunks))]   # Unique IDs
        metadatas = [metadata for _ in chunks]            # Same metadata for all chunks
        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query_embedding, top_k=3):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
```

**Concept — ChromaDB:**

ChromaDB is a **vector database** — a database optimized for storing and searching embedding vectors. Unlike a regular SQL database that searches by exact value matching, ChromaDB searches by **similarity** between vectors.

- `PersistentClient(path="chroma_db")` — data is written to a folder called `chroma_db/` on disk. It survives across runs (no re-indexing needed).
- `get_or_create_collection("notes")` — a collection is like a table. Creates it if it doesn't exist.
- `collection.add(ids, documents, embeddings, metadatas)` — stores 4 things per chunk:
  - `id` — unique string identifier (`"doc_0"`, `"doc_1"`, ...)
  - `document` — the raw text chunk
  - `embedding` — the 384-dim vector
  - `metadata` — source file name
- `collection.query(query_embeddings, n_results=3)` — finds the `n_results` closest stored vectors to the query vector.

**Similarity measure:** ChromaDB uses **cosine similarity** by default — measures the angle between two vectors. Vectors pointing in the same direction = similar meaning = high similarity score.

---

### `retrieval/retriever.py`

**Purpose:** Combines embedding + vector search into a single `retrieve()` call.

```python
class Retriever:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_db = ChromaManager()

    def retrieve(self, query, top_k=3):
        query_embedding = self.embedding_model.embed_query(query)
        results = self.vector_db.search(query_embedding, top_k)
        return results["documents"][0]    # list of top-k chunk strings
```

**What `results` looks like from ChromaDB:**
```python
{
  "documents": [["chunk text 1", "chunk text 2", "chunk text 3"]],
  "distances": [[0.12, 0.18, 0.25]],
  "metadatas": [[{...}, {...}, {...}]],
  "ids": [["doc_0", "doc_2", "doc_5"]]
}
```
`results["documents"][0]` extracts the inner list — the actual text of the top 3 chunks.

**Why a separate `Retriever` class?** It cleanly separates *how* to find relevant context (the retrieval strategy) from *what* to do with it (the RAG service). You could swap this for a BM25 keyword retriever or a hybrid search with no changes to `RAGService`.

---

### `prompts/rag_prompt.py`

**Purpose:** Defines the system prompt and a function to build the user-facing prompt.

```python
SYSTEM_PROMPT = """
You are a helpful AI Assistant.
Answer ONLY using the provided context.
If the answer is not available in the context, say:
"I couldn't find the answer in the provided document."
Keep answers concise.
"""

def build_prompt(context, question):
    context = "\n\n".join(context)    # Join the 3 chunks with blank lines between
    return f"""
Context:

{context}

Question:

{question}

Answer:
"""
```

**Concept — Prompt Engineering in RAG:**

The prompt has two parts:

1. **System prompt** (sent as the `system` role): Sets the AI's behavior.
   - "Answer ONLY using the provided context" — prevents hallucination.
   - "If not available, say..." — handles questions outside the document gracefully.

2. **User prompt** (sent as the `user` role): The actual content.
   - Provides the retrieved context chunks.
   - Poses the user's question.
   - Ends with `Answer:` to cue the model to respond.

**Why `"\n\n".join(context)`?** Separating the 3 chunks with double newlines makes them visually distinct in the prompt so the LLM can process each chunk as a separate paragraph.

---

### `llm/groq_client.py`

**Purpose:** Calls the Groq API to generate an answer from a given prompt.

```python
class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model=Config.MODEL_NAME,     # "llama-3.3-70b-versatile"
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )
        return response.choices[0].message.content
```

**Concept — Chat Completions API:**

This follows the OpenAI-compatible chat format, which Groq also uses:
- `messages` is a list of `{"role": ..., "content": ...}` dicts.
- `"system"` role sets the AI's persona and rules.
- `"user"` role is the human's message (the context + question prompt).
- The model responds as `"assistant"`.

**`temperature=0`:** Controls randomness.
- `0` = fully deterministic, most confident answer. Perfect for factual Q&A.
- `1` = more creative/varied (used for writing tasks).

**`response.choices[0].message.content`:** Groq returns a list of possible completions (`choices`). We take the first one and extract the text content.

**Why Groq?** Groq runs LLMs on custom hardware (LPUs) that are dramatically faster than GPU-based inference. Llama 3.3 70B runs at hundreds of tokens/second — responses feel instant.

---

### `services/rag_service.py`

**Purpose:** High-level orchestrator for a single user question.

```python
class RAGService:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = GroqClient()

    def ask(self, question):
        chunks = self.retriever.retrieve(question)       # Step 1: find relevant chunks
        prompt = build_prompt(chunks, question)          # Step 2: build structured prompt
        return self.llm.generate(prompt)                 # Step 3: get LLM answer
```

This is the **facade** of the RAG pipeline — the single point of contact between the application layer (`app.py`) and the entire retrieval + generation machinery below it.

Three lines in `ask()` map directly to the three RAG steps:
1. **Retrieve** — semantic search over the vector database.
2. **Augment** — build a prompt that includes the retrieved context.
3. **Generate** — send to the LLM and get an answer.

---

### `app.py`

**Purpose:** Entry point. Runs indexing once, then starts the interactive chat loop.

```python
DATA_PATH = "data/notes.txt"

def build_vector_database():
    loader = TextLoader(DATA_PATH)
    document = loader.load()

    cleaned_text = TextCleaner.clean(document.page_content)

    splitter = TextSplitter()
    chunks = splitter.split(cleaned_text)

    embedding_model = EmbeddingModel()
    embeddings = embedding_model.embed_documents(chunks)

    vector_db = ChromaManager()

    if vector_db.collection.count() == 0:     # Only index if DB is empty
        vector_db.add_documents(chunks, embeddings, document.metadata)
    else:
        logger.info("Database already indexed.")

def main():
    build_vector_database()
    rag = RAGService()

    while True:
        question = input("You : ")
        if question.lower() == "exit":
            break
        answer = rag.ask(question)
        print("Assistant :", answer)

if __name__ == "__main__":
    main()
```

**Key design decisions:**

- **Idempotent indexing:** `if vector_db.collection.count() == 0` checks if documents are already indexed before adding them. This means you can restart the app without re-processing and re-storing the document every time.
- **`if __name__ == "__main__"`:** Standard Python pattern — `main()` only runs when you execute `python app.py` directly, not when this file is imported as a module.
- **Simple `while True` loop:** The chat loop runs indefinitely until the user types `"exit"`.

---

## 7. Key Concepts Explained

### Embeddings

An embedding turns text into a list of numbers (a vector) where **similar meanings = numerically close vectors**.

The model `all-MiniLM-L6-v2`:
- Is a **sentence transformer** — it reads the whole sentence, not just word-by-word.
- Produces 384-dimensional vectors (384 numbers per text input).
- Is pre-trained on millions of sentence pairs to understand semantic similarity.

Example (conceptual):
```
"Python is a programming language" → [0.23, -0.15, 0.87, 0.45, ...]
"Python coding"                    → [0.21, -0.13, 0.84, 0.42, ...]  ← close
"I love ice cream"                 → [-0.6, 0.92, -0.3, -0.7, ...]  ← far
```

### Vector Database & Similarity Search

A vector database stores embedding vectors and supports **approximate nearest-neighbor search** — finding the stored vectors most similar to a query vector, very quickly.

ChromaDB uses **cosine similarity**:
```
similarity = cos(angle between two vectors)
           = (A · B) / (|A| × |B|)
```
- Value of `1.0` = identical direction = identical meaning.
- Value of `0.0` = perpendicular = unrelated.
- Value of `-1.0` = opposite direction = opposite meaning.

ChromaDB returns results ordered from most similar to least similar.

### Chunking & Overlap

You cannot pass an entire large document to an LLM — both the embedding model and the LLM have context limits. Chunking breaks the document into pieces that fit within those limits.

**Overlap** prevents information loss at chunk boundaries:

```
Chunk 1:  [--------------------100-chars-overlap----]
Chunk 2:              [----100-chars-overlap----------...]
```

The overlapping 100 characters appear in both chunk 1 and chunk 2. This means a sentence that falls near a boundary is fully represented in at least one retrievable chunk.

**This project's settings:**
- `CHUNK_SIZE = 500` — each chunk is at most 500 characters.
- `CHUNK_OVERLAP = 100` — adjacent chunks share 100 characters.

### Prompt Engineering in RAG

The quality of answers depends heavily on how the prompt is structured. This project uses two key techniques:

1. **Grounding instruction** in the system prompt:
   > "Answer ONLY using the provided context."
   
   This prevents the LLM from using its general training knowledge and forces it to stay within the document.

2. **Fallback instruction** in the system prompt:
   > "If the answer is not available in the context, say: 'I couldn't find the answer...'"
   
   Without this, the LLM might guess or hallucinate.

3. **Structured user prompt** (Context → Question → Answer):
   - Putting context first helps the model pay attention to it.
   - Ending with `Answer:` is a natural cue for the model to respond.

### Why "From Scratch"?

Frameworks like LangChain wrap all of these steps in single function calls. That is great for productivity but hides what is happening. Building from scratch means:

- You understand every transformation the data goes through.
- You can debug any step independently.
- You can replace any component (e.g., swap ChromaDB for Pinecone, swap Groq for OpenAI) because the boundaries between layers are clear.
- You know exactly what an embedding is, what a vector database query returns, and how the prompt is structured.

---

## 8. Configuration Reference

All values live in `config.py` and can be overridden via `.env`:

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | (from `.env`) | Groq API key — required |
| `MODEL_NAME` | `llama-3.3-70b-versatile` | Groq LLM model ID |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `CHROMA_PATH` | `chroma_db` | Folder where ChromaDB data is stored |
| `COLLECTION_NAME` | `notes` | ChromaDB collection name |
| `CHUNK_SIZE` | `500` | Characters per chunk |
| `CHUNK_OVERLAP` | `100` | Overlapping characters between chunks |

---

## 9. How to Run

**Prerequisites:**
- Python 3.10+
- A Groq API key (free at console.groq.com)

```bash
# 1. Clone and enter the project
git clone <repo>
cd 02_Chat-with-txt-rag

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
# Contents:
# GROQ_API_KEY=your_key_here
# MODEL_NAME=llama-3.3-70b-versatile

# 5. Run
python app.py
```

**First run:** Downloads `all-MiniLM-L6-v2` (~90 MB) once, then indexes `notes.txt`.

**Subsequent runs:** Model is cached locally, database is already indexed — startup is fast.

**To reset the vector database** (re-index from scratch): delete the `chroma_db/` folder.

---

## 10. Numbered Execution Trace (Example)

User runs `python app.py` and asks: **"What are tuples?"**

```
1.  app.py: main() called
2.  app.py: build_vector_database() called

--- INDEXING PHASE ---
3.  TextLoader("data/notes.txt").load()
      → reads file → Document(page_content="Python is a high-level...", metadata={"source":"notes.txt"})

4.  TextCleaner.clean(document.page_content)
      → collapses whitespace → "Python is a high-level programming language. Python supports..."

5.  TextSplitter().split(cleaned_text)
      → CHUNK_SIZE=500, OVERLAP=100
      → notes.txt is small (~280 chars), so only 1 chunk is produced:
         ["Python is a high-level programming language. Python supports..."]

6.  EmbeddingModel().embed_documents(chunks)
      → loads all-MiniLM-L6-v2 (cached after first run)
      → encodes the 1 chunk → [[0.23, -0.15, 0.87, ...]]  (384 floats)

7.  ChromaManager() connects to chroma_db/
      → collection.count() == 0 → DB is empty → proceed to add

8.  vector_db.add_documents(chunks, embeddings, metadata)
      → ChromaDB stores: id="doc_0", document=chunk_text, embedding=[...], metadata={"source":"notes.txt"}

9.  logger.info("Document indexed successfully.")

--- QUERY PHASE ---
10. RAGService() initializes Retriever() and GroqClient()
11. Terminal prints: "CHAT WITH TXT (RAG FROM SCRATCH)"
12. User types: "What are tuples?"

13. RAGService.ask("What are tuples?")

14. Retriever.retrieve("What are tuples?")
      a. EmbeddingModel.embed_query("What are tuples?")
            → encodes question → [0.05, 0.77, -0.34, ...]  (384 floats)
      b. ChromaManager.search(query_embedding, top_k=3)
            → cosine similarity search
            → returns top 3 closest chunks (here, only 1 exists, so returns 1 repeated or 1 result)
            → documents[0] = ["Python is a high-level programming language..."]

15. build_prompt(chunks, "What are tuples?")
      → context = "Python is a high-level programming language..."
      → prompt = "Context:\n\n{context}\n\nQuestion:\n\nWhat are tuples?\n\nAnswer:\n"

16. GroqClient.generate(prompt)
      → POST to Groq API with:
          system: "You are a helpful AI Assistant. Answer ONLY using the provided context..."
          user:   "Context:\n\nPython is a high-level...Tuples are immutable...\n\nQuestion:\nWhat are tuples?\n\nAnswer:"
      → Groq returns: "Tuples are immutable."

17. Terminal prints:
      Assistant:
      Tuples are immutable.
```

---

*This documentation covers every file, concept, and design decision in the project. The goal was to build intuition for the full RAG pipeline — from raw text on disk to a grounded LLM answer in the terminal.*
