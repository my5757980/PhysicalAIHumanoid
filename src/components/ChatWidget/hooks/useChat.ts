import { useState, useCallback } from 'react';
import { type Citation, type Message } from '../types';
import { CHAT_API_BASE } from '../config';

/** Generate a simple random ID for message deduplication */
function nanoid(): string {
  return Math.random().toString(36).slice(2, 10);
}

/** Max history turns sent to backend per request (matches MAX_HISTORY_TURNS env var) */
const MAX_HISTORY_TURNS = 12;

export interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (
    question: string,
    selectedText?: string,
    userLevel?: 'beginner' | 'intermediate' | 'advanced' | null,
    translateTo?: 'urdu' | null,
  ) => Promise<void>;
  clearHistory: () => void;
}

/**
 * Core state management hook for the RAG chat widget.
 *
 * Features:
 *   - Sends messages to /chat or /chat/selected via Fetch + ReadableStream
 *     (NOT EventSource — EventSource doesn't support POST bodies)
 *   - Accumulates streamed delta content into the assistant message
 *   - Parses citations from the SSE "citations" event
 *   - Maintains multi-turn conversation history (last MAX_HISTORY_TURNS turns)
 *   - Handles network errors gracefully with a user-visible fallback message
 *
 * Bonus hooks:
 *   - userLevel → sent as user_level in ChatRequest (T024 personalization)
 *   - translateTo → sent as translate_to in ChatRequest (T025 Urdu)
 */
export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (
      question: string,
      selectedText?: string,
      userLevel?: 'beginner' | 'intermediate' | 'advanced' | null,
      translateTo?: 'urdu' | null,
    ) => {
      if (!question.trim() || isLoading) return;

      const userMsgId = nanoid();
      const assistantMsgId = nanoid();

      const userMsg: Message = {
        id: userMsgId,
        role: 'user',
        content: question,
        citations: [],
        timestamp: new Date(),
      };

      const assistantMsg: Message = {
        id: assistantMsgId,
        role: 'assistant',
        content: '',
        citations: [],
        timestamp: new Date(),
        isStreaming: true,
      };

      setMessages((prev) => [...prev, userMsg, assistantMsg]);
      setIsLoading(true);
      setError(null);

      // Build history from prior messages (exclude the just-added pair)
      const historySlice = messages.slice(-MAX_HISTORY_TURNS);
      const history = historySlice.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      // Route to /chat/selected if selected text is provided
      const endpoint = selectedText?.trim() ? '/chat/selected' : '/chat';

      const body: Record<string, unknown> = {
        question,
        history,
        page_url:
          typeof window !== 'undefined' ? window.location.pathname : undefined,
      };

      if (selectedText?.trim()) body.selected_text = selectedText.trim();
      if (userLevel) body.user_level = userLevel;
      if (translateTo) body.translate_to = translateTo;

      try {
        const response = await fetch(`${CHAT_API_BASE}${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });

        if (!response.ok) {
          throw new Error(`Server error ${response.status}`);
        }
        if (!response.body) {
          throw new Error('No response body received');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });

          // SSE events are separated by double newlines
          const parts = buffer.split('\n\n');
          buffer = parts.pop() ?? '';

          for (const part of parts) {
            const trimmed = part.trim();
            if (!trimmed.startsWith('data: ')) continue;

            try {
              const chunk = JSON.parse(trimmed.slice(6));

              if (chunk.type === 'delta' && chunk.content) {
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId
                      ? { ...m, content: m.content + (chunk.content as string) }
                      : m,
                  ),
                );
              } else if (chunk.type === 'citations') {
                const citations: Citation[] = chunk.citations ?? [];
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId
                      ? { ...m, citations, isStreaming: false }
                      : m,
                  ),
                );
              } else if (chunk.type === 'error') {
                throw new Error(
                  (chunk.error as string) ?? 'Unknown streaming error',
                );
              }
            } catch (parseErr) {
              // Ignore malformed SSE lines — stream continues
            }
          }
        }
      } catch (err) {
        const message =
          err instanceof Error ? err.message : 'Connection failed';
        setError(message);
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId
              ? {
                  ...m,
                  content:
                    'Sorry, I encountered an error connecting to the assistant. Please try again.',
                  isStreaming: false,
                }
              : m,
          ),
        );
      } finally {
        setIsLoading(false);
        // Ensure isStreaming is cleared even if citations event was missed
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId ? { ...m, isStreaming: false } : m,
          ),
        );
      }
    },
    [messages, isLoading],
  );

  const clearHistory = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return { messages, isLoading, error, sendMessage, clearHistory };
}
