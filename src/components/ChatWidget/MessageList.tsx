import React, { useEffect, useRef } from 'react';
import type { Message } from './types';
import MessageBubble from './MessageBubble';
import styles from './styles.module.css';

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

/**
 * Scrollable container for chat message history.
 * Auto-scrolls to the bottom when new messages arrive or content streams in.
 */
export default function MessageList({
  messages,
  isLoading,
}: MessageListProps): JSX.Element {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages update
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className={styles.emptyState}>
        <p className={styles.emptyTitle}>Physical AI Assistant</p>
        <p className={styles.emptyHint}>
          Ask a question about the textbook, or select any text on the page and
          ask about it.
        </p>
      </div>
    );
  }

  return (
    <div className={styles.messageList} role="log" aria-live="polite" aria-label="Chat messages">
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
