# File Indexer - Project Structure

## Directory Organization

```
file-indexer/
├── src/                    # Core application modules
│   ├── content_extractor.py   # Text extraction from various file formats
│   ├── database.py            # SQL database connection and operations
│   ├── file_scanner.py        # Directory traversal and file discovery
│   ├── models.py              # SQLAlchemy database table definitions
│   └── vector_store.py        # Vector embeddings management
├── data/                   # Data storage directory
│   └── file_index.db          # SQLite database file
├── main.py                 # Application entry point and orchestration
├── config.py               # Configuration variables and settings
├── dashboard.py            # Streamlit web interface
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Core Components

### Application Layer
- **main.py**: Orchestrates the complete indexing workflow from file scanning to vector store creation
- **config.py**: Centralizes configuration management for directories, database connections, and processing parameters
- **dashboard.py**: Provides web-based interface for search and data visualization

### Data Processing Layer
- **file_scanner.py**: Implements recursive directory traversal with file type filtering
- **content_extractor.py**: Handles multi-format text extraction with error handling and encoding support
- **database.py**: Manages SQLAlchemy sessions and database operations with connection pooling

### Storage Layer
- **models.py**: Defines File entity with metadata fields (name, path, size, timestamps, file_type)
- **vector_store.py**: Manages FAISS/ChromaDB operations for semantic embeddings
- **data/**: Persistent storage for both SQL database and vector indices

## Architectural Patterns

### Modular Design
Each component has single responsibility with clear interfaces between modules, enabling independent testing and maintenance.

### Dual Storage Strategy
Combines structured SQL storage for metadata with unstructured vector storage for content, optimizing both exact and semantic search capabilities.

### Incremental Processing
Database-first approach checks existing records before processing, preventing duplicate work and enabling resumable operations.

### Error Isolation
Per-file error handling with transaction rollback ensures system resilience during batch processing operations.