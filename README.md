# 🎓 Smart School OS - AI Tutor

AI-powered tutoring system using RAG to provide textbook-grounded answers.

## ✨ Features

- 🤖 AI Tutor powered by Llama 3
- 📚 Textbook Search with page citations
- 🔒 100% Local & Private
- 💰 Free to run
- 🌐 Multi-Subject support

## 🚀 Quick Start

### Prerequisites
1. Python 3.9+
2. Node.js 16+
3. Ollama ([Download](https://ollama.ai))

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
ollama serve
ollama pull llama3
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Upload Textbooks
```bash
cd backend
python upload_helper.py
```

## 📁 Structure

```
Ai-tutor/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── upload_helper.py
│   └── README.md
├── frontend/
│   ├── src/
│   │   └── App.js
│   ├── package.json
│   └── README.md
├── .gitignore
└── README.md
```

## 🔧 How It Works

1. Student asks question
2. System searches textbook database
3. Retrieves relevant passages
4. Llama 3 answers from context only
5. Returns answer with page citations

## 🌟 Benefits

- No hallucinations (textbook-only answers)
- Exact page citations
- Works offline
- Zero ongoing costs
- Unlimited students

---

**Built with:** Python, FastAPI, React, Llama 3, ChromaDB
