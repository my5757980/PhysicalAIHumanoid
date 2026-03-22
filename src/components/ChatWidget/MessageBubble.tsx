import React from 'react';
import type { Message } from './types';
import CitationList from './CitationList';
import styles from './styles.module.css';

interface MessageBubbleProps {
  message: Message;
}

/**
 * Renders a single chat message bubble.
 *
 * Features:
 *   - User messages: right-aligned, black background
 *   - Assistant messages: left-aligned, light grey background
 *   - Markdown rendered as plain text (formatting preserved via pre-wrap)
 *   - Blinking cursor (▌) shown while isStreaming=true
 *   - Citations shown below assistant messages after streaming completes
 *
 * Note: react-markdown is intentionally avoided here to keep the bundle small
 * and avoid SSR issues. Markdown symbols in responses are still readable as-is.
 * To enable rich markdown rendering, replace the <p> with <ReactMarkdown>.
 */
export default function MessageBubble({ message }: MessageBubbleProps): JSX.Element {
  const isUser = message.role === 'user';

  return (
    <div
      className={`${styles.bubble} ${isUser ? styles.userBubble : styles.assistantBubble}`}
      role="article"
      aria-label={`${message.role} message`}
    >
      <div className={styles.bubbleRole}>{isUser ? 'You' : 'Assistant'}</div>
      <div className={styles.bubbleContent}>
        {/* Preserve newlines and markdown-style formatting */}
        <p style={{ whiteSpace: 'pre-wrap', margin: 0 }}>
          {message.content}
          {message.isStreaming && (
            <span className={styles.cursor} aria-hidden="true">
              ▌
            </span>
          )}
        </p>
      </div>
      {!isUser && !message.isStreaming && message.citations.length > 0 && (
        <CitationList citations={message.citations} />
      )}
    </div>
  );
}
