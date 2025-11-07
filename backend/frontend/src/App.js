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
  const [subjects, setSubjects] = useState(['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History
