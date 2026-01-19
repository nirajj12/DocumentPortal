# Document Portal - Complete Folder & File Structure

## Directory Tree

```
document_portal/
├── .git/
│   ├── objects/
│   ├── refs/
│   │   ├── heads/
│   │   │   ├── dev
│   │   │   └── main
│   │   └── remotes/
│   │       └── origin/
│   │           ├── dev
│   │           └── main
│   ├── ORIG_HEAD
│   └── [git metadata]
│
├── .github/
│   └── workflows/
│       ├── aws.yaml
│       ├── ci.yaml
│       └── task_definition.json
│
├── .gitignore
│
├── api/
│   ├── main.py
│   └── logs/
│       └── 15_01_2026_06_20_59.log
│
├── app.py
├── streamlit_ui.py
│
├── archive/
│   └── src/
│       ├── __init__.py
│       ├── document_analyzer/
│       │   ├── __init__.py
│       │   ├── data_analysis.py
│       │   └── data_ingestion.py
│       ├── document_compare/
│       │   ├── __init__.py
│       │   ├── data_ingestion.py
│       │   ├── document_comparator.py
│       │   └── retrieval.py
│       ├── multidocument_chat/
│       │   ├── __init__.py
│       │   ├── contextualcompression.py
│       │   ├── data_ingestion.py
│       │   ├── evaluation.py
│       │   ├── mmr.py
│       │   └── retrieval.py
│       └── single_document_chat/
│           ├── __init__.py
│           ├── data_ingestion.py
│           └── retrieval.py
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── 09410fd8.pdf
│   ├── 9a7c0cb2.pdf
│   ├── document_analysis/
│   │   ├── NIPS-2017-attention-is-all-you-need-Paper.pdf
│   │   ├── session_Y1223_114151_7415bde3/
│   │   │   └── [PDF files]
│   │   ├── session_20260116_043059_5345a88a/
│   │   │   └── [PDF files]
│   │   ├── session_20260116_044223_981b0dcb/
│   │   │   └── [PDF files]
│   │   ├── session_20260116_044328_0c733482/
│   │   │   └── [PDF files]
│   │   ├── session_20260116_044331_8596e829/
│   │   │   └── [PDF files]
│   │   ├── session_20260116_044836_56f69f46/
│   │   │   └── [PDF files]
│   │   ├── session_20260116_045522_616c7f93/
│   │   │   └── [PDF files]
│   │   ├── session_20260116_045703_ddd4a4f4/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_051224_951a7d72/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_051546_834737ab/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_052321_8ad56f4c/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_052521_cc55e845/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_052640_9868b85b/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_052829_f8f1e513/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_053125_d7914481/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_053309_e3b2256b/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_053346_ef5dfffc/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_053435_ea77d746/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_053813_798a1c38/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_053842_e44d9571/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_053918_5a1ccf46/
│   │   │   └── [PDF files]
│   │   ├── session_20260117_053956_e9192978/
│   │   │   └── [PDF files]
│   │   ├── session_20260119_110815_85b7e3cb/
│   │   │   └── [PDF files]
│   │   ├── session_20260119_185237_8e641691/
│   │   │   └── [PDF files]
│   │   ├── test_ingestion_analysis/
│   │   │   └── [PDF files]
│   │   └── test_session/
│   │       └── [PDF files]
│   ├── document_compare/
│   │   ├── Stability_Report_Amoxicillin.pdf
│   │   ├── Stability_Report_Paracetamol.pdf
│   │   └── session_20260110_111146_4064c25d/
│   │       ├── Stability_Report_Amoxicillin.pdf
│   │       └── Stability_Report_Paracetamol.pdf
│   ├── multi_document_chat/
│   │   ├── AI_1000plus.txt
│   │   ├── DataScience_1000plus.pdf
│   │   ├── ML_1000plus.docx
│   │   ├── NIPS-2017-attention-is-all-you-need-Paper.pdf
│   │   ├── NLP_1000plus.txt
│   │   ├── session_20260114103400_41b5e059/
│   │   │   ├── AI_1000plus.txt
│   │   │   ├── DataScience_1000plus.pdf
│   │   │   └── ML_1000plus.docx
│   │   ├── session_20260114103438_2e9c82c6/
│   │   │   ├── AI_1000plus.txt
│   │   │   ├── DataScience_1000plus.pdf
│   │   │   ├── ML_1000plus.docx
│   │   │   ├── NIPS-2017-attention-is-all-you-need-Paper.pdf
│   │   │   └── NLP_1000plus.txt
│   │   └── session_20260114104908_05aa8d61/
│   │       ├── 01cfbddb.docx
│   │       ├── 139e3fd2.pdf
│   │       ├── 7bcdbef3.txt
│   │       ├── b6962df5.pdf
│   │       └── e7853a5c.txt
│   ├── single_document_chat/
│   │   ├── NIPS-2017-attention-is-all-you-need-Paper.pdf
│   │   └── session_20260112015231_1f7db93f.pdf
│   └── session_*/
│       └── [uploaded files per session]
│
├── exception/
│   ├── __init__.py
│   ├── custom_exception.py
│   └── custom_exception_archieve.py
│
├── faiss_index/
│   ├── index.faiss
│   ├── index.pkl
│   ├── ingested_meta.json
│   ├── session_20260114103438_2e9c82c6/
│   │   ├── index.faiss
│   │   └── index.pkl
│   ├── session_20260114104908_05aa8d61/
│   │   ├── index.faiss
│   │   └── index.pkl
│   ├── session_20260117_054434_e371210f/
│   │   ├── index.faiss
│   │   ├── index.pkl
│   │   └── ingested_meta.json
│   ├── session_20260117_054545_7000fb95/
│   │   ├── index.faiss
│   │   ├── index.pkl
│   │   └── ingested_meta.json
│   └── session_20260117_121146_a4c232b6/
│       ├── index.faiss
│       ├── index.pkl
│       └── ingested_meta.json
│
├── infrastructure/
│   └── document-portal-cf.yaml
│
├── logger/
│   ├── __init__.py
│   └── custom_logger.py
│
├── logs/
│   ├── 10_01_2026_16_37_49.log
│   ├── 10_01_2026_16_37_51.log
│   ├── [multiple log files dated 10_01 to 19_01]
│   └── 19_01_2026_19_38_26.log
│
├── models/
│   └── models.py
│
├── notebook/
│   ├── data/
│   │   └── sample.pdf
│   ├── exception_experiments.ipynb
│   ├── experiments.ipynb
│   ├── logging_experiments.ipynb
│   └── logs/
│       ├── 21_12_2025_05_05_51.log
│       ├── 21_12_2025_06_48_48.log
│       └── 22_12_2025_10_18_20.log
│
├── prompt/
│   ├── __init__.py
│   └── prompt_library.py
│
├── src/
│   ├── __init__.py
│   ├── document_analyzer/
│   │   ├── __init__.py
│   │   └── data_analysis.py
│   ├── document_chat/
│   │   ├── __init__.py
│   │   └── retrieval.py
│   ├── document_compare/
│   │   ├── __init__.py
│   │   └── document_comparator.py
│   └── document_ingestion/
│       ├── __init__.py
│       └── data_ingestion.py
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── tests/
│   ├── __init__.py
│   └── test_unit_cases.py
│
├── utils/
│   ├── __init__.py
│   ├── config_loader.py
│   ├── document_ops.py
│   ├── file_io.py
│   └── model_loader.py
│
├── CODE_STRUCTURE.md
├── Dockerfile
├── README.md
├── incline_policy.json
├── requirements.txt
├── setup.py
├── test.py
├── versions.py
└── env/
    └── [Conda environment files]
```

