# Smart School OS - Backend API

AI Tutor backend with RAG (Retrieval Augmented Generation) using Llama 3 and ChromaDB.

## 🚀 Quick Start

### Prerequisites
1. **Python 3.9+** installed
2. **Ollama** installed ([ollama.ai](https://ollama.ai))
3. **Llama 3 model** downloaded

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama (in separate terminal)
ollama serve

# Download Llama 3 model (one-time, ~4.7GB)
ollama pull llama3

# Start backend server
python main.py
```

Server will run at: `http://localhost:8000`

## 📚 Upload Textbooks

### Method 1: Interactive Helper Script
```bash
python upload_helper.py
```

### Method 2: Direct API Call
```bash
curl -X POST "http://localhost:8000/upload-textbook" \
  -F "file=@textbook.pdf" \
  -F "title=Grade 10 Mathematics" \
  -F "subject=Mathematics" \
  -F "grade_level=10"
```

## 🔌 API Endpoints

### `POST /upload-textbook`
Upload a textbook PDF for processing

**Parameters:**
- `file`: PDF file
- `title`: Textbook title
- `subject`: Subject name (e.g., "Mathematics")
- `grade_level`: Grade level (9-12)

### `POST /ask`
Ask the AI tutor a question

**Body:**
```json
{
  "student_id": "student_123",
  "subject": "Mathematics",
  "question": "Explain the Pythagorean theorem",
  "grade_level": 10
}
```

**Response:**
```json
{
  "answer": "The Pythagorean theorem states...",
  "sources": [
    {
      "textbook": "Grade 10 Mathematics",
      "page": 42,
      "relevance": 1
    }
  ],
  "confidence": "high"
}
```

### `GET /subjects`
List all available subjects

### `GET /health`
Check system health (Ollama status, database)

## 🗄️ Database

Textbooks are stored in `./textbook_db` directory (ChromaDB).

To reset database, delete this folder.

## 🔧 Configuration

Edit `main.py` to change:
- Port (default: 8000)
- Ollama URL (default: localhost:11434)
- Model name (default: llama3)
- Number of search results (default: 3)

## ⚡ Performance Tips

- **GPU recommended** for faster responses
- First query is slow (model loading)
- Subsequent queries are fast (~2-5 seconds)
- Use `llama3:8b` for faster (but less accurate) responses

## 🐛 Troubleshooting

**"Connection refused"**
- Start Ollama: `ollama serve`

**"Model not found"**
- Download model: `ollama pull llama3`

**Slow responses**
- Use GPU if available
- Try smaller model: `ollama pull llama3:8b`

**CORS errors**
- Already configured for all origins
- Check frontend is calling correct port

## 📊 System Requirements

**Minimum:**
- 8GB RAM
- 10GB storage
- CPU (slow but works)

**Recommended:**
- 16GB+ RAM
- NVIDIA GPU with 6GB+ VRAM
- 50GB storage (for multiple textbooks)
