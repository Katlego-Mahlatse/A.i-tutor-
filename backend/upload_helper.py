"""
Textbook Upload Helper
Easy script to upload textbooks to your AI tutor system
"""

import requests
import os
from pathlib import Path

API_URL = "http://localhost:8000"

def upload_textbook(pdf_path, title, subject, grade_level):
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return False
    
    print(f"📤 Uploading: {title}...")
    print(f"   Subject: {subject} | Grade: {grade_level}")
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            data = {'title': title, 'subject': subject, 'grade_level': grade_level}
            
            response = requests.post(f"{API_URL}/upload-textbook", files=files, data=data, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"   Processed: {result['chunks_processed']} text chunks")
                print(f"   Total pages: {result['total_pages']}")
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return False
                
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend server")
        print("   Make sure the backend is running: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def check_system_status():
    print("🔍 Checking system status...")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ Backend is running")
            print(f"   Ollama status: {status['ollama']}")
            print(f"   Textbooks loaded: {status['textbooks_loaded']}")
            return True
        else:
            print("❌ Backend is not responding properly")
            return False
    except:
        print("❌ Backend is not running")
        print("   Start it with: python main.py")
        return False

def list_subjects():
    try:
        response = requests.get(f"{API_URL}/subjects")
        if response.status_code == 200:
            subjects = response.json()['subjects']
            if subjects:
                print("\n📚 Available subjects:")
                for subject in subjects:
                    print(f"   - {subject}")
            else:
                print("\n📚 No textbooks uploaded yet")
            return subjects
    except:
        print("❌ Cannot retrieve subjects list")
        return []

def interactive_mode():
    print("\n" + "=" * 50)
    print("📚 SMART SCHOOL OS - Textbook Upload Helper")
    print("=" * 50)
    
    if not check_system_status():
        return
    
    list_subjects()
    
    while True:
        print("\n" + "=" * 50)
        print("Options:")
        print("1. Upload single textbook")
        print("2. Check system status")
        print("3. List available subjects")
        print("4. Exit")
        print("=" * 50)
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            print("\n📖 Single Textbook Upload")
            pdf_path = input("PDF file path: ").strip()
            title = input("Textbook title: ").strip()
            subject = input("Subject (e.g., Mathematics, Physics): ").strip()
            grade_str = input("Grade level (9-12): ").strip()
            
            try:
                grade_level = int(grade_str)
                upload_textbook(pdf_path, title, subject, grade_level)
            except ValueError:
                print("❌ Invalid grade level")
        
        elif choice == "2":
            check_system_status()
        
        elif choice == "3":
            list_subjects()
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    interactive_mode()
