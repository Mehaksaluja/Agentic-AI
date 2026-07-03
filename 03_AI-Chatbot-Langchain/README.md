# AI Chatbot — LangChain + Groq

A command-line AI chatbot built while learning LangChain fundamentals. Uses Groq's fast inference API with the Llama 3.3 70B model, structured with clean separation of concerns across prompts, chains, models, and services.

---

## What This Project Does

You run `app.py`, type a question, and get an AI response — in a loop until you type `exit`.

```
======================================================================
AI Chatbot (LangChain + Groq)
======================================================================
Type 'exit' to quit.

You : What is machine learning?
AI  : Machine learning is a branch of AI where systems learn from data...
```

The interesting part is not the output — it is **how the chatbot is wired together** using LangChain's core patterns.

---

## Project Structure

```
03_AI-Chatbot-Langchain/
├── app.py                    # Entry point — CLI loop
├── config.py                 # Loads .env and exposes as Config class
├── requirements.txt          # Dependencies
├── .env                      # API keys (never commit this)
├── .gitignore
├── utils/
│   └── logger.py             # Logging setup
├── models/
│   └── llm.py                # LLM instantiation (ChatGroq)
├── prompts/
│   └── chatbot_prompt.py     # System prompt + human message template
├── chains/
│   ├── parser.py             # Output parser
│   └── chatbot_chain.py      # Composes the full pipeline
└── services/
    └── chatbot_service.py    # High-level ask() interface
```

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Add your API key to .env
GROQ_API_KEY=your_key_here
MODEL_NAME=llama-3.3-70b-versatile

# Run
python app.py
```

---

## The Core Idea — LangChain Chains

The most important thing to understand in this project is the **chain**:

```python
chain = prompt | llm | parser
```

This single line in `chains/chatbot_chain.py` is the heart of the project. It says:

1. Take the user's question → format it with `prompt`
2. Send the formatted prompt → to the `llm` (Groq/Llama)
3. Take the LLM's response → extract the text with `parser`

This `|` pipe syntax is LangChain's way of composing **Runnables** — components that can be chained together. Every piece (prompt, llm, parser) is a Runnable, which means each one has an `.invoke()` method and they connect seamlessly.

---

## Key LangChain Concepts Used

### 1. ChatPromptTemplate

**File:** `prompts/chatbot_prompt.py`

```python
from langchain_core.prompts import ChatPromptTemplate

ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI Assistant..."),
    ("human", "{question}")
])
```

**What to remember:**
- `from_messages()` takes a list of `(role, content)` tuples
- Roles are `"system"`, `"human"`, `"ai"` (or `"assistant"`)
- `{question}` is a **variable placeholder** — it gets replaced when you call `.invoke({"question": "..."})`
- The **system message** defines the AI's persona and rules
- The **human message** is what the user actually asks

**Why it matters for advanced projects:** Every advanced LangChain project — RAG, agents, multi-step pipelines — starts here. You will swap out or extend the prompt, but the structure stays the same.

---

### 2. ChatGroq (LLM Wrapper)

**File:** `models/llm.py`

```python
from langchain_groq import ChatGroq

ChatGroq(
    api_key=Config.GROQ_API_KEY,
    model=Config.MODEL_NAME,
    temperature=0
)
```

**What to remember:**
- LangChain wraps every LLM provider (OpenAI, Groq, Anthropic, Ollama, etc.) in a consistent interface — you swap the import and class name, the rest of the chain stays identical
- `temperature=0` means deterministic output (same question → same answer). Higher values (0.7–1.0) give more creative/varied responses
- In advanced projects you will swap `ChatGroq` for `ChatOpenAI`, `ChatAnthropic`, `ChatOllama`, etc. — the chain composition (`prompt | llm | parser`) does not change

---

### 3. StrOutputParser

**File:** `chains/parser.py`

```python
from langchain_core.output_parsers import StrOutputParser

