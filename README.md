# Simple RAG System

A lightweight Retrieval-Augmented Generation (RAG) system built with free components.

## Features

- **Free Vector Database**: ChromaDB (open-source)
- **Free Embeddings**: Sentence Transformers (local)
- **Free LLM**:  Groq (free API)
- **Document Support**: PDF, TXT, MD files
- **CLI Interface**: Command-line and interactive modes
- **Simple API**: Easy to integrate and extend

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd rag-with-scope

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy and edit the `.env` file:

```bash
cp .env.example .env
```

Configure your preferred LLM provider:

**For Groq (free API):**
```bash
# Get API key from https://groq.com
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama2-70b-4096
```

### 3. Usage

#### CLI Mode
```bash
# Show system information
python src/cli.py --info

# Ingest a document
python src/cli.py --ingest-file data/documents/sample.pdf

# Ingest all documents from directory
python src/cli.py --ingest-dir data/documents/

# Query the system
python src/cli.py --query "What is machine learning?"

# Interactive mode
python src/cli.py --interactive
```

#### Python API
```python
from src.rag_pipeline import RAGPipeline

# Initialize
rag = RAGPipeline()

# Inest documents
rag.ingest_document("data/documents/sample.pdf")
rag.ingest_text("Your custom text here")

# Query
result = rag.query("What is Python?")
print(result['answer'])
```

#### Run Example
```bash
python examples/basic_usage.py
```

## Architecture

```
Documents → Text Splitter → Embeddings → Vector DB
    ↑                                        ↓
    └─────── Query ← LLM ← Search Results ←─┘
```

## Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `CHUNK_SIZE` | `1000` | Text chunk size for processing |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `MAX_RETRIEVED_DOCS` | `5` | Max documents to retrieve |
| `SIMILARITY_THRESHOLD` | `0.7` | Minimum similarity score |

## Supported File Formats

- PDF files (`.pdf`)
- Text files (`.txt`)
- Markdown files (`.md`)

## LLM Options

### Groq Models
- `llama2-70b-4096`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

## Performance Tips

1. **Chunk Size**: Larger chunks (1000-2000) work better for detailed queries
2. **Embedding Model**: `all-mpnet-base-v2` provides better quality at cost of speed
3. **Batch Processing**: Process multiple documents at once for efficiency
4. **Local LLM**: Ollama provides better privacy and no rate limits

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Groq API Issues:**
- Verify API key in `.env`
- Check rate limits
- Ensure model name is correct

**Groq API Issues:**
- Verify API key in `.env`
- Check rate limits
- Ensure model name is correct

**Memory Issues:**
- Reduce `CHUNK_SIZE` in configuration
- Use smaller embedding model
- Process documents in batches

## Development

### Running Tests
```bash
pytest tests/
```

### Project Structure
```
rag-system/
├── src/                    # Core modules
│   ├── vector_db.py       # ChromaDB integration
│   ├── embeddings.py      # Sentence transformers
│   ├── llm.py             # LLM providers
│   ├── document_processor.py  # Text processing
│   ├── rag_pipeline.py    # Main RAG pipeline
│   └── cli.py             # Command-line interface
├── data/documents/        # Document storage
├── examples/              # Usage examples
├── tests/                 # Unit tests
└── config.py             # Configuration settings
```

## License

MIT License - feel free to use and modify.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review the example code
- Open an issue on GitHub