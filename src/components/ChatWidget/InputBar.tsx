import React, { useState, useRef, type KeyboardEvent } from 'react';
import styles from './styles.module.css';

interface InputBarProps {
  onSend: (text: string) => void;
  disabled: boolean;
  placeholder?: string;
}

/**
 * Chat input bar with send button.
 *
 * Keyboard behaviour:
 *   Enter          → send message
 *   Shift + Enter  → insert newline (multi-line input)
 */
export default function InputBar({
  onSend,
  disabled,
  placeholder = 'Ask about the textbook…',
}: InputBarProps): JSX.Element {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue('');
    // Reset textarea height after send
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = () => {
    // Auto-resize textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  return (
    <div className={styles.inputBar}>
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        onInput={handleInput}
        disabled={disabled}
        placeholder={placeholder}
        rows={1}
        className={styles.textarea}
        aria-label="Chat input"
        aria-multiline="true"
      />
      <button
        type="button"
        onClick={handleSubmit}
        disabled={disabled || !value.trim()}
        className={styles.sendButton}
        aria-label="Send message"
        title="Send (Enter)"
      >
        {disabled ? '…' : '→'}
      </button>
    </div>
  );
}
