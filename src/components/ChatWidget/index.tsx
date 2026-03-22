import React, { useState } from 'react';
import ChatPanel from './ChatPanel';
import { useChat } from './hooks/useChat';
import { useTextSelection } from './hooks/useTextSelection';
import styles from './styles.module.css';

/**
 * ChatWidget — root toggle component.
 *
 * Responsibilities:
 *   1. Render the floating toggle button (bottom-right).
 *   2. Mount/unmount the ChatPanel when open/closed.
 *   3. Wire useChat + useTextSelection hooks and pass props down.
 */
export default function ChatWidget(): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);

  const chat = useChat();
  const { selectedText, clearSelection } = useTextSelection();

  return (
    <div className={styles.container}>
      {/* Expanded chat panel */}
      {isOpen && (
        <ChatPanel
          chat={chat}
          selectedText={selectedText}
          onClearSelection={clearSelection}
          onClose={() => setIsOpen(false)}
        />
      )}

      {/* Floating toggle button */}
      <button
        type="button"
        className={styles.toggleButton}
        onClick={() => setIsOpen((prev) => !prev)}
        aria-label={isOpen ? 'Close chat' : 'Open Physical AI Assistant'}
        aria-expanded={isOpen}
        title="Physical AI Assistant"
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
}
