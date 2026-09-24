import { TrendingUp, Wifi, RefreshCw } from 'lucide-react';

export default function Header({ onClearChat }) {
  return (
    <header className="bg-slate-900 border-b border-slate-700 px-4 py-3 flex items-center justify-between shadow-lg">
      {/* Logo & Title */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 bg-gradient-to-br from-green-400 to-emerald-600 rounded-xl flex items-center justify-center shadow-md">
          <TrendingUp size={20} className="text-white" />
        </div>
        <div>
          <h1 className="text-white font-bold text-lg leading-tight">FinBot</h1>
          <p className="text-slate-400 text-xs">AI Personal Finance Advisor</p>
        </div>
      </div>

      {/* Status & Actions */}
      <div className="flex items-center gap-3">
        {/* Online Indicator */}
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse-slow" />
          <span className="text-slate-400 text-xs hidden sm:block">Online</span>
        </div>

        {/* New Chat Button */}
        <button
          onClick={onClearChat}
          title="Start new chat"
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs text-slate-400 hover:text-white
                     hover:bg-slate-700 rounded-lg transition-colors duration-200 border border-slate-700"
        >
          <RefreshCw size={13} />
          <span className="hidden sm:block">New Chat</span>
        </button>
      </div>
    </header>
  );
}
