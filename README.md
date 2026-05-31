# AskDocs AI - Smart RAG-Based Document Intelligence Chatbot

**AskDocs AI** is an advanced, resume-grade Retrieval-Augmented Generation (RAG) web application that enables users to upload multiple PDF documents and engage in context-grounded natural language conversations. 

The application utilizes **local, offline sentence embedding models** to construct a high-performance vector database (ChromaDB) completely for free and on-device, and leverages **Google Gemini 1.5** to generate precise, hallucination-free answers backed by transparent document source citations.

---

## 🚀 Key Features

### 🔹 Core RAG Pipeline
* **Multi-PDF Parsing & Cleaning:** Page-by-page text parsing with formatting cleanup using `PyPDF`.
* **Recursive Chunking:** Logical text chunking with configurable overlap (`RecursiveCharacterTextSplitter`) to preserve contextual continuity.
* **100% Offline Vector Store:** Free, local, CPU-optimized semantic vector generation using `sentence-transformers/all-MiniLM-L6-v2`.
* **Local Persistent Database:** Secure vector indexing and persistent local storage using `ChromaDB`.

### 🔸 Premium User Experience
* **Glassmorphic Dark Theme:** Custom-styled developer dashboard UI built on Streamlit using custom vanilla CSS.
* **Sleek API Key Integration:** Easy-to-use in-app sidebar key field featuring a 1-click free key generator link for [Google AI Studio](https://aistudio.google.com/).
* **Transparent Source Citations:** Interactive expanders showing exact matching text snippets and page numbers for answer accountability.
* **Document Summarizer:** Auto-generates high-level executive summaries of active documents.
* **Dynamic AI Questions:** Analyzes uploaded documents on-the-fly to suggest relevant click-to-ask questions.
* **Exportable Transcripts:** Download the entire chat history as a professionally formatted Markdown file.
* **Admin Dashboard:** Displays live vector collection stats, page counts, and total chunks.

---

## 📐 System Architecture

```text
       [ Multiple PDF Files ]
                 │
                 ▼
       [ PyPDF Text Extractor ]
                 │
                 ▼
   [ Recursive Character Splitting ]
                 │
                 ▼
     [ Local Sentence Embeddings ] <─── (all-MiniLM-L6-v2)
                 │
                 ▼
     [ Persistent ChromaDB Store ]
                 ▲
                 │ (Similarity Search)
                 ▼
       [ User Query Input ] ─────► [ RAG prompt compilation ]
                                              │
                                              ▼
                                    [ Google Gemini 1.5 ]
                                              │
                                              ▼
                                  [ Chat Response + Citations ]
```

---

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Frontend UI:** Streamlit (with custom glowing glassmorphic CSS injection)
* **Orchestration:** LangChain (Core, Community, and Google GenAI wrappers)
* **Embeddings:** HuggingFace `sentence-transformers`
* **Vector Store:** ChromaDB (persistent local)
* **LLM Engine:** Google Gemini API (`gemini-1.5-flash`)
* **Parsing:** PyPDF

---

## 📂 Project Directory Structure

```text
askdocs-ai/
│
├── app.py                      # Main Streamlit web application & custom CSS
├── requirements.txt            # Python package specifications
├── README.md                   # Professional project documentation
├── .gitignore                  # Git exclusions (data/, vector_db/, secrets)
├── .env.example                # Example environment variables template
│
├── src/                        # Backend modular logic package
│   ├── __init__.py
│   ├── pdf_loader.py           # Text extraction & page-level metadata
│   ├── text_splitter.py       # Recursive chunking & boundary overlap
│   ├── vector_store.py         # ChromaDB persistence & similarity search
│   ├── rag_chain.py            # LangChain Gemini RAG QA & summary prompt
│   └── utils.py                # Chat Markdown exporter & question generator
│
├── data/
│   └── uploaded_docs/          # Preserves source uploads locally
│
└── vector_db/                  # Local active ChromaDB vector index folder
```

---

## ⚡ Quick Start

### 1. Clone & Set Active Workspace
Open your terminal inside your project directory:
```bash
cd askdocs-ai
```

### 2. Set Up Virtual Environment & Dependencies
Create and activate your Python virtual environment, then install requirements:
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Setup Environment variables (Optional)
Copy `.env.example` to `.env` and fill in your key, or enter it directly in the app UI:
```bash
cp .env.example .env
```

### 4. Run Verification Tests
Test that local database vectorization and similarity queries run correctly offline:
```bash
python verify_rag.py
```

### 5. Launch the Web Dashboard
```bash
streamlit run app.py
```

---

## 👤 Resume Description (For Placement & Interviews)

**AskDocs AI - RAG Based Document Q&A Chatbot**
*Python, LangChain, ChromaDB, HuggingFace, Streamlit, Gemini API, Git*

* Developed a resume-level Retrieval-Augmented Generation (RAG) chatbot allowing users to upload multiple PDF documents and perform secure natural-language inquiries.
* Implemented page-level PDF text extraction and recursive text splitting with 100-character overlaps to maintain contextual boundaries.
* Designed a zero-cost local database pipeline using offline HuggingFace sentence-transformer embeddings (`all-MiniLM-L6-v2`) and persistent `ChromaDB`.
* Integrated the `Gemini-1.5-flash` API with a custom system prompt ensuring strictly contextual answers, preventing creative hallucinations.
* Built a high-fidelity glassmorphism dark-themed Streamlit dashboard with custom CSS, containing live stats, an auto-summary builder, document-derived suggested questions, and interactive source citations showing exact text snippets.