---

## File Listing

### Root Level Files
- `.git/` - Git repository
- `.github/workflows/` - GitHub Actions workflows
- `.gitignore` - Git ignore rules
- `CODE_STRUCTURE.md` - Code structure documentation
- `Dockerfile` - Docker configuration
- `README.md` - Project README
- `app.py` - Streamlit app entry point
- `incline_policy.json` - Policy JSON
- `requirements.txt` - Python dependencies
- `setup.py` - Package setup
- `streamlit_ui.py` - Streamlit UI
- `test.py` - Test file
- `versions.py` - Version management

---

### API Layer (`api/`)
- `main.py` - FastAPI application
- `logs/` - API logs

---

### Source Code (`src/`)
- `document_analyzer/` - Document analysis module
  - `data_analysis.py`
- `document_chat/` - Chat/RAG module
  - `retrieval.py`
- `document_compare/` - Document comparison module
  - `document_comparator.py`
- `document_ingestion/` - Document ingestion module
  - `data_ingestion.py`

---

### Configuration (`config/`)
- `config.yaml` - Main configuration

---

### Data (`data/`)
- `document_analysis/` - Analysis results
- `document_compare/` - Comparison results
- `multi_document_chat/` - Multi-doc chat data
- `single_document_chat/` - Single-doc chat data
- `session_*/` - Per-session data directories

