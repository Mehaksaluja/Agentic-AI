# Chat With TXT (RAG From Scratch)

A Retrieval-Augmented Generation (RAG) application built **without LangChain**.

## Tech Stack

- Python
- Groq
- Sentence Transformers
- ChromaDB

---

## Features

- TXT Loader
- Text Cleaning
- Chunking
- Embeddings
- Vector Database
- Similarity Search
- Groq LLM
- Production Folder Structure

---

## Installation

```bash
git clone <repo>

cd chat-with-txt-rag
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

---

Create

```
.env
```

```env
GROQ_API_KEY=YOUR_API_KEY
MODEL_NAME=llama-3.3-70b-versatile
```

---

Run

```bash
python app.py
```