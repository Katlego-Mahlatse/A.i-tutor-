import React, { useState, useRef, useEffect } from 'react';
import { Send, Book, Loader, CheckCircle, AlertCircle } from 'lucide-react';

export default function AITutor() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hi! I\'m your AI tutor. Ask me anything about your subjects and I\'ll help you learn!',
      sources: []
    }
  ]);
  const [input, setInput] = useState('');
  const [subject, setSubject] = useState('Mathematics');
  const [loading, setLoading] = useState(false);
  const [subjects, setSubjects] = useState(['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History']);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load available subjects from backend
  useEffect(() => {
    fetch('http://localhost:8000/subjects')
      .then(res => res.json())
      .then(data => {
        if (data.subjects.length > 0) {
          setSubjects(data.subjects);
        }
      })
      .catch(err => console.log('Using default subjects'));
  }, []);

  const askQuestion = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: 'user',
      content: input,
      sources: []
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: 'student_' + Math.random().toString(36).substr(2, 9),
          subject: subject,
          question: input,
          grade_level: 10
        })
      });

      const data = await response.json();

      const assistantMessage = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources || [],
        confidence: data.confidence
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Sorry, I couldn\'t connect to the tutor. Make sure the backend server is running at http://localhost:8000',
        sources: [],
        confidence: 'error'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: 'linear-gradient(to bottom right, #eff6ff, #e0e7ff)' }}>
      {/* Header */}
      <div style={{ background: 'white', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: '#4f46e5', padding: '0.5rem', borderRadius: '0.5rem' }}>
            <Book color="white" size={24} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#1f2937', margin: 0 }}>Smart School AI Tutor</h1>
            <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: 0 }}>Ask questions, get instant help</p>
          </div>
        </div>
        
        {/* Subject Selector */}
        <select
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          style={{ padding: '0.5rem 1rem', border: '2px solid #c7d2fe', borderRadius: '0.5rem', background: 'white', cursor: 'pointer' }}
        >
          {subjects.map(subj => (
            <option key={subj} value={subj}>{subj}</option>
          ))}
        </select>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '1rem' }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{ display: 'flex', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start', marginBottom: '1rem' }}
          >
            <div
              style={{
                maxWidth: '48rem',
                borderRadius: '1rem',
                padding: '1rem',
                background: msg.role === 'user' ? '#4f46e5' : 'white',
                color: msg.role === 'user' ? 'white' : '#1f2937',
                boxShadow: msg.role === 'user' ? 'none' : '0 1px 3px rgba(0,0,0,0.1)'
              }}
            >
              <p style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{msg.content}</p>
              
              {/* Show sources if available */}
              {msg.sources && msg.sources.length > 0 && (
                <div style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid #e5e7eb' }}>
                  <p style={{ fontSize: '0.75rem', fontWeight: '600', color: '#6b7280', marginBottom: '0.5rem' }}>📚 Sources:</p>
                  {msg.sources.map((source, i) => (
                    <div key={i} style={{ fontSize: '0.75rem', color: '#6b7280', display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                      <CheckCircle size={12} color="#10b981" />
                      <span>{source.textbook} - Page {source.page}</span>
                    </div>
                  ))}
                  {msg.confidence && (
                    <div style={{ marginTop: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.75rem' }}>
                      {msg.confidence === 'high' ? (
                        <CheckCircle size={12} color="#10b981" />
                      ) : (
                        <AlertCircle size={12} color="#f59e0b" />
                      )}
                      <span style={{ color: '#6b7280' }}>
                        Confidence: {msg.confidence}
                      </span>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {loading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
            <div style={{ background: 'white', borderRadius: '1rem', padding: '1rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Loader style={{ animation: 'spin 1s linear infinite' }} color="#4f46e5" size={20} />
              <span style={{ color: '#6b7280' }}>Thinking...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{ background: 'white', borderTop: '1px solid #e5e7eb', padding: '1rem' }}>
        <div style={{ maxWidth: '64rem', margin: '0 auto', display: 'flex', gap: '0.5rem' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask your question here..."
            style={{ flex: 1, padding: '0.75rem 1rem', border: '2px solid #d1d5db', borderRadius: '0.75rem', outline: 'none' }}
            disabled={loading}
          />
          <button
            onClick={askQuestion}
            disabled={loading || !input.trim()}
            style={{
              background: loading || !input.trim() ? '#d1d5db' : '#4f46e5',
              color: 'white',
              padding: '0.75rem 1.5rem',
              borderRadius: '0.75rem',
              border: 'none',
              cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <Send size={20} />
            Ask
          </button>
        </div>
        <p style={{ textAlign: 'center', fontSize: '0.75rem', color: '#6b7280', marginTop: '0.5rem' }}>
          All answers are based on your textbooks • Powered by Llama 3
        </p>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
