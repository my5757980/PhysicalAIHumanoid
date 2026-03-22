import React from 'react';
import type { Citation } from './types';
import styles from './styles.module.css';

interface CitationListProps {
  citations: Citation[];
}

/**
 * Renders a compact list of chapter/section citations below an assistant message.
 * Displayed after streaming completes (when isStreaming=false).
 */
export default function CitationList({
  citations,
}: CitationListProps): JSX.Element | null {
  if (citations.length === 0) return null;

  return (
    <div className={styles.citations}>
      <span className={styles.citationsLabel}>Sources:</span>
      <ul className={styles.citationsList}>
        {citations.map((c, i) => (
          <li key={i} className={styles.citationItem}>
            <span className={styles.citationChapter}>Ch.{c.chapter_num}</span>
            {' — '}
            <span className={styles.citationTitle}>{c.chapter_title}</span>
            {c.section_title && (
              <>
                {' › '}
                <span className={styles.citationSection}>{c.section_title}</span>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
