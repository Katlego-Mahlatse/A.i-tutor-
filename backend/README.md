# Smart School OS - Backend API

AI Tutor backend with RAG using Llama 3 and ChromaDB.

## Quick Start

### Prerequisites
- Python 3.9+
- Ollama installed
- Llama 3 model

### Installation

```bash
pip install -r requirements.txt
ollama serve
ollama pull llama3
python main.py
```

Server runs at: `http://localhost:8000`

## Upload Textbooks

```bash
python upload_helper.py
```

## API Endpoints

- `POST /upload-textbook` - Upload textbook PDF
- `POST /ask` - Ask a question
- `GET /subjects` - List subjects
- `GET /health` - System health

## Troubleshooting

**"Connection refused"** - Start Ollama: `ollama serve`

**"Model not found"** - Download: `ollama pull llama3`

**Slow responses** - Use GPU or smaller model: `ollama pull llama3:8b`
