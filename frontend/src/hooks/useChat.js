import { useState, useCallback } from 'react';
import { sendMessage as sendMessageAPI } from '../services/api';

const WELCOME_MESSAGE = {
  id: 'welcome',
  role: 'assistant',
  content: `# 👋 Welcome to FinBot!

I'm your **AI-powered Personal Finance Advisor**, specialized in Indian personal finance.

Here's what I can help you with:

- 📊 **Budget Planning** — 50/30/20 rule for your salary
- 🏠 **EMI Calculation** — Home, car, or personal loans
- 📈 **SIP Returns** — Mutual fund investment projections
- 🏦 **Fixed Deposit** — FD maturity & interest calculations
- 🎯 **Savings Goals** — Plan for your dreams
- 💡 **Investment Advice** — PPF, ELSS, NPS, and more

**Try asking:** *"How do I budget ₹45,000 monthly salary?"*`,
  timestamp: new Date(),
};

export function useChat() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const [interactionId, setInteractionId] = useState(null);
  const [error, setError] = useState(null);

  const addMessage = useCallback((message) => {
    setMessages((prev) => [...prev, message]);
  }, []);

  const sendMessage = useCallback(async (text) => {
    if (!text.trim() || isLoading) return;
    setError(null);

    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text.trim(),
      timestamp: new Date(),
    };
    addMessage(userMessage);

    // Add loading placeholder
    const assistantId = (Date.now() + 1).toString();
    addMessage({
      id: assistantId,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true,
    });

    setIsLoading(true);

    try {
      // Use simple /chat endpoint (no streaming) — most reliable
      const result = await sendMessageAPI(text.trim(), interactionId);

      if (result.interaction_id) {
        setInteractionId(result.interaction_id);
      }

      setMessages((prev) => {
        const newMessages = [...prev];
        const lastIdx = newMessages.length - 1;
        if (newMessages[lastIdx].id === assistantId) {
          newMessages[lastIdx] = {
            ...newMessages[lastIdx],
            content: result.reply,
            isStreaming: false,
          };
        }
        return newMessages;
      });
    } catch (err) {
      const errMsg = err.message || 'Network error. Is the backend running on http://localhost:8000?';
      setError(errMsg);
      setMessages((prev) => {
        const newMessages = [...prev];
        const lastIdx = newMessages.length - 1;
        if (newMessages[lastIdx].id === assistantId) {
          newMessages[lastIdx] = {
            ...newMessages[lastIdx],
            content: `⚠️ **Error:** ${errMsg}\n\n**Check:**\n- Is backend running? Visit http://localhost:8000/health\n- Is your GEMINI_API_KEY set in backend/.env?`,
            isStreaming: false,
            isError: true,
          };
        }
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  }, [isLoading, interactionId, addMessage]);

  const clearChat = useCallback(() => {
    setMessages([WELCOME_MESSAGE]);
    setInteractionId(null);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearChat,
  };
}
