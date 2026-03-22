import React, { useState } from 'react';
import type { UseChatReturn } from './hooks/useChat';
import MessageList from './MessageList';
import SelectionBadge from './SelectionBadge';
import InputBar from './InputBar';
import styles from './styles.module.css';

interface ChatPanelProps {
  chat: UseChatReturn;
  selectedText: string;
  onClearSelection: () => void;
  onClose: () => void;
}

/**
 * Expanded chat panel — assembles all sub-components into the full chat UI.
 *
 * Bonus hooks:
 *   - userLevel state: drives user_level in ChatRequest (T024 personalization)
 *   - translateTo state: drives translate_to in ChatRequest (T025 Urdu)
 */
export default function ChatPanel({
  chat,
  selectedText,
  onClearSelection,
  onClose,
}: ChatPanelProps): JSX.Element {
  // ── Bonus: personalization level selector (T024) ───────────────────────────
  const [userLevel, setUserLevel] = useState<
    'beginner' | 'intermediate' | 'advanced' | null
  >(null);

  // ── Bonus: Urdu language toggle (T025) ────────────────────────────────────
  const [translateTo, setTranslateTo] = useState<'urdu' | null>(null);

  const handleSend = (question: string) => {
    chat.sendMessage(question, selectedText || undefined, userLevel, translateTo);
    // Clear the text selection context after sending
    if (selectedText) onClearSelection();
  };

  return (
    <div className={styles.panel} role="dialog" aria-label="Physical AI Assistant">
      {/* Header */}
      <div className={styles.panelHeader}>
        <span>Physical AI Assistant</span>
        <div className={styles.headerActions}>
          {/* Bonus: Level selector (T024) */}
          <div className={styles.levelSelector} title="Adjust explanation depth">
            {(['B', 'I', 'A'] as const).map((label, i) => {
              const levels = ['beginner', 'intermediate', 'advanced'] as const;
              const level = levels[i];
              return (
                <button
                  key={level}
                  type="button"
                  className={`${styles.levelBtn} ${userLevel === level ? styles.levelBtnActive : ''}`}
                  onClick={() => setUserLevel(userLevel === level ? null : level)}
                  title={`${level} level`}
                  aria-pressed={userLevel === level}
                >
                  {label}
                </button>
              );
            })}
          </div>
          {/* Bonus: Urdu toggle (T025) */}
          <button
            type="button"
            className={`${styles.langToggle} ${translateTo === 'urdu' ? styles.langToggleActive : ''}`}
            onClick={() => setTranslateTo(translateTo === 'urdu' ? null : 'urdu')}
            title="Toggle Urdu translation"
            aria-pressed={translateTo === 'urdu'}
          >
            {translateTo === 'urdu' ? 'اردو' : 'EN'}
          </button>
          {/* Clear history */}
          <button
            type="button"
            className={styles.clearBtn}
            onClick={chat.clearHistory}
            title="Clear chat history"
            aria-label="Clear conversation"
          >
            ↺
          </button>
          {/* Close panel */}
          <button
            type="button"
            className={styles.closeBtn}
            onClick={onClose}
            aria-label="Close chat"
          >
            ✕
          </button>
        </div>
      </div>

      {/* Selected text badge */}
      {selectedText && (
        <SelectionBadge text={selectedText} onClear={onClearSelection} />
      )}

      {/* Message list */}
      <MessageList messages={chat.messages} isLoading={chat.isLoading} />

      {/* Error banner */}
      {chat.error && (
        <div className={styles.errorBanner} role="alert">
          {chat.error}
        </div>
      )}

      {/* Input */}
      <InputBar
        onSend={handleSend}
        disabled={chat.isLoading}
        placeholder={
          selectedText
            ? 'Ask about the selected text…'
            : 'Ask about the textbook…'
        }
      />
    </div>
  );
}
