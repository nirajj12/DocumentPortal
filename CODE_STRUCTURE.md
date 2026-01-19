# Document Portal - Complete Code Structure

A detailed guide to understanding the codebase, modules, classes, and data flows in the Document Portal project.

## Table of Contents

1. [Project Architecture](#project-architecture)
2. [Core Modules](#core-modules)
3. [API Layer](#api-layer)
4. [Data Models](#data-models)
5. [Utility Functions](#utility-functions)
6. [Data Flow Diagrams](#data-flow-diagrams)
7. [Class Dependencies](#class-dependencies)
8. [Configuration](#configuration)

---

## Project Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                        │
│  (HTML/CSS/JS Templates, Streamlit, Next.js)           │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  API Layer (FastAPI)                     │
│  - /analyze, /compare, /chat/index, /chat/query         │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│            Business Logic Layer (src/)                   │
│  - document_ingestion/   (DocHandler, ChatIngestor)     │
│  - document_analyzer/    (DocumentAnalyzer)             │
│  - document_compare/     (DocumentComparatorLLM)        │
│  - document_chat/        (ConversationalRAG)            │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│            Infrastructure Layer (utils/)                 │
│  - model_loader.py    (LLM & Embedding loading)         │
│  - document_ops.py    (Document parsing & ops)          │
│  - config_loader.py   (YAML config)                     │
│  - file_io.py         (File handling)                   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│          Data Layer (FAISS, Files, S3)                   │
│  - faiss_index/       (Vector store)                    │
│  - data/              (Session files)                   │
│  - config/            (Config files)                    │
└─────────────────────────────────────────────────────────┘
```

---

## Core Modules

### 1. Document Ingestion Module (`src/document_ingestion/data_ingestion.py`)

**Purpose**: Handle document upload, parsing, embedding, and vector store management.

#### Class: `FaissManager`

Manages FAISS vector store operations with deduplication.

```python
class FaissManager:
    def __init__(self, index_dir: Path, model_loader: Optional[ModelLoader] = None)
    
    # Core Methods
    def _exists(self) -> bool
        # Check if FAISS index exists on disk
        
    def _fingerprint(text: str, md: Dict[str, Any]) -> str
        # Generate unique document fingerprint to prevent duplicates
        # Uses SHA256 hash or source:row_id combination
        
    def add_documents(self, docs: List[Document]) -> int
        # Add new documents with deduplication
        # Returns: Number of newly added documents
        
    def load_or_create(self, texts: Optional[List[str]] = None, 
                      metadatas: Optional[List[dict]] = None)
        # Load existing FAISS index or create new one
        # Returns: FAISS vectorstore instance
        
    def _save_meta(self)
        # Save metadata (ingested_meta.json) to disk
```

**Data Flow**:
```
Documents → Fingerprint Check → Embedding → FAISS Store
                                                    ↓
                            ingested_meta.json (dedup records)
```

**Example Usage**:
```python
fm = FaissManager(Path("faiss_index/session_123"))
fm.load_or_create(texts=chunks, metadatas=[{"source": "doc.pdf"}])
fm.add_documents(new_docs)  # Adds only non-duplicate docs
```

---

#### Class: `ChatIngestor`

Handles multi-file document ingestion for RAG with session management.

```python
class ChatIngestor:
    def __init__(self, 
        temp_base: str = "data",
        faiss_base: str = "faiss_index",
        use_session_dirs: bool = True,
        session_id: Optional[str] = None)
    
    # Core Methods
    def _resolve_dir(self, base: Path) -> Path
        # Return session-specific or global directory
        
    def _split(self, docs: List[Document], 
              chunk_size=1000, chunk_overlap=200) -> List[Document]
        # Split documents into chunks using RecursiveCharacterTextSplitter
        
    def build_retriever(self, uploaded_files: Iterable,
                       *, chunk_size: int = 1000, 
                       chunk_overlap: int = 200, k: int = 5)
        # Complete pipeline: save → load → split → embed → create FAISS
```

**Workflow**:
```
Upload Files → Save to temp_dir → Load (PDF/DOCX/TXT) → 
Split (chunks) → Embed → Create FAISS → Return Retriever
```

**Configuration Parameters**:
```
chunk_size=1000          # Max tokens per chunk
chunk_overlap=200        # Overlap for context
k=5                      # Top-k retrieval
use_session_dirs=True    # Isolate per session
```

---

#### Class: `DocHandler`

Simple PDF upload and read for document analysis.

```python
class DocHandler:
    def __init__(self, data_dir: Optional[str] = None, 
                session_id: Optional[str] = None)
    
    # Core Methods
    def save_pdf(self, uploaded_file) -> str
        # Save uploaded PDF to disk
        # Returns: local file path
        
    def read_pdf(self, pdf_path: str) -> str
        # Extract text from PDF using PyMuPDF (fitz)
        # Returns: complete text content
```

**Used for**: Document analysis pipeline (not RAG).

---

#### Class: `DocumentComparator`

Multi-document comparison with text concatenation.

```python
class DocumentComparator:
    def __init__(self)
    
    # Core Methods
    def save_uploaded_files(self, ref_file, act_file) -> tuple[str, str]
        # Save reference and actual documents
        # Returns: (ref_path, act_path)
        
    def combine_documents(self, ref_path: str, act_path: str) -> str
        # Load and concatenate both documents
        # Returns: combined text with source markers
        
    def clean_old_sessions(self, keep_latest: int = 3)
        # Clean old session directories (disk cleanup)
```

**Output Format**:
```
<<REFERENCE_DOCUMENTS>>
--- SOURCE: reference.pdf ---
[content]

<<ACTUAL_DOCUMENTS>>
--- SOURCE: actual.pdf ---
[content]
```

---

### 2. Document Analyzer Module (`src/document_analyzer/data_analysis.py`)

**Purpose**: Extract structured information from documents using LLM.

#### Class: `DocumentAnalyzer`

```python
class DocumentAnalyzer:
    def __init__(self)
    
    # Core Methods
    def analyze_document(self, text: str) -> Dict[str, Any]
        # Analyze document and extract metadata
        # Returns: Structured analysis with summary, entities, sentiment, etc.
        
    def _build_chain(self)
        # Build LangChain LCEL pipeline with prompt + LLM + parser
```

**Output Structure**:
```json
{
  "summary": ["key point 1", "key point 2"],
  "title": "Document Title",
  "author": "Author Name",
  "sentiment": "positive",
  "entities": ["Entity1", "Entity2"],
  "page_count": 10,
  "language": "English"
}
```

**Prompt Used**:
```
You are a document analysis assistant.
Extract: title, author, summary, entities, sentiment, language.
Return ONLY valid JSON matching schema.
```

---

### 3. Document Comparator Module (`src/document_compare/document_comparator.py`)

**Purpose**: Compare two documents and identify differences.

#### Class: `DocumentComparatorLLM`

```python
class DocumentComparatorLLM:
    def __init__(self)
        # Initialize LLM, prompts, and JSON parser
    
    # Core Methods
    def compare_documents(self, combined_docs: str) -> pd.DataFrame
        # Compare and return page-wise differences
        # Input: concatenated reference + actual documents
        # Returns: DataFrame with [page, changes] columns
        
    def format_response(self, response_parsed: List[Dict]) -> pd.DataFrame
        # Format LLM response to DataFrame
```

**Output Format**:
```
page    | changes
--------|------------------
1       | New section added
2       | No Change
3       | Title modified
```

**Prompt Structure**:
```
Compare two PDFs (reference vs actual):
1. Identify page-wise differences
2. Note exact changes
3. Mark unchanged pages as "No Change"

Return JSON:
[
  {"page": "1", "changes": "..."},
  {"page": "2", "changes": "No Change"}
]
```

---

### 4. Document Chat Module (`src/document_chat/retrieval.py`)

**Purpose**: Implement Retrieval-Augmented Generation (RAG) with conversation context.

#### Class: `ConversationalRAG`

Implements LCEL-based RAG pipeline with lazy retriever initialization.

```python
class ConversationalRAG:
    def __init__(self, session_id: Optional[str], retriever=None)
        # Initialize with session and optional pre-built retriever
    
    # Public API
    def load_retriever_from_faiss(self, index_path: str, k: int = 5,
                                 index_name: str = "index",
                                 search_type: str = "similarity") -> Any
        # Load FAISS index from disk and build LCEL chain
        
    def invoke(self, user_input: str, 
              chat_history: Optional[List[BaseMessage]] = None) -> str
        # Run RAG pipeline with conversation context
        # Returns: Answer with source documents
    
    # Internal Methods
    def _load_llm(self) -> Any
        # Load LLM from ModelLoader
        
    def _build_lcel_chain(self)
        # Build LangChain LCEL pipeline:
        # 1. Contextualize question
        # 2. Retrieve documents
        # 3. Format context
        # 4. Generate answer
        
    @staticmethod
    def _format_docs(docs) -> str
        # Format retrieved documents for prompt
```

**LCEL Chain Architecture**:

```python
# Step 1: Contextualize Question
question_rewriter = (
    {"input": itemgetter("input"), "chat_history": itemgetter("chat_history")}
    | contextualize_prompt
    | llm
    | StrOutputParser()
)

# Step 2: Retrieve Documents
retrieval_chain = question_rewriter | retriever | format_docs

# Step 3: Generate Answer
rag_chain = (
    {
        "context": retrieval_chain,
        "input": itemgetter("input")
    }
    | qa_prompt
    | llm
    | StrOutputParser()
)
```

**Data Flow**:
```
User Query + Chat History
         ↓
[Contextualize] → Standalone Question
         ↓
[Retrieve] → Top-k Document Chunks
         ↓
[Format] → Context String
         ↓
[Generate] → LLM Response
         ↓
Answer with Sources
```

**Example Usage**:
```python
rag = ConversationalRAG(session_id="abc123")
rag.load_retriever_from_faiss("faiss_index/abc123", k=5)

history = [
    HumanMessage(content="Tell me about this doc"),
    AIMessage(content="This document discusses...")
]

answer = rag.invoke(
    "What are the key policies?",
    chat_history=history
)
```

---

## API Layer

### File: `api/main.py`

FastAPI application with REST endpoints for all operations.

#### Server Configuration

```python
app = FastAPI(title="Document Portal API", version="0.1")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files & Templates
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")
```

---

#### Endpoint 1: Health Check

```python
@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "document-portal"}
```

**Response**:
```json
{
  "status": "ok",
  "service": "document-portal"
}
```

---

#### Endpoint 2: Serve UI

```python
@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

Serves the web UI at `/` (loads `templates/index.html`).

---

#### Endpoint 3: Document Analysis

```python
@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)) -> Any
```

**Input**:
- `file`: PDF file upload

**Process**:
1. Save PDF using `DocHandler`
2. Extract text
3. Run `DocumentAnalyzer` on text
4. Return structured analysis

**Response**:
```json
{
  "document_id": "uuid-123",
  "file_name": "document.pdf",
  "summary": ["point1", "point2"],
  "title": "Document Title",
  "sentiment": "positive",
  "entities": ["entity1", "entity2"],
  "page_count": 10,
  "language": "English"
}
```

---

#### Endpoint 4: Document Comparison

```python
@app.post("/compare")
async def compare_documents(
    reference: UploadFile = File(...),
    actual: UploadFile = File(...)
) -> Any
```

**Input**:
- `reference`: Reference PDF
- `actual`: Actual PDF to compare

**Process**:
1. Save both files using `DocumentComparator`
2. Concatenate with source markers
3. Run `DocumentComparatorLLM`
4. Return page-wise differences

**Response**:
```json
{
  "comparison_id": "uuid-456",
  "reference_file": "ref.pdf",
  "actual_file": "act.pdf",
  "differences": [
    {"page": "1", "changes": "New section added"},
    {"page": "2", "changes": "No Change"}
  ],
  "similarity_score": 0.85
}
```

---

#### Endpoint 5: Build Chat Index

```python
@app.post("/chat/index")
async def chat_build_index(
    files: List[UploadFile] = File(...),
    session_id: Optional[str] = Form(None),
    use_session_dirs: bool = Form(True),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(200),
    k: int = Form(5),
) -> Any
```

**Input**:
- `files`: List of PDF/DOCX/TXT files
- `session_id`: Optional session ID (auto-generated if None)
- `chunk_size`: Chunk size for splitting
- `chunk_overlap`: Overlap between chunks
- `k`: Top-k retrieval

**Process**:
1. Create `ChatIngestor` with session ID
2. Upload files, load, split, embed
3. Build FAISS retriever
4. Save to disk

**Response**:
```json
{
  "session_id": "session_abc123",
  "status": "indexed",
  "files_processed": 3,
  "chunks_created": 245,
  "k": 5,
  "use_session_dirs": true
}
```

---

#### Endpoint 6: Chat Query

```python
@app.post("/chat/query")
async def chat_query(
    session_id: str = Form(...),
    question: str = Form(...),
    chat_history: Optional[List[Dict]] = Form(None),
    top_k: Optional[int] = Form(5),
) -> Any
```

**Input**:
- `session_id`: Session ID with indexed documents
- `question`: User question
- `chat_history`: Previous messages (for context)
- `top_k`: Number of chunks to retrieve

**Process**:
1. Load `ConversationalRAG` for session
2. Load FAISS retriever from disk
3. Invoke RAG chain with chat history
4. Return answer with sources

**Response**:
```json
{
  "session_id": "session_abc123",
  "question": "What are the key policies?",
  "answer": "The key policies are...",
  "sources": [
    {
      "content": "Policy section from document",
      "score": 0.92,
      "document": "policy.pdf",
      "page": 3
    }
  ]
}
```

---

## Data Models

### File: `models/models.py`

Pydantic data models for type safety and validation.

#### Enum: `PromptType`

```python
class PromptType(str, Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISON = "document_comparison"
    CONTEXTUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"
```

Maps prompt template names to enum values.

---

#### Model: `Metadata`

Document metadata extracted during analysis.

```python
class Metadata(BaseModel):
    Summary: List[str]              # Key points
    Title: str                      # Document title
    Author: str                     # Author name
    DateCreated: str                # Creation date
    LastModifiedDate: str           # Last modified
    Publisher: str                  # Publisher
    Language: str                   # Language (e.g., "English")
    PageCount: Union[int, str]      # Number of pages
    SentimentTone: str              # Sentiment (positive/negative/neutral)
```

---

#### Model: `ChangeFormat`

Page-wise comparison changes.

```python
class ChangeFormat(BaseModel):
    page: str           # Page number
    changes: str        # Description of changes
```

---

#### Model: `SummaryResponse`

Root model for comparison results.

```python
class SummaryResponse(RootModel[List[ChangeFormat]]):
    pass
```

Wraps list of changes for JSON serialization.

---

## Utility Functions

### File: `utils/model_loader.py`

Loads embedding models and LLMs dynamically.

#### Class: `ApiKeyManager`

Manages API key loading and validation.

```python
class ApiKeyManager:
    REQUIRED_KEYS = ["GROQ_API_KEY", "GOOGLE_API_KEY"]
    
    def __init__(self)
        # Load API keys from:
        # 1. ECS Secrets Manager (JSON)
        # 2. Individual environment variables
        # 3. Validate all required keys present
        
    def get(self, key: str) -> str
        # Retrieve API key by name
```

---

#### Class: `ModelLoader`

Central loader for all ML models.

```python
class ModelLoader:
    def __init__(self)
        # Load config from YAML
        # Initialize API key manager
        
    def load_embeddings(self) -> HuggingFaceEmbeddings
        # Load sentence-transformers/all-MiniLM-L6-v2
        # Returns: 384-dimensional embeddings
        
    def load_llm(self) -> ChatLLM
        # Load LLM based on LLM_PROVIDER env var
        # Supports: groq, google, openai, claude, ollama
```

**Supported LLMs**:
```python
if provider_key == "groq":
    return ChatGroq(api_key=api_key, model_name="openai/gpt-oss-120b")
    
elif provider_key == "google":
    return ChatGoogleGenerativeAI(api_key=api_key, model="gemini-2.0-flash")
    
# ... etc for openai, claude, ollama
```

---

### File: `utils/document_ops.py`

Document loading and processing utilities.

#### Function: `load_documents(paths: Iterable[Path]) -> List[Document]`

Loads documents from files with format-specific loaders.

```python
def load_documents(paths: Iterable[Path]) -> List[Document]:
    """
    Load documents using appropriate loader based on file extension.
    
    Supports:
    - .pdf → PyPDFLoader
    - .docx → Docx2txtLoader
    - .txt → TextLoader
    
    Returns: List of LangChain Document objects
    """
```

---

#### Function: `concat_for_analysis(docs: List[Document]) -> str`

Concatenates documents with source markers for analysis.

```python
def concat_for_analysis(docs: List[Document]) -> str:
    """
    Format: 
    --- SOURCE: filename.pdf ---
    [content]
    
    Returns: Single string with all documents concatenated
    """
```

---

#### Function: `concat_for_comparison(ref_docs, act_docs) -> str`

Concatenates reference and actual documents with markers.

```python
def concat_for_comparison(ref_docs: List[Document], 
                         act_docs: List[Document]) -> str:
    """
    Format:
    <<REFERENCE_DOCUMENTS>>
    --- SOURCE: ref.pdf ---
    [content]
    
    <<ACTUAL_DOCUMENTS>>
    --- SOURCE: act.pdf ---
    [content]
    
    Returns: Formatted string for LLM comparison
    """
```

---

#### Class: `FastAPIFileAdapter`

Adapts FastAPI `UploadFile` to the handler's file interface.

```python
class FastAPIFileAdapter:
    def __init__(self, uf: UploadFile):
        self._uf = uf
        self.name = uf.filename
        
    def getbuffer(self) -> bytes:
        """Read file contents as bytes"""
        self._uf.file.seek(0)
        return self._uf.file.read()
```

Allows using FastAPI uploads with document handlers.

---

#### Function: `read_pdf_via_handler(handler, path: str) -> str`

Extracts text from PDF using DocHandler.

```python
def read_pdf_via_handler(handler, path: str) -> str:
    """Extract text from PDF at path using handler"""
    return handler.read_pdf(path)
```

---

### File: `utils/file_io.py`

File and session management utilities.

#### Function: `generate_session_id(prefix: str = "session") -> str`

Generates unique session ID with timestamp.

```python
def generate_session_id(prefix: str = "session") -> str:
    """
    Returns: session_YYYYMMDD_HHMMSS_UUID
    Example: session_20260119_102340_a1b2c3d4
    """
```

---

#### Function: `save_uploaded_files(uploaded_files: Iterable, target_dir: Path) -> List[Path]`

Saves uploaded files to target directory.

```python
def save_uploaded_files(uploaded_files: Iterable, 
                       target_dir: Path) -> List[Path]:
    """
    1. Create target directory
    2. Save each file with original name
    3. Validate file extension
    
    Returns: List of saved file paths
    """
```

---

### File: `utils/config_loader.py`

YAML configuration loader.

#### Function: `load_config() -> Dict`

Loads `config/config.yaml`.

```python
def load_config() -> Dict:
    """
    Loads YAML and returns:
    {
      "faiss_db": {"collection_name": "..."},
      "embedding_model": {"provider": "huggingface", "model_name": "..."},
      "retriever": {"top_k": 10},
      "llm": {
        "groq": {...},
        "google": {...}
      }
    }
    """
```

---

### File: `logger/custom_logger.py`

Structured logging with JSON output.

#### Class: `CustomLogger`

```python
class CustomLogger:
    def __init__(self)
        # Setup structlog with JSON output
        # Creates logs/ directory and app.log file
        
    def get_logger(self, name: str) -> Logger
        # Returns structlog logger for module
        # Logs to both file and console
```

**Log Format**:
```json
{
  "timestamp": "2026-01-19T10:23:40",
  "event": "Documents split",
  "chunks": 245,
  "chunk_size": 1000,
  "overlap": 200
}
```

---

### File: `exception/custom_exception_archieve.py`

Custom exception handling.

#### Class: `DocumentPortalException`

```python
class DocumentPortalException(Exception):
    def __init__(self, message: str, sys_info: Any)
        # Log error with system info
        # Used throughout for error handling
        
# Usage:
try:
    ...
except Exception as e:
    raise DocumentPortalException("Failed to load documents", sys)
```

---

## Data Flow Diagrams

### Document Analysis Flow

```
┌─────────────────┐
│ Upload PDF      │
└────────┬────────┘
         │
    ┌────▼─────────────────────┐
    │ FastAPI /analyze         │
    └────┬─────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ DocHandler.save_pdf()      │  ← Save to data/
    └────┬──────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ DocHandler.read_pdf()      │  ← Extract text
    └────┬──────────────────────┘
         │ Text string
         │
    ┌────▼──────────────────────────┐
    │ DocumentAnalyzer.analyze()     │
    │                                │
    │ 1. Build LCEL chain           │
    │ 2. Load LLM                   │
    │ 3. Load JSON parser           │
    │ 4. Invoke chain               │
    └────┬──────────────────────────┘
         │ Structured JSON
         │
    ┌────▼───────────────┐
    │ Return Response    │
    │ (Metadata + keys)  │
    └────────────────────┘
```

---

### Document Comparison Flow

```
┌──────────────────────┐
│ Upload 2 PDFs        │
│ (Reference, Actual)  │
└──────────┬───────────┘
           │
    ┌──────▼────────────────────────┐
    │ FastAPI /compare             │
    └──────┬────────────────────────┘
           │
    ┌──────▼──────────────────────┐
    │ DocumentComparator           │
    │ .save_uploaded_files()       │
    └──────┬──────────────────────┘
           │
    ┌──────▼──────────────────────┐
    │ Load both PDFs               │
    │ (PyPDFLoader)               │
    └──────┬──────────────────────┘
           │
    ┌──────▼──────────────────────┐
    │ concat_for_comparison()      │
    │ Format with markers          │
    └──────┬──────────────────────┘
           │ Combined text
           │
    ┌──────▼──────────────────────────┐
    │ DocumentComparatorLLM            │
    │                                  │
    │ 1. Build LCEL chain             │
    │ 2. Load LLM                     │
    │ 3. Load JSON parser             │
    │ 4. Invoke chain                 │
    │ 5. Parse response               │
    │ 6. Convert to DataFrame         │
    └──────┬──────────────────────────┘
           │ DataFrame
           │
    ┌──────▼─────────────────┐
    │ Return Response        │
    │ (Page-wise changes)    │
    └──────────────────────┘
```

---

### Document Chat (RAG) Flow

```
┌───────────────────────┐
│ Upload Multiple Files │
│ (PDF/DOCX/TXT)        │
└──────────┬────────────┘
           │
    ┌──────▼───────────────────────────┐
    │ FastAPI /chat/index              │
    │ Generate session_id              │
    └──────┬───────────────────────────┘
           │
    ┌──────▼──────────────────────┐
    │ ChatIngestor.build_retriever │
    │                              │
    │ 1. Save files to temp_dir   │
    │ 2. Load documents            │
    │    (format handlers)         │
    │ 3. Split into chunks         │
    │    (1000 tokens, 200 overlap) │
    │ 4. Load embeddings           │
    │    (HuggingFace all-MiniLM)  │
    │ 5. Create FAISS store        │
    │ 6. Save to disk              │
    └──────┬──────────────────────┘
           │
    ┌──────▼────────────────────────────────┐
    │ FAISS Index Created                   │
    │ faiss_index/session_abc/              │
    │ ├── index.faiss (vectors)            │
    │ ├── index.pkl (metadata)             │
    │ └── ingested_meta.json (dedup info) │
    └──────┬────────────────────────────────┘
           │
    ┌──────▼─────────────────────────┐
    │ Return session_id to client     │
    └─────────────────────────────────┘
           │
           │ (Later)
           │
    ┌──────▼─────────────────────────┐
    │ FastAPI /chat/query             │
    │ Input: session_id, question     │
    └──────┬─────────────────────────┘
           │
    ┌──────▼──────────────────────────────┐
    │ ConversationalRAG(session_id)        │
    │ .load_retriever_from_faiss()        │
    │ .invoke(question, chat_history)     │
    │                                     │
    │ LCEL Pipeline:                      │
    │ ┌──────────────────────────────┐   │
    │ │ 1. Contextualize Question    │   │
    │ │    (with chat history)       │   │
    │ └──────────┬───────────────────┘   │
    │            │                       │
    │ ┌──────────▼───────────────────┐   │
    │ │ 2. Retrieve Docs             │   │
    │ │    (FAISS similarity search) │   │
    │ │    Top-k=5 chunks           │   │
    │ └──────────┬───────────────────┘   │
    │            │                       │
    │ ┌──────────▼───────────────────┐   │
    │ │ 3. Format Context            │   │
    │ │    (concatenate chunks)      │   │
    │ └──────────┬───────────────────┘   │
    │            │                       │
    │ ┌──────────▼───────────────────┐   │
    │ │ 4. Generate Answer           │   │
    │ │    (LLM with context + q)    │   │
    │ └──────────┬───────────────────┘   │
    │            │                       │
    │            ▼                       │
    │       Answer String               │
    └──────┬──────────────────────────────┘
           │
    ┌──────▼───────────────────┐
    │ Format with Sources       │
    │ (chunk scores, files)     │
    └──────┬───────────────────┘
           │
    ┌──────▼──────────────────────┐
    │ Return JSON Response        │
    │ {answer, sources, ...}      │
    └───────────────────────────┘
```

---

## Class Dependencies

### Dependency Graph

```
FastAPI (api/main.py)
├── DocHandler (data_ingestion.py)
├── DocumentAnalyzer (data_analysis.py)
│   ├── ModelLoader
│   ├── CustomLogger
│   └── PROMPT_REGISTRY
├── DocumentComparator (data_ingestion.py)
├── DocumentComparatorLLM (document_comparator.py)
│   ├── ModelLoader
│   ├── CustomLogger
│   ├── JsonOutputParser
│   └── PROMPT_REGISTRY
├── ChatIngestor (data_ingestion.py)
│   ├── ModelLoader
│   ├── CustomLogger
│   ├── save_uploaded_files
│   ├── load_documents
│   ├── RecursiveCharacterTextSplitter
│   └── FaissManager
│       └── ModelLoader (embeddings)
└── ConversationalRAG (retrieval.py)
    ├── ModelLoader
    ├── CustomLogger
    ├── PROMPT_REGISTRY
    ├── FAISS.load_local()
    └── StrOutputParser

ModelLoader
├── ApiKeyManager
├── load_config() → YAML
├── HuggingFaceEmbeddings
└── ChatGroq/ChatGoogle/... (LLMs)

Utils (various)
├── model_loader.py
├── config_loader.py
├── document_ops.py
├── file_io.py
└── custom_logger.py

Models (models/models.py)
├── Metadata (BaseModel)
├── ChangeFormat (BaseModel)
├── SummaryResponse (RootModel)
└── PromptType (Enum)
```

---

## Configuration

### File: `config/config.yaml`

Central configuration for embedding model, retrievers, and LLMs.

```yaml
faiss_db:
  collection_name: "document_portal"

embedding_model:
  provider: "huggingface"
  model_name: "sentence-transformers/all-MiniLM-L6-v2"
  # 384 dimensions, ~50MB, fast local inference

retriever:
  top_k: 10  # Number of chunks to retrieve

llm:
  groq:
    provider: "groq"
    model_name: "openai/gpt-oss-120b"  # Free, fast
    temperature: 0
    max_output_tokens: 2048
    
  google:
    provider: "google"
    model_name: "gemini-2.0-flash"     # Free 15 days
    temperature: 0
    max_output_tokens: 2048
```

---

### File: `.env` Template

```bash
# LLM Provider
LLM_PROVIDER=groq                      # or: google, openai, claude, ollama

# API Keys
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=AIza...
OPENAI_API_KEY=sk-...

# Paths
FAISS_BASE=faiss_index
UPLOAD_BASE=data
LOG_DIR=logs

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
ENV=local
```

---

## Prompt Templates

### File: `prompt/prompt_library.py`

Central registry of all prompts used in the system.

#### 1. Document Analysis Prompt

```
You are a highly capable AI assistant trained to analyze and summarize documents.
Return only valid JSON matching the exact schema below.

{format_instructions}

Analyze this document:
{document_text}
```

**Output Schema**: `Metadata` (title, author, summary, entities, sentiment, etc.)

---

#### 2. Document Comparison Prompt

```
You will be provided with content for two PDFs.

Tasks:
1. Compare the content in two PDFs
2. Identify the differences and note down the page number
3. Provide page-wise comparison content
4. If any page has no change, mention as 'No Change'

Input documents:
{combined_docs}

Your response should follow this format:
{format_instructions}
```

**Output Schema**: `SummaryResponse` (list of `ChangeFormat`)

---

#### 3. Contextualize Question Prompt

```
Given a conversation history and the most recent user query, rewrite the query 
as a standalone question that makes sense without relying on the previous context.

Do not provide an answer—only reformulate the question.

Chat history: {chat_history}
Question: {input}
Standalone question:
```

**Purpose**: Reformulates follow-up questions to be self-contained.

---

#### 4. Context QA Prompt

```
You are an assistant for question-answering tasks.

Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say you don't know.

Context: {context}

Question: {input}

Answer:
```

**Purpose**: Generates answers based on retrieved context.

---

### Prompt Registry

```python
PROMPT_REGISTRY = {
    PromptType.DOCUMENT_ANALYSIS.value: document_analysis_prompt,
    PromptType.DOCUMENT_COMPARISON.value: document_comparison_prompt,
    PromptType.CONTEXTUALIZE_QUESTION.value: contextualize_question_prompt,
    PromptType.CONTEXT_QA.value: context_qa_prompt,
}
```

Accessed as:
```python
prompt = PROMPT_REGISTRY[PromptType.DOCUMENT_ANALYSIS.value]
```

---

## Key Algorithms & Techniques

### Text Chunking

**Method**: RecursiveCharacterTextSplitter

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,           # Max tokens per chunk
    chunk_overlap=512,         # Overlap for context
    separators=["\n\n", "\n", " ", ""]  # Split hierarchy
)
chunks = splitter.split_documents(docs)
```

**Why**: Preserves document structure by splitting at natural boundaries (paragraphs → sentences → words).

---

### Embedding & Similarity Search

**Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Speed**: ~50 documents/sec (CPU)
- **Memory**: ~50MB

**Vector Store**: FAISS
- **Search Type**: Cosine Similarity
- **Retrieval**: Top-k nearest neighbors
- **Deduplication**: SHA256 fingerprint per document

---

### RAG Pipeline

**Step 1: Question Contextualization**
- Input: User question + chat history
- Output: Standalone question
- Purpose: Remove references to previous context

**Step 2: Document Retrieval**
- Input: Standalone question (embedded)
- Output: Top-k similar chunks
- Metric: Cosine similarity score

**Step 3: Context Formatting**
- Input: Retrieved chunks
- Output: Concatenated context string
- Format: Separated by `\n\n`

**Step 4: Answer Generation**
- Input: Context + question
- Output: LLM-generated answer
- Method: LCEL pipeline with streaming support

---

## Performance Characteristics

### Typical Latencies

| Operation | Time | Notes |
|-----------|------|-------|
| PDF upload & save | 100-500ms | Depends on file size |
| Text extraction | 200-800ms | PyMuPDF parsing |
| Chunking (1000 tokens) | 50-200ms | Recursive split |
| Embedding generation | 500-2000ms | Batch embeddings |
| FAISS index creation | 1-5s | Depends on chunk count |
| Similarity search (k=5) | 10-50ms | FAISS lookup |
| LLM inference (Groq) | 500-2000ms | Very fast |
| RAG query total | 1-3s | Full pipeline |

---

### Memory Usage

| Component | Memory | Notes |
|-----------|--------|-------|
| Embeddings model | ~50MB | all-MiniLM cached |
| FAISS index (1000 docs) | ~100-300MB | Depends on doc count |
| LLM model | 0MB | Cloud-based (Groq/Google) |
| Per-session (files + temp) | 50-200MB | Cleanup recommended |

---

## Testing

### File: `test.py`

Contains integration tests for major components:

```python
# Document Analysis Test
def test_document_analysis():
    dh = DocHandler()
    analyzer = DocumentAnalyzer()
    # ... test pipeline

# Document Comparison Test
def test_compare_documents():
    comparator = DocumentComparator()
    llm_comp = DocumentComparatorLLM()
    # ... test pipeline

# RAG Test
def test_document_ingestion_and_rag():
    ci = ChatIngestor()
    rag = ConversationalRAG()
    # ... test pipeline
```

---

## Common Patterns

### Pattern 1: File Upload + Processing

```python
from fastapi import UploadFile, File
from utils.document_ops import FastAPIFileAdapter

@app.post("/process")
async def process(file: UploadFile = File(...)):
    adapter = FastAPIFileAdapter(file)
    handler = DocHandler()
    path = handler.save_pdf(adapter)
    # ... process
```

---

### Pattern 2: LLM Invocation

```python
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser

loader = ModelLoader()
llm = loader.load_llm()
parser = JsonOutputParser(pydantic_object=MyModel)

chain = prompt | llm | parser
result = chain.invoke({"key": "value"})
```

---

### Pattern 3: Session Management

```python
from utils.file_io import generate_session_id

session_id = generate_session_id()  # session_20260119_102340_abc123

ingester = ChatIngestor(session_id=session_id)
# All files saved to: data/session_id/
# FAISS index saved to: faiss_index/session_id/
```

---

### Pattern 4: Error Handling

```python
from exception.custom_exception_archieve import DocumentPortalException

try:
    # ... operation
except Exception as e:
    logger.error("Operation failed", error=str(e))
    raise DocumentPortalException("User-friendly message", sys)
```

---

## Conclusion

The Document Portal codebase is structured in clear layers:

1. **API Layer** (`api/main.py`): REST endpoints
2. **Business Logic** (`src/`): Core algorithms and workflows
3. **Infrastructure** (`utils/`): Reusable components
4. **Data Models** (`models/`): Type-safe schemas
5. **Configuration** (`config/`): Centralized settings

Each component has a specific responsibility, making the code modular, testable, and maintainable.

---

**Last Updated**: January 2026
**Version**: 0.1
**Author**: Niraj Kumar
