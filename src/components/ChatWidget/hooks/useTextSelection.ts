import { useState, useEffect } from 'react';

/**
 * Captures text selected (highlighted) by the user on any page.
 *
 * Behaviour:
 *   - Listens for `selectionchange` events (debounced 300ms)
 *   - Min length: 20 characters (avoids capturing accidental clicks)
 *   - Max length: 1500 characters (matches backend selected_text limit)
 *   - Returns empty string when nothing meaningful is selected
 *
 * @returns [selectedText, clearSelection]
 */
export function useTextSelection(): [string, () => void] {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    let debounceTimer: ReturnType<typeof setTimeout>;

    const handleSelectionChange = () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        const selection = window.getSelection()?.toString().trim() ?? '';
        if (selection.length >= 20) {
          setSelectedText(selection.slice(0, 1500));
        } else {
          setSelectedText('');
        }
      }, 300);
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      clearTimeout(debounceTimer);
    };
  }, []);

  const clearSelection = () => setSelectedText('');

  return [selectedText, clearSelection];
}
