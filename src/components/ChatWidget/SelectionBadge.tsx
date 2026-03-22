import React from 'react';
import styles from './styles.module.css';

interface SelectionBadgeProps {
  text: string;
  onClear: () => void;
}

/**
 * Displays a badge showing the currently highlighted text from the page.
 * Renders only when `text` is non-empty (controlled by useTextSelection hook).
 *
 * Clicking ✕ calls onClear() to dismiss the selection context.
 */
export default function SelectionBadge({
  text,
  onClear,
}: SelectionBadgeProps): JSX.Element | null {
  if (!text) return null;

  const preview = text.length > 80 ? `${text.slice(0, 80)}…` : text;

  return (
    <div className={styles.selectionBadge} role="status" aria-label="Selected text context">
      <span className={styles.selectionLabel}>Asking about: </span>
      <span className={styles.selectionPreview}>"{preview}"</span>
      <button
        className={styles.selectionClear}
        onClick={onClear}
        aria-label="Clear selected text"
        type="button"
      >
        ✕
      </button>
    </div>
  );
}
