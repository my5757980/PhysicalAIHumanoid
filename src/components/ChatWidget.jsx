// ChatWidget.jsx
import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import './ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(null);
  const [isUserSelectedMode, setIsUserSelectedMode] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const getSelectedText = () => window.getSelection()?.toString().trim() || null;

  useEffect(() => {
    const handleSelection = () => {
      const text = getSelectedText();
      if (text) {
        setSelectedText(text);
        setIsUserSelectedMode(true);
      } else {
        setIsUserSelectedMode(false);
      }
    };
    const escHandler = (e) => { if (e.key === 'Escape') { setSelectedText(null); setIsUserSelectedMode(false); } };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', escHandler);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', escHandler);
    };
  }, []);

  const scrollToBottom = () => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); };
  useEffect(() => { scrollToBottom(); }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { type: 'user', content: inputValue };
    const currentSelectedText = isUserSelectedMode ? selectedText : null;

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/ask_stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: inputValue,
          selected_text: currentSelectedText,
          max_results: 5,
          temperature: 0.7,
        }),
      });

      if (!response.ok) throw new Error(`API error ${response.status}`);
      const data = await response.json();

      const botMessage = {
        type: 'bot',
        content: data.answer || 'No answer generated',
        sources: data.sources || [],
        validation: data.validation || {},
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [...prev, { type: 'bot', content: 'Error occurred. Please try again.' }]);
    } finally {
      setIsLoading(false);
      setIsUserSelectedMode(false);
      setSelectedText(null);
    }
  };

  const handleKeyPress = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } };
  const toggleChat = () => { setIsOpen(!isOpen); if (!isOpen) setTimeout(() => inputRef.current?.focus(), 150); };
  const clearChat = () => setMessages([]);

  if (!isOpen) {
    return (
      <div className="chat-widget-fab" onClick={toggleChat}>
        <div className="chat-icon">💬</div>
        {isUserSelectedMode && <div className="selection-indicator"><span>!</span></div>}
      </div>
    );
  }

  return createPortal(
    <div className="chat-widget-overlay">
      <div className="chat-widget">
        <div className="chat-header">
          <div className="chat-title">Physical AI Chatbot</div>
          <div className="chat-controls">
            <button className="chat-clear-btn" onClick={clearChat}>🗑️</button>
            <button className="chat-close-btn" onClick={toggleChat}>✕</button>
          </div>
        </div>

        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="chat-welcome">
              <h3>Welcome to Physical AI & Humanoid Robotics Chatbot!</h3>
              <p>Ask anything about the textbook.</p>
              {isUserSelectedMode && (
                <div className="selected-text-prompt">
                  <p><strong>Selected text detected:</strong></p>
                  <p>"{selectedText?.substring(0, 120)}..."</p>
                </div>
              )}
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`chat-message ${msg.type}`}>
                <div className="message-content">
                  {msg.type === 'bot' && msg.sources?.length > 0 && (
                    <details>
                      <summary>Sources ({msg.sources.length})</summary>
                      <ul>
                        {msg.sources.slice(0, 3).map((s, idx) => (
                          <li key={idx}><strong>{s.chapter}</strong>: {s.section}</li>
                        ))}
                      </ul>
                    </details>
                  )}
                  {msg.type === 'bot' && msg.validation && (
                    <div className={`validation-indicator ${msg.validation.has_hallucination ? 'warning' : 'success'}`}>
                      <strong>{msg.validation.has_hallucination ? '⚠️ Potential issue detected' : '✅ Answer validated'}</strong>
                      <p>{msg.validation.message}</p>
                    </div>
                  )}
                  <div className="message-text">
                    {msg.content.split('\n').map((line, j) => <p key={j}>{line}</p>)}
                  </div>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="chat-message bot">
              <div className="typing-indicator"><span></span><span></span><span></span></div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder={isUserSelectedMode ? "Ask about the selected text…" : "Ask about Physical AI & Humanoid Robotics…"}
            rows={2}
            disabled={isLoading}
          />
          <button className="send-button" onClick={sendMessage} disabled={!inputValue.trim() || isLoading}>
            {isLoading ? 'Sending…' : 'Send'}
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
};

export default ChatWidget;
