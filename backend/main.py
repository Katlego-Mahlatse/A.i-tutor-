"""
Smart School OS - AI Tutor Backend with RAG
Uses Llama 3 + ChromaDB for accurate, textbook-grounded answers
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import PyPDF2
import io
import requests
from typing import List, Optional
import json

app = FastAPI(title="Smart School OS - AI Tutor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.PersistentClient(path="./textbook_db")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

textbook_collection = chroma_client.get_or_create_collection(
    name="textbooks",
    embedding_function=sentence_transformer_ef
)

class Question(BaseModel):
    student_id: str
    subject: str
    question: str
    grade_level: Optional[int] = 9

class Answer(BaseModel):
    answer: str
    sources: List[dict]
    confidence: str

class TextbookMetadata(BaseModel):
    title: str
    subject: str
    grade_level: int
    author: Optional[str] = None

OLLAMA_URL = "http://localhost:11434/api/generate"

def call_llama3(prompt: str, context: str = "") -> str:
    full_prompt = f"""You are a helpful high school tutor. Answer based ONLY on the provided textbook context.

Context from textbook:
{context}

Student question: {prompt}

Instructions:
- Answer clearly and concisely
- Use simple language appropriate for high school
- If the context doesn't contain the answer, say "I don't have information about this in the textbook"
- Reference specific concepts from the context
- Break down complex topics step-by-step

Answer:"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": "llama3", "prompt": full_prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Llama 3 error: {str(e)}")

def extract_text_from_pdf(pdf_file) -> List[dict]:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    chunks = []
    
    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text.strip():
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                if len(para.strip()) > 50:
                    chunks.append({
                        "text": para.strip(),
                        "page": page_num + 1,
                        "length": len(para)
                    })
    
    return chunks

@app.post("/upload-textbook")
async def upload_textbook(
    file: UploadFile = File(...),
    title: str = "",
    subject: str = "",
    grade_level: int = 9
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")
    
    try:
        pdf_content = await file.read()
        pdf_file = io.BytesIO(pdf_content)
        chunks = extract_text_from_pdf(pdf_file)
        
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [
            {"title": title, "subject": subject, "grade_level": grade_level, "page": chunk["page"]}
            for chunk in chunks
        ]
        ids = [f"{title}_page{chunk['page']}_chunk{i}" for i, chunk in enumerate(chunks)]
        
        textbook_collection.add(documents=texts, metadatas=metadatas, ids=ids)
        
        return {
            "status": "success",
            "title": title,
            "chunks_processed": len(chunks),
            "total_pages": max(c["page"] for c in chunks)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    anonymous_question = question.question
    
    results = textbook_collection.query(
        query_texts=[anonymous_question],
        n_results=3,
        where={"subject": question.subject}
    )
    
    if not results["documents"][0]:
        return Answer(
            answer="I don't have any textbook information loaded for this subject yet. Please ask your teacher to upload the textbook.",
            sources=[],
            confidence="none"
        )
    
    context_parts = []
    sources = []
    
    for i, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        context_parts.append(f"[Source {i+1}, Page {metadata['page']}]:\n{doc}\n")
        sources.append({
            "textbook": metadata["title"],
            "page": metadata["page"],
            "relevance": i + 1
        })
    
    context = "\n".join(context_parts)
    answer_text = call_llama3(anonymous_question, context)
    confidence = "high" if len(results["documents"][0]) >= 2 else "medium"
    
    return Answer(answer=answer_text, sources=sources, confidence=confidence)

@app.get("/subjects")
async def get_subjects():
    all_docs = textbook_collection.get()
    subjects = set()
    
    if all_docs["metadatas"]:
        for metadata in all_docs["metadatas"]:
            subjects.add(metadata["subject"])
    
    return {"subjects": list(subjects)}

@app.get("/health")
async def health_check():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        ollama_status = "running" if response.status_code == 200 else "error"
    except:
        ollama_status = "not_running"
    
    return {
        "status": "healthy",
        "ollama": ollama_status,
        "textbooks_loaded": textbook_collection.count()
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Smart School OS - AI Tutor Backend")
    print("📚 Make sure Ollama is running: ollama serve")
    print("🤖 Make sure Llama 3 is installed: ollama pull llama3")
    uvicorn.run(app, host="0.0.0.0", port=8000)
