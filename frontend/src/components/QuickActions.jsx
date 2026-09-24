const QUICK_ACTIONS = [
  {
    emoji: '📊',
    label: 'Budget Planner',
    prompt: 'Help me create a monthly budget plan for a salary of ₹50,000',
  },
  {
    emoji: '🏠',
    label: 'EMI Calculator',
    prompt: 'Calculate EMI for a ₹20 lakh home loan at 8.5% interest for 20 years',
  },
  {
    emoji: '📈',
    label: 'SIP Returns',
    prompt: 'If I invest ₹5,000 per month in SIP for 10 years at 12% returns, how much will I get?',
  },
  {
    emoji: '🏦',
    label: 'FD Calculator',
    prompt: 'Calculate returns for ₹1,00,000 FD at 7% for 3 years with quarterly compounding',
  },
  {
    emoji: '🎯',
    label: 'Savings Goal',
    prompt: 'I want to save ₹5,00,000 for a car. I have ₹50,000 saved and can invest ₹15,000/month at 7% returns. How long will it take?',
  },
  {
    emoji: '💡',
    label: 'Tax Saving Tips',
    prompt: 'How can I save income tax under Section 80C? I am in the 30% tax bracket.',
  },
  {
    emoji: '🆘',
    label: 'Emergency Fund',
    prompt: 'How much emergency fund should I maintain and where should I keep it?',
  },
  {
    emoji: '📉',
    label: 'Debt Free Plan',
    prompt: 'I have ₹2 lakh credit card debt at 36% interest. Help me plan to become debt free.',
  },
];

export default function QuickActions({ onSelect, disabled }) {
  return (
    <div className="px-4 pb-3">
      <p className="text-xs text-slate-500 mb-2 font-medium uppercase tracking-wide">Quick Actions</p>
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-thin">
        {QUICK_ACTIONS.map((action) => (
          <button
            key={action.label}
            onClick={() => onSelect(action.prompt)}
            disabled={disabled}
            className="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-800
                       border border-slate-700 hover:border-green-500/50 hover:bg-slate-700
                       rounded-full text-xs text-slate-300 hover:text-white
                       transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed
                       whitespace-nowrap"
          >
            <span>{action.emoji}</span>
            <span>{action.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
