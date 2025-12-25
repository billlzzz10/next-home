# File Indexer - Technology Stack

## Programming Language
- **Python 3**: Core application language with extensive library ecosystem for data processing and machine learning

## Database Technologies
- **SQLite**: Primary database for development and small-scale deployments
- **SQLAlchemy**: ORM for database abstraction and query building
- **PostgreSQL**: Recommended upgrade path for production environments

## Vector Search & ML
- **FAISS (Facebook AI Similarity Search)**: High-performance vector similarity search library
- **ChromaDB**: Alternative vector database option for embeddings storage
- **sentence-transformers**: Pre-trained transformer models for text embeddings
  - Default model: `all-MiniLM-L6-v2` (lightweight, fast inference)

## Content Processing
- **pypdf**: PDF text extraction with support for multiple PDF formats
- **python-docx**: Microsoft Word document (.docx) content extraction
- **Built-in Python**: Text file processing (.txt, .md, .py) with UTF-8 encoding

## Web Interface
- **Streamlit**: Rapid web application development for dashboard and search interface
- **FastAPI**: Alternative option for REST API development

## Core Dependencies
```
sqlalchemy          # Database ORM and connection management
pypdf              # PDF content extraction
python-docx        # Word document processing
faiss-cpu          # Vector similarity search (CPU version)
sentence-transformers  # Text embedding models
streamlit          # Web dashboard framework
```

## Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run main indexing process
python main.py

# Launch web dashboard
streamlit run dashboard.py

# Database initialization (automatic on first run)
python -c "from src.database import create_database; create_database()"
```

## System Requirements
- **Python**: 3.7+ (recommended 3.9+)
- **Memory**: 4GB+ RAM for vector operations
- **Storage**: Variable based on indexed content volume
- **CPU**: Multi-core recommended for large file processing