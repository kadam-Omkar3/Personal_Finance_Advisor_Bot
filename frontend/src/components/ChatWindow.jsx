import { useEffect, useRef, useState, useCallback } from 'react';
import MessageBubble from './MessageBubble';
import QuickActions from './QuickActions';
import { Send, Mic, MicOff } from 'lucide-react';

export default function ChatWindow({ messages, isLoading, onSendMessage }) {
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);
  const recognitionRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = useCallback(() => {
    const text = input.trim();
    if (!text || isLoading) return;
    setInput('');
    onSendMessage(text);
  }, [input, isLoading, onSendMessage]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleQuickAction = (prompt) => {
    setInput(prompt);
    inputRef.current?.focus();
  };

  // Voice input (Web Speech API)
  const toggleVoice = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Voice input is not supported in this browser. Try Chrome.');
      return;
    }

    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      setInput((prev) => prev + (prev ? ' ' : '') + transcript);
    };
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
  };

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto chat-scroll px-4 py-4 space-y-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Quick actions */}
      <QuickActions onSelect={handleQuickAction} disabled={isLoading} />

      {/* Input area */}
      <div className="px-4 pb-4">
        <div className={`flex items-end gap-2 bg-slate-800 border rounded-2xl p-3 transition-colors
            ${isLoading ? 'border-slate-700' : 'border-slate-600 focus-within:border-green-500/60'}`}
        >
          {/* Textarea */}
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about budgeting, EMI, SIP, investments..."
            rows={1}
            className="flex-1 bg-transparent text-slate-100 placeholder-slate-500 text-sm
                       resize-none outline-none max-h-32 leading-relaxed py-0.5"
            style={{ height: 'auto', minHeight: '24px' }}
            onInput={(e) => {
              e.target.style.height = 'auto';
              e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px';
            }}
            disabled={isLoading}
          />

          {/* Voice button */}
          <button
            onClick={toggleVoice}
            title={isListening ? 'Stop listening' : 'Voice input'}
            className={`p-1.5 rounded-xl transition-colors flex-shrink-0
              ${isListening
                ? 'text-red-400 bg-red-400/10 animate-pulse'
                : 'text-slate-500 hover:text-slate-300 hover:bg-slate-700'
              }`}
          >
            {isListening ? <MicOff size={16} /> : <Mic size={16} />}
          </button>

          {/* Send button */}
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="p-1.5 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl
                       text-white hover:from-green-400 hover:to-emerald-500
                       disabled:opacity-40 disabled:cursor-not-allowed
                       transition-all duration-200 flex-shrink-0 shadow-md"
          >
            <Send size={16} />
          </button>
        </div>

        {/* Hint */}
        <p className="text-xs text-slate-600 text-center mt-2">
          FinBot can make mistakes. Always verify financial decisions with a qualified advisor.
        </p>
      </div>
    </div>
  );
}