---

### FAISS Vector Store (`faiss_index/`)
- `index.faiss` - FAISS index binary
- `index.pkl` - FAISS metadata
- `ingested_meta.json` - Ingestion metadata
- `session_*/` - Per-session indices

---

### Utilities (`utils/`)
- `config_loader.py` - Config loading
- `document_ops.py` - Document operations
- `file_io.py` - File I/O operations
- `model_loader.py` - Model loading

---

### Logging (`logger/`)
- `custom_logger.py` - Custom logger

---

### Exceptions (`exception/`)
- `custom_exception.py` - Exception handling
- `custom_exception_archieve.py` - Archived exceptions

---

### Prompts (`prompt/`)
- `prompt_library.py` - Prompt templates

---

### Models (`models/`)
- `models.py` - Pydantic models

---

### Frontend (`static/` & `templates/`)
- `static/style.css` - Styling
- `templates/index.html` - HTML template

---

### Testing (`tests/`)
- `test_unit_cases.py` - Unit tests

---

### Notebooks (`notebook/`)
- `exception_experiments.ipynb` - Exception experiments
- `experiments.ipynb` - General experiments
- `logging_experiments.ipynb` - Logging experiments
- `data/sample.pdf` - Sample data
- `logs/` - Notebook logs

---

### Archive (`archive/`)
- `src/` - Archived source code
  - `document_analyzer/` - Old analyzer
  - `document_compare/` - Old comparator
  - `multidocument_chat/` - Old multi-doc chat
  - `single_document_chat/` - Old single-doc chat

---

### Infrastructure (`infrastructure/`)
- `document-portal-cf.yaml` - CloudFormation template

---

### GitHub Workflows (`.github/workflows/`)
- `aws.yaml` - AWS deployment workflow
- `ci.yaml` - CI/CD workflow
- `task_definition.json` - ECS task definition

---

### Environment (`env/`)
- Conda environment packages and metadata

---

### Logs (`logs/`)
- Multiple timestamped log files

---

### API Logs (`api/logs/`)
- API-specific log files

---

## File Count Summary

| Directory | File Count |
|-----------|-----------|
| `.git/objects/` | ~1000+ |
| `.github/workflows/` | 3 |
| `api/` | 1 python + logs |
| `archive/src/` | 15+ python |
| `config/` | 1 |
| `data/` | 50+ |
| `exception/` | 2 |
| `faiss_index/` | 15+ |
| `infrastructure/` | 1 |
| `logger/` | 1 |
| `logs/` | 150+ |
| `models/` | 1 |
| `notebook/` | 3 notebooks + data |
| `prompt/` | 1 |
| `src/` | 4 core modules |
| `static/` | 1 |
| `templates/` | 1 |
| `tests/` | 1 |
| `utils/` | 4 |
| Root | 13 |

---

## Key Python Modules

### Core Modules
- `src/document_ingestion/data_ingestion.py`
- `src/document_analyzer/data_analysis.py`
- `src/document_compare/document_comparator.py`
- `src/document_chat/retrieval.py`

### Utilities
- `utils/model_loader.py`
- `utils/config_loader.py`
- `utils/document_ops.py`
- `utils/file_io.py`

### Infrastructure
- `api/main.py`
- `logger/custom_logger.py`
- `exception/custom_exception_archieve.py`
- `models/models.py`
- `prompt/prompt_library.py`

---

## Configuration Files
- `config/config.yaml` - LLM, embedding, retriever config
- `.env` - Environment variables (not committed)
- `Dockerfile` - Container configuration
- `requirements.txt` - Python packages

---

## Data Directories
- `data/document_analysis/` - Analysis session data
- `data/document_compare/` - Comparison session data
- `data/multi_document_chat/` - Multi-doc session data
- `data/single_document_chat/` - Single-doc session data
- `faiss_index/` - Vector store indices
- `logs/` - Application logs

---

## Development Files
- `test.py` - Test runner
- `app.py` - Streamlit entry point
- `streamlit_ui.py` - Streamlit UI code
- `versions.py` - Dependency versions
- `notebook/` - Jupyter notebooks for development

---

## Documentation Files
- `README.md` - Project overview
- `CODE_STRUCTURE.md` - Code documentation

---

## Archive Directory
Contains previous versions of modules:
- Archived document analyzer
- Archived document comparator
- Archived single/multi-document chat
- Archived retrieval implementations

