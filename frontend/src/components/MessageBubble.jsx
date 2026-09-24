import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { TrendingUp, User, Copy, Check } from 'lucide-react';
import { useState } from 'react';

function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 py-2 px-1">
      <div className="typing-dot" />
      <div className="typing-dot" />
      <div className="typing-dot" />
    </div>
  );
}

export default function MessageBubble({ message }) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('en-IN', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className={`message-enter flex items-end gap-2.5 ${isUser ? 'flex-row-reverse' : 'flex-row'} group`}>
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center
          ${isUser
            ? 'bg-gradient-to-br from-blue-500 to-indigo-600'
            : 'bg-gradient-to-br from-green-400 to-emerald-600'
          }`}
      >
        {isUser
          ? <User size={16} className="text-white" />
          : <TrendingUp size={16} className="text-white" />
        }
      </div>

      {/* Bubble */}
      <div className={`max-w-[78%] relative ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed
            ${isUser
              ? 'bg-gradient-to-br from-blue-600 to-indigo-700 text-white rounded-br-sm'
              : message.isError
                ? 'bg-red-900/40 border border-red-700/50 text-red-200 rounded-bl-sm'
                : 'bg-slate-800 border border-slate-700 text-slate-100 rounded-bl-sm'
            }`}
        >
          {/* Show typing indicator if streaming with no content yet */}
          {message.isStreaming && !message.content ? (
            <TypingIndicator />
          ) : isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="markdown-content">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            </div>
          )}

          {/* Streaming cursor */}
          {message.isStreaming && message.content && (
            <span className="inline-block w-0.5 h-4 bg-green-400 ml-0.5 animate-pulse align-middle" />
          )}
        </div>

        {/* Timestamp + Copy button */}
        <div className={`flex items-center gap-2 mt-1 px-1 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
          <span className="text-xs text-slate-500">{formatTime(message.timestamp)}</span>
          {!isUser && !message.isStreaming && message.content && (
            <button
              onClick={handleCopy}
              className="opacity-0 group-hover:opacity-100 transition-opacity text-slate-500 hover:text-slate-300"
              title="Copy message"
            >
              {copied
                ? <Check size={12} className="text-green-400" />
                : <Copy size={12} />
              }
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
