import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import { useChat } from './hooks/useChat';

export default function App() {
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();

  return (
    <div className="flex flex-col h-screen bg-slate-950">
      <Header onClearChat={clearChat} />

      {/* Error banner */}
      {error && (
        <div className="bg-red-900/30 border-b border-red-700/50 px-4 py-2 text-xs text-red-300 text-center">
          ⚠️ {error}
        </div>
      )}

      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        onSendMessage={sendMessage}
      />
    </div>
  );
}