StrOutputParser()
```

**What to remember:**
- LLM responses are objects (not plain strings). `StrOutputParser` extracts just the text content
- This is the simplest parser — in advanced projects you will use:
  - `JsonOutputParser` → when you want structured JSON back
  - `PydanticOutputParser` → when you want a validated Python object
  - `CommaSeparatedListOutputParser` → for lists
- Output parsers are always the **last step** in a chain

---

### 4. LCEL — LangChain Expression Language (the `|` pipe)

**File:** `chains/chatbot_chain.py`

```python
chain = prompt | llm | parser
```

**What to remember:**
- This is called **LCEL** (LangChain Expression Language)
- Every component in the pipe must be a **Runnable** (has `.invoke()`, `.stream()`, `.batch()`)
- Data flows **left to right** — output of each step becomes input of the next
- You call the whole chain with `chain.invoke({"question": "your question"})`
- In advanced projects chains get longer: `retriever | prompt | llm | parser` (RAG), or branch with `RunnableParallel`, or loop with agents

---

### 5. `.invoke()` — Running a Chain

**File:** `services/chatbot_service.py`

```python
self.chain.invoke({"question": question})
```

**What to remember:**
- `.invoke()` runs the chain **synchronously** (blocks until done)
- You pass a **dict** whose keys match the `{}` placeholders in your prompt
- Two other important variants:
  - `.stream()` → returns tokens one by one (for streaming UIs)
  - `.batch()` → runs the chain on a list of inputs in parallel
- In advanced projects with multiple prompt variables: `chain.invoke({"context": ..., "question": ...})`

---

### 6. Config Class Pattern

**File:** `config.py`

```python
from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
```

**What to remember:**
- `load_dotenv()` reads `.env` and populates `os.environ` — call it once at startup
- Centralizing config in a `Config` class means you change values in one place, not scattered across files
- The second argument to `os.getenv()` is a **default** — falls back if the env var is missing
- Always add `.env` to `.gitignore` — never commit API keys

---

## Architecture Flow

```
User types question
        │
        ▼
    app.py (CLI loop)
        │
        ▼
  ChatbotService.ask(question)
        │
        ▼
  chain.invoke({"question": question})
        │
        ├──► ChatPromptTemplate  →  formats question into system+human messages
        │
        ├──► ChatGroq            →  sends to Groq API, gets LLM response object
        │
        └──► StrOutputParser     →  extracts plain text from response object
                │
                ▼
         Returns string to app.py
                │
                ▼
        Printed to terminal
```

---

## Design Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Factory** | `LLMFactory`, `ChatbotPrompt`, `OutputParserFactory` | Create objects in one place; easy to swap implementations |
| **Service Layer** | `ChatbotService` | Hides chain complexity behind a simple `.ask()` method |
| **Separation of Concerns** | models / prompts / chains / services | Each folder has one job; changing the LLM doesn't touch the prompt |
| **Config Class** | `config.py` | Centralizes all env variables; no `os.getenv()` scattered in business logic |

---

## What This Project Does NOT Have (Yet)

Understanding what is missing helps you know what to build next:

| Missing Feature | LangChain Tool for It | When You Will Need It |
|---|---|---|
| **Memory / History** | `ConversationBufferMemory`, `RunnableWithMessageHistory` | Multi-turn chat where AI remembers context |
| **RAG (documents)** | `VectorStore`, `Retriever` | Chatbot that answers from your own files/PDFs |
| **Streaming output** | `.stream()` on chain | Real-time token-by-token output in a UI |
| **Agents / Tools** | `AgentExecutor`, `@tool` | AI that can search web, run code, call APIs |
| **Structured output** | `PydanticOutputParser`, `.with_structured_output()` | When you need JSON/typed responses |
| **Multiple chains** | `RunnableParallel`, `RunnableBranch` | Complex pipelines with branching logic |

---

## Things to Remember for Advanced Projects

1. **The `|` pipe is everything.** All advanced LangChain projects are just longer, smarter pipes. Once you understand `prompt | llm | parser`, you understand the pattern — you just add more steps.

2. **Swap providers without rewriting logic.** Because all LLMs share the same Runnable interface, switching from Groq to OpenAI means changing one import and one class name — nothing else in the chain changes.

3. **Prompts are the most important thing to get right.** The system message defines all behavior. In advanced projects, prompt engineering becomes the bulk of the work.

4. **Variables in prompts must match `.invoke()` keys exactly.** If your prompt has `{context}` and `{question}`, your `.invoke()` call must pass `{"context": ..., "question": ...}` — missing keys crash at runtime.

5. **Output parsers close the loop.** The chain always ends with a parser that turns the LLM response object into whatever format your app needs (string, JSON, Python object).

6. **Service layer is worth keeping.** Wrapping the chain in a `ChatbotService.ask()` method means your UI/CLI code never touches LangChain directly — easier to test and swap out later.

7. **Never commit `.env`.** Use `.env.example` with placeholder values to document required variables for other developers (or your future self).

---

## Dependencies

```
langchain          # Core framework
langchain-core     # Runnables, prompts, parsers
langchain-groq     # Groq API integration (ChatGroq)
python-dotenv      # Load .env file into os.environ
```

> **Note:** There is a typo in `requirements.txt` — `puython-dotenv` should be `python-dotenv`. Fix it before sharing the project.
