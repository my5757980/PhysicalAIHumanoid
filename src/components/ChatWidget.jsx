// ChatWidget.jsx
import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import './ChatWidget.css';

const API_URL =
  import.meta.env.VITE_BACKEND_URL || '/api/ask_stream';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const question = inputValue;

    setMessages(prev => [...prev, { type: 'user', content: question }]);
    setInputValue('');
    setIsLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: question,
          max_results: 5,
          temperature: 0.7,
        }),
      });

      if (!res.ok) {
        throw new Error(`API error ${res.status}`);
      }

      const data = await res.json();

      setMessages(prev => [
        ...prev,
        {
          type: 'bot',
          content: data.answer || 'No answer generated.',
          sources: data.sources || [],
          confidence: data.validation?.confidence_score ?? null,
        },
      ]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { type: 'bot', content: '❌ Error occurred. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) {
    return (
      <div className="chat-widget-fab" onClick={() => setIsOpen(true)}>
        💬
      </div>
    );
  }

  return createPortal(
    <div className="chat-widget-overlay">
      <div className="chat-widget">
        <div className="chat-header">
          <strong>Physical AI Chatbot</strong>
          <button onClick={() => setIsOpen(false)}>✕</button>
        </div>

        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-message ${msg.type}`}>
              <div className="message-text">
                {msg.content.split('\n').map((l, j) => <p key={j}>{l}</p>)}
              </div>

              {msg.type === 'bot' && msg.confidence !== null && (
                <div className="confidence">
                  Confidence: {(msg.confidence * 100).toFixed(0)}%
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="chat-message bot">Typing…</div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={e => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask about Physical AI & Humanoid Robotics…"
            rows={2}
            disabled={isLoading}
          />
          <button onClick={sendMessage} disabled={isLoading || !inputValue.trim()}>
            Send
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
};

export default ChatWidget;
