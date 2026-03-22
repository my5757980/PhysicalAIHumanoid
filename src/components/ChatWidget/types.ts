/**
 * TypeScript interfaces for the RAG Chat Widget.
 * Shared across all widget components and hooks.
 */

export interface Citation {
  chapter_num: number;
  chapter_title: string;
  section_title: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations: Citation[];
  timestamp: Date;
  /** True while the assistant response is still streaming */
  isStreaming?: boolean;
}

export interface ChatState {
  messages: Message[];
  isOpen: boolean;
  isLoading: boolean;
  /** Text captured via window.getSelection() */
  selectedText: string;
  error: string | null;
}
