import React, { useState, useEffect, useRef } from 'react';

export default function AIAssistantPage({ onNavigate }) {
  // Theme state with localStorage persistence
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('theme');
      if (saved) return saved === 'dark';
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  // Sync dark class on root html
  useEffect(() => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark]);

  // Chat message input and filter
  const [inputQuery, setInputQuery] = useState('');
  const [dataFilter, setDataFilter] = useState('All Data');
  const [showFilterDropdown, setShowFilterDropdown] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  // Active query selection for instant faster response
  const [activeQueryTitle, setActiveQueryTitle] = useState(
    'What are the top customer complaints about checkout?'
  );

  // Modal states for interactive actions
  const [activeModal, setActiveModal] = useState(null); // 'all_feedback', 'create_feature', 'manage_sources', 'edit_context', 'view_all_questions'
  const [selectedFeatureAction, setSelectedFeatureAction] = useState(null);

  // Pre-cached instant responses for faster response time
  const knowledgeBase = {
    'What are the top customer complaints about checkout?': {
      userTimestamp: '10:24 AM',
      intro: 'Here are the top customer complaints about the checkout process based on 1,248 feedback items from the last 3 months.',
      topIssues: [
        { rank: 1, label: 'Checkout is too slow', pct: 28, count: 352, color: 'bg-rose-500', badgeColor: 'bg-rose-500/20 text-rose-400 border-rose-500/30' },
        { rank: 2, label: 'Multiple payment options needed', pct: 18, count: 224, color: 'bg-blue-500', badgeColor: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
        { rank: 3, label: 'Payment failures', pct: 15, count: 186, color: 'bg-amber-400', badgeColor: 'bg-amber-500/20 text-amber-400 border-amber-500/30' },
        { rank: 4, label: 'Guest checkout option', pct: 12, count: 153, color: 'bg-purple-500', badgeColor: 'bg-purple-500/20 text-purple-400 border-purple-500/30' },
        { rank: 5, label: 'Error messages not clear', pct: 10, count: 124, color: 'bg-emerald-500', badgeColor: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' },
      ],
      sentiment: {
        totalItems: 352,
        negative: 62,
        neutral: 24,
        positive: 14,
      },
      customerFeedback: [
        {
          quote: 'The checkout process is too slow, especially on mobile. I have to try multiple times.',
          source: 'App Store',
          date: 'Jul 28, 2025',
          icon: 'apple',
        },
        {
          quote: 'I wish there were more payment options like Apple Pay and Google Pay.',
          source: 'Play Store',
          date: 'Jul 26, 2025',
          icon: 'play',
        },
        {
          quote: 'The payment keeps failing even though my card is valid.',
          source: 'Support Ticket',
          date: 'Jul 24, 2025',
          icon: 'ticket',
        },
      ],
      insights: [
        'Checkout performance is a major pain point, mentioned in 28% of checkout-related feedback.',
        'Users are requesting more payment methods, especially Apple Pay and Google Pay.',
        'Payment failures and unclear error messages are causing frustration and cart abandonment.',
        'Adding a guest checkout option is also a common request, particularly from new users.',
      ],
      actions: [
        { id: 1, title: 'Improve checkout performance', iconColor: 'bg-purple-600', icon: 'list' },
        { id: 2, title: 'Add multiple payment options', iconColor: 'bg-blue-600', icon: 'card' },
        { id: 3, title: 'Improve error messages', iconColor: 'bg-emerald-600', icon: 'shield' },
        { id: 4, title: 'Add guest checkout option', iconColor: 'bg-amber-600', icon: 'user' },
      ],
    },
    'What features are most requested by users?': {
      userTimestamp: '10:28 AM',
      intro: 'Based on 2,840 customer feature requests, here are the top requested capabilities across all channels.',
      topIssues: [
        { rank: 1, label: 'One-Click Instant Checkout', pct: 34, count: 480, color: 'bg-purple-500', badgeColor: 'bg-purple-500/20 text-purple-400 border-purple-500/30' },
        { rank: 2, label: 'Dark Mode UI Support', pct: 24, count: 340, color: 'bg-blue-500', badgeColor: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
        { rank: 3, label: 'Real-time Order Tracking SMS', pct: 19, count: 270, color: 'bg-emerald-500', badgeColor: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' },
        { rank: 4, label: 'Saved Wishlists & Price Alerts', pct: 14, count: 198, color: 'bg-amber-500', badgeColor: 'bg-amber-500/20 text-amber-400 border-amber-500/30' },
        { rank: 5, label: 'Multi-Currency Wallet', pct: 9, count: 128, color: 'bg-rose-500', badgeColor: 'bg-rose-500/20 text-rose-400 border-rose-500/30' },
      ],
      sentiment: {
        totalItems: 480,
        negative: 18,
        neutral: 32,
        positive: 50,
      },
      customerFeedback: [
        {
          quote: 'Please add 1-click checkout like Amazon so I do not have to retype my address every single time.',
          source: 'Play Store',
          date: 'Aug 02, 2025',
          icon: 'play',
        },
        {
          quote: 'I love shopping at night, a true dark mode would save battery and eyes!',
          source: 'App Store',
          date: 'Jul 30, 2025',
          icon: 'apple',
        },
        {
          quote: 'Price drop notification emails would make me buy much more frequently.',
          source: 'In-App Feedback',
          date: 'Jul 29, 2025',
          icon: 'ticket',
        },
      ],
      insights: [
        'One-click purchasing reduces friction by over 40% based on feedback frequency.',
        'High desire for convenience features: saved payment methods and instant address lookup.',
        'Positive sentiment is high (50%) when users discuss potential roadmap enhancements.',
        'Mobile shoppers represent 74% of wishlist and price alert requests.',
      ],
      actions: [
        { id: 1, title: 'PRD: One-Click Checkout Flow', iconColor: 'bg-purple-600', icon: 'list' },
        { id: 2, title: 'Implement Dark Theme Engine', iconColor: 'bg-blue-600', icon: 'card' },
        { id: 3, title: 'Integrate Twilio SMS Tracking', iconColor: 'bg-emerald-600', icon: 'shield' },
        { id: 4, title: 'Price Drop Alert Pipeline', iconColor: 'bg-amber-600', icon: 'user' },
      ],
    },
    'Show sentiment trend for the last 6 months': {
      userTimestamp: '10:31 AM',
      intro: 'Aggregated sentiment metrics show a steady increase in customer satisfaction from May through October.',
      topIssues: [
        { rank: 1, label: 'Search & Navigation Experience', pct: 38, count: 520, color: 'bg-emerald-500', badgeColor: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' },
        { rank: 2, label: 'Customer Support Response Speed', pct: 26, count: 356, color: 'bg-blue-500', badgeColor: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
        { rank: 3, label: 'Mobile App Crash Frequency', pct: 16, count: 219, color: 'bg-amber-500', badgeColor: 'bg-amber-500/20 text-amber-400 border-amber-500/30' },
        { rank: 4, label: 'Delivery Timeliness', pct: 12, count: 164, color: 'bg-purple-500', badgeColor: 'bg-purple-500/20 text-purple-400 border-purple-500/30' },
        { rank: 5, label: 'Return & Refund Processing', pct: 8, count: 110, color: 'bg-rose-500', badgeColor: 'bg-rose-500/20 text-rose-400 border-rose-500/30' },
      ],
      sentiment: {
        totalItems: 1369,
        negative: 32,
        neutral: 28,
        positive: 40,
      },
      customerFeedback: [
        {
          quote: 'The app has gotten so much smoother after the July performance update.',
          source: 'App Store',
          date: 'Aug 14, 2025',
          icon: 'apple',
        },
        {
          quote: 'Support agent resolved my damaged item claim in under 15 minutes!',
          source: 'Support Ticket',
          date: 'Aug 10, 2025',
          icon: 'ticket',
        },
        {
          quote: 'Still occasionally crashes when scrolling high-res product galleries.',
          source: 'Play Store',
          date: 'Aug 05, 2025',
          icon: 'play',
        },
      ],
      insights: [
        'Positive sentiment climbed from 24% to 40% following v2.4 mobile deployment.',
        'Negative feedback dropped significantly after fixing payment gateway timeouts.',
        'Support tickets resolved within 1 hour have a 92% positive CSAT score.',
        'Image caching in the mobile catalog remains the primary culprit for memory crashes.',
      ],
      actions: [
        { id: 1, title: 'Optimize Product Image Caching', iconColor: 'bg-purple-600', icon: 'list' },
        { id: 2, title: 'Automate Refund Approvals', iconColor: 'bg-blue-600', icon: 'card' },
        { id: 3, title: 'Support Chatbot Escalations', iconColor: 'bg-emerald-600', icon: 'shield' },
        { id: 4, title: 'Delivery Partner SLA Review', iconColor: 'bg-amber-600', icon: 'user' },
      ],
    },
  };

  // Get current active response data
  const currentData = knowledgeBase[activeQueryTitle] || knowledgeBase['What are the top customer complaints about checkout?'];

  // Handle question submit
  const handleAskQuestion = (q) => {
    const trimmed = q.trim();
    if (!trimmed) return;
    setIsGenerating(true);
    setInputQuery('');
    setTimeout(() => {
      if (knowledgeBase[trimmed]) {
        setActiveQueryTitle(trimmed);
      } else {
        knowledgeBase[trimmed] = {
          userTimestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          intro: `Here is the AI synthesis for "${trimmed}" across 1,180 verified data points.`,
          topIssues: [
            { rank: 1, label: `Primary friction point for ${trimmed.slice(0, 24)}...`, pct: 32, count: 378, color: 'bg-rose-500', badgeColor: 'bg-rose-500/20 text-rose-400 border-rose-500/30' },
            { rank: 2, label: 'Secondary user request pattern', pct: 22, count: 260, color: 'bg-blue-500', badgeColor: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
            { rank: 3, label: 'Platform performance & sync delays', pct: 18, count: 212, color: 'bg-amber-400', badgeColor: 'bg-amber-500/20 text-amber-400 border-amber-500/30' },
            { rank: 4, label: 'Documentation & UI clarity', pct: 15, count: 177, color: 'bg-purple-500', badgeColor: 'bg-purple-500/20 text-purple-400 border-purple-500/30' },
            { rank: 5, label: 'Third-party webhook integrations', pct: 13, count: 153, color: 'bg-emerald-500', badgeColor: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' },
          ],
          sentiment: {
            totalItems: 378,
            negative: 54,
            neutral: 28,
            positive: 18,
          },
          customerFeedback: [
            {
              quote: `This aspect requires immediate optimization: "${trimmed}".`,
              source: 'App Store',
              date: 'Just now',
              icon: 'apple',
            },
            {
              quote: 'Would be fantastic if the product team prioritized this in the next sprint.',
              source: 'Play Store',
              date: 'Yesterday',
              icon: 'play',
            },
            {
              quote: 'Reported this friction multiple times through chat support.',
              source: 'Support Ticket',
              date: '2 days ago',
              icon: 'ticket',
            },
          ],
          insights: [
            `Analysis indicates strong customer intent regarding "${trimmed}".`,
            'Cross-referencing with roadmap suggests high PM prioritization urgency.',
            'Directly impacts customer churn and session completion rates.',
            'Recommended to spin off a dedicated PRD for engineering review.',
          ],
          actions: [
            { id: 1, title: `PRD: Resolve ${trimmed.slice(0, 20)}`, iconColor: 'bg-purple-600', icon: 'list' },
            { id: 2, title: 'Add to Sprint Backlog', iconColor: 'bg-blue-600', icon: 'card' },
            { id: 3, title: 'Setup Telemetry Alerts', iconColor: 'bg-emerald-600', icon: 'shield' },
            { id: 4, title: 'Share with PM Team', iconColor: 'bg-amber-600', icon: 'user' },
          ],
        };
        setActiveQueryTitle(trimmed);
      }
      setIsGenerating(false);
    }, 280);
  };

  // List of example questions shown in the right sidebar
  const exampleQuestions = [
    'What are the top customer complaints about checkout?',
    'What features are most requested by users?',
    'Show sentiment trend for the last 6 months',
    'Summarize feedback related to payment issues',
    'What are the key insights from negative feedback?',
    'Compare feedback before and after the latest release',
    'Which features should we prioritize based on customer feedback?',
    'Generate a PRD for one-click checkout based on customer feedback',
    'What are users saying about the mobile app experience?',
  ];

  // List of data sources
  const dataSources = [
    { name: 'App Store Reviews', count: '12.4K items', connected: true, iconBg: 'bg-blue-500/20 text-blue-400' },
    { name: 'Play Store Reviews', count: '8.2K items', connected: true, iconBg: 'bg-amber-500/20 text-amber-400' },
    { name: 'Support Tickets', count: '5.1K items', connected: true, iconBg: 'bg-emerald-500/20 text-emerald-400' },
    { name: 'Surveys', count: '2.3K items', connected: true, iconBg: 'bg-cyan-500/20 text-cyan-400' },
    { name: 'Social Media', count: '3.4K items', connected: true, iconBg: 'bg-indigo-500/20 text-indigo-400' },
    { name: 'In-App Feedback', count: '1.8K items', connected: true, iconBg: 'bg-purple-500/20 text-purple-400' },
  ];

  // SVG Donut calculation
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const negOffset = 0;
  const negStroke = (currentData.sentiment.negative / 100) * circumference;
  const neuStroke = (currentData.sentiment.neutral / 100) * circumference;
  const posStroke = (currentData.sentiment.positive / 100) * circumference;

  return (
    <div
      className={`min-h-screen flex antialiased font-sans transition-colors duration-200 ${
        isDark ? 'dark bg-[#0B0F17] text-slate-100' : 'bg-[#F8FAFC] text-slate-800'
      }`}
    >
      {/* ========================================================
          1. LEFT SIDEBAR
      ======================================================== */}
      <aside
        className="w-64 min-w-[16rem] flex-shrink-0 flex flex-col justify-between border-r border-slate-800/80 dark:border-[#1E293B] bg-[#0E131F] dark:bg-[#0E131F] select-none z-30 min-h-screen"
        data-purpose="sidebar"
      >
        <div>
          {/* Brand Logo Area */}
          <div className="h-16 flex items-center gap-3 px-5 border-b border-slate-800/60 dark:border-[#1E293B]">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 via-indigo-500 to-purple-400 flex items-center justify-center text-white shadow-lg shadow-purple-500/20 flex-shrink-0">
              <svg className="w-5 h-5 fill-none" stroke="currentColor" strokeWidth="2.2" viewBox="0 0 24 24">
                <path
                  d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div>
              <div className="font-bold text-sm tracking-tight text-white flex items-center gap-1.5">ProdIntel AI</div>
              <div className="text-[10px] text-slate-400 tracking-wide font-medium">Product Feedback Intelligence</div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="p-3 space-y-1 font-medium text-xs">
            <button
              onClick={() => onNavigate && onNavigate('PM Dashboard')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <rect height="7" rx="1.5" width="7" x="3" y="3" />
                <rect height="7" rx="1.5" width="7" x="14" y="3" />
                <rect height="7" rx="1.5" width="7" x="14" y="14" />
                <rect height="7" rx="1.5" width="7" x="3" y="14" />
              </svg>
              <span>Dashboard</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('Insights')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="9" />
                <path d="M12 3v3m0 12v3m9-9h-3M6 12H3m15.364-6.364l-2.121 2.121M8.757 15.243l-2.121 2.121m12.728 0l-2.121-2.121M8.757 8.757L6.636 6.636" />
              </svg>
              <span>Insights</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('Feedback')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              <span>Feedback</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('Features')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <path d="M16.5 9.4 7.55 4.24a1.78 1.78 0 0 0-2.5 1.55v12.42a1.78 1.78 0 0 0 2.5 1.55L16.5 14.6a1.78 1.78 0 0 0 0-3.2z" />
              </svg>
              <span>Features</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('Prioritization')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
              </svg>
              <span>Prioritization</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('Requirements')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" x2="8" y1="13" y2="13" />
                <line x1="16" x2="8" y1="17" y2="17" />
              </svg>
              <span>Requirements (PRDs)</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('Roadmap')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <line x1="3" x2="21" y1="6" y2="6" />
                <line x1="3" x2="21" y1="12" y2="12" />
                <line x1="3" x2="21" y1="18" y2="18" />
                <circle cx="9" cy="6" r="2" />
                <circle cx="15" cy="12" r="2" />
                <circle cx="8" cy="18" r="2" />
              </svg>
              <span>Roadmap</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('Reports')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <path d="M18 20V10M12 20V4M6 20v-6" />
              </svg>
              <span>Reports</span>
            </button>

            {/* Active AI Assistant Menu Link */}
            <button
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-white bg-purple-600 shadow-md shadow-purple-900/40 font-semibold text-left transition-all"
            >
              <svg className="w-4 h-4 text-purple-200" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83" />
              </svg>
              <span>AI Assistant</span>
            </button>
          </nav>
        </div>

        {/* Bottom Workspace Usage & User Block */}
        <div className="p-3 border-t border-slate-800/70 dark:border-[#1E293B]">
          {/* Current Workspace Widget */}
          <div
            onClick={() => onNavigate && onNavigate('Workspaces')}
            className="mb-4 bg-[#121927] dark:bg-[#131B2A] p-3 rounded-xl border border-slate-800/80 dark:border-[#1F2B3E] cursor-pointer hover:border-slate-700 transition"
          >
            <div className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider">Current Workspace</div>
            <div className="mt-1 flex items-center justify-between text-xs font-semibold text-slate-200">
              <span>E-Commerce Platform</span>
              <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
            </div>
            <div className="text-[11px] text-slate-400 mt-0.5">12 Members</div>

            {/* Storage Usage Bar */}
            <div className="mt-3">
              <div className="flex justify-between items-center text-[10px] text-slate-400 font-medium mb-1">
                <span>Workspace Usage</span>
                <span className="text-purple-400 font-semibold">78%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div className="bg-gradient-to-r from-purple-500 to-indigo-500 h-1.5 rounded-full" style={{ width: '78%' }}></div>
              </div>
              <div className="text-[10px] text-slate-400 mt-1">7.8 GB / 10 GB</div>
            </div>
          </div>

          {/* User Profile Monogram */}
          <div className="flex items-center justify-between pt-1">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-violet-600 to-indigo-500 flex items-center justify-center text-white font-semibold text-xs ring-2 ring-indigo-400/20">
                PS
              </div>
              <div className="overflow-hidden leading-tight">
                <div className="text-xs font-semibold truncate text-slate-200">Priya Sharma</div>
                <div className="text-[10px] text-slate-400 truncate">Product Manager</div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* ========================================================
          2. MAIN CONTENT AREA + RIGHT SIDEBAR
      ======================================================== */}
      <div className="flex-1 flex flex-col min-w-0 bg-[#0B0F17] dark:bg-[#0B0F17]">
        {/* Top Header */}
        <header
          className="h-16 px-6 border-b border-slate-800/70 dark:border-[#1E293B] flex items-center justify-between sticky top-0 z-20 bg-[#0B0F17]/90 dark:bg-[#0B0F17]/90 backdrop-blur-md transition-colors"
          data-purpose="top-navigation"
        >
          {/* Left: Breadcrumb / Assistant Title & Beta tag */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2L9.5 8.5L3 11L9.5 13.5L12 20L14.5 13.5L21 11L14.5 8.5L12 2Z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
                </svg>
              </div>
              <div className="font-bold text-base text-slate-100 flex items-center gap-2">
                <span>AI Assistant</span>
                <span className="px-2 py-0.5 text-[10px] font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/30 rounded-full tracking-wide">
                  BETA
                </span>
              </div>
            </div>
            <div className="h-4 w-px bg-slate-800 hidden md:block"></div>
            <span className="text-xs text-slate-400 hidden md:inline">
              Ask questions about your customer feedback, product insights, features, PRDs, or roadmap.
            </span>
          </div>

          {/* Right Header Utilities & Consistent Toggle */}
          <div className="flex items-center gap-3">
            <div className="hidden lg:flex items-center gap-1.5 text-xs text-purple-400 bg-purple-950/30 border border-purple-800/40 px-3 py-1 rounded-full">
              <svg className="w-3.5 h-3.5 text-purple-400 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              <span className="font-medium text-[11px]">Powered by Semantic AI</span>
            </div>

            <button
              onClick={() => onNavigate && onNavigate('Workspaces')}
              className="flex items-center gap-2 px-3 py-1.5 text-xs rounded-lg bg-[#111726] border border-slate-800 text-slate-300 hover:bg-slate-800/80 transition-colors"
              type="button"
            >
              <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
              </svg>
              <span className="font-medium">E-Commerce Platform</span>
              <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
            </button>

            <button
              aria-label="Search"
              onClick={() => {
                const q = prompt('Search customer intelligence:');
                if (q) handleAskQuestion(q);
              }}
              className="p-2 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800/50 transition"
              type="button"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>
            </button>

            {/* Notification Bell */}
            <div className="relative">
              <button
                aria-label="Notifications"
                className="p-2 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800/50 transition"
                type="button"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                  <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
                  <path d="M13.73 21a2 2 0 0 1-3.46 0" />
                </svg>
              </button>
              <span className="absolute top-1 right-1 w-4 h-4 bg-rose-500 text-white rounded-full text-[9px] font-bold flex items-center justify-center shadow-sm">
                3
              </span>
            </div>

            {/* Help / Docs */}
            <button
              aria-label="Help"
              onClick={() => alert('AI Assistant: Ask natural language questions against all parsed feedback, reviews, and survey datasets with sub-second retrieval.')}
              className="p-2 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800/50 transition"
              type="button"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" />
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
                <path d="M12 17h.01" />
              </svg>
            </button>

            {/* CONSISTENT THEME TOGGLE (Sliding Pill with Sun & Moon Icons) */}
            <div className="border-l border-slate-800 pl-3">
              <button
                type="button"
                aria-label="Toggle Light and Dark Mode"
                onClick={() => setIsDark(!isDark)}
                className={`relative inline-flex items-center h-6 w-11 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900 ${
                  isDark ? 'bg-purple-600' : 'bg-slate-200'
                }`}
              >
                <span
                  className={`inline-block w-4 h-4 transform rounded-full bg-white transition duration-200 ease-in-out shadow flex items-center justify-center ${
                    isDark ? 'translate-x-6' : 'translate-x-1'
                  }`}
                >
                  {isDark ? (
                    <svg className="w-2.5 h-2.5 text-purple-700" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                    </svg>
                  ) : (
                    <svg className="w-2.5 h-2.5 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        clipRule="evenodd"
                        fillRule="evenodd"
                        d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                      />
                    </svg>
                  )}
                </span>
              </button>
            </div>

            {/* User Profile Pill */}
            <div className="flex items-center gap-2 pl-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-violet-600 to-indigo-500 flex items-center justify-center text-white font-semibold text-xs ring-2 ring-indigo-400/20">
                PS
              </div>
              <div className="hidden xl:block text-left text-xs leading-none">
                <div className="font-semibold text-slate-200">Priya Sharma</div>
                <div className="text-[10px] text-slate-400 mt-0.5">Product Manager</div>
              </div>
            </div>
          </div>
        </header>

        {/* Content Body: Chat Conversation + Right Sidebar */}
        <div className="flex-1 flex overflow-hidden">
          {/* 2A. Chat & Intelligence Canvas */}
          <div className="flex-1 flex flex-col overflow-y-auto px-6 py-6 space-y-6">
            
            {/* User Query Bubble (Right-aligned) */}
            <div className="flex justify-end items-start gap-3">
              <div className="flex flex-col items-end">
                <div className="bg-[#244796] hover:bg-[#203f84] text-white px-5 py-3 rounded-2xl rounded-tr-sm text-sm font-medium shadow-lg max-w-xl transition-all">
                  {activeQueryTitle}
                </div>
                <span className="text-[11px] text-slate-500 mt-1 font-mono">{currentData.userTimestamp}</span>
              </div>
              <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold text-xs shadow-md">
                PS
              </div>
            </div>

            {/* AI Assistant Response Bubble (Left-aligned) */}
            <div className="flex items-start gap-3">
              {/* Bot Avatar Icon */}
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-purple-500/20 flex-shrink-0 mt-0.5">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
                </svg>
              </div>

              {/* Bot Response Content Card */}
              <div className="flex-1 space-y-5">
                {/* Intro summary sentence */}
                <p className="text-sm text-slate-300 font-medium">
                  {isGenerating ? (
                    <span className="inline-flex items-center gap-2 text-purple-400">
                      <svg className="animate-spin h-4 w-4 text-purple-400" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                      </svg>
                      Synthesizing intelligence in real-time...
                    </span>
                  ) : (
                    currentData.intro
                  )}
                </p>

                {/* Grid: Top Issues & Sentiment Distribution */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  {/* Card 1: Top Issues in Checkout */}
                  <div className="bg-[#111726] border border-slate-800/90 rounded-xl p-5 shadow-sm">
                    <h3 className="text-sm font-semibold text-slate-200 mb-4 tracking-tight">Top Issues in Checkout</h3>
                    
                    <div className="space-y-3.5">
                      {currentData.topIssues.map((issue) => (
                        <div key={issue.rank} className="flex items-center gap-3">
                          {/* Number badge */}
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${issue.badgeColor} border`}>
                            {issue.rank}
                          </div>
                          
                          {/* Title */}
                          <div className="w-52 text-xs font-medium text-slate-300 truncate">
                            {issue.label}
                          </div>

                          {/* Progress bar */}
                          <div className="flex-1 bg-slate-800/80 rounded-full h-2 overflow-hidden">
                            <div
                              className={`${issue.color} h-2 rounded-full transition-all duration-500`}
                              style={{ width: `${issue.pct * 2.5}%` }}
                            ></div>
                          </div>

                          {/* Stat label */}
                          <div className="w-20 text-right text-xs font-semibold text-slate-400 font-mono">
                            {issue.pct}% <span className="text-slate-500 font-normal">({issue.count})</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Card 2: Sentiment Distribution */}
                  <div className="bg-[#111726] border border-slate-800/90 rounded-xl p-5 shadow-sm flex flex-col justify-between">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-semibold text-slate-200 tracking-tight">Sentiment Distribution</h3>
                      <button
                        onClick={() => setActiveModal('all_feedback')}
                        className="text-xs text-purple-400 hover:text-purple-300 font-medium flex items-center gap-1 transition"
                      >
                        <span>View All Feedback</span>
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                        </svg>
                      </button>
                    </div>

                    <div className="flex items-center justify-center gap-8 py-2">
                      {/* SVG Donut Chart */}
                      <div className="relative w-36 h-36 flex items-center justify-center">
                        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 140 140">
                          {/* Base circle background */}
                          <circle
                            cx="70"
                            cy="70"
                            r={radius}
                            fill="transparent"
                            stroke="#1E293B"
                            strokeWidth="18"
                          />
                          {/* Negative segment (Red) */}
                          <circle
                            cx="70"
                            cy="70"
                            r={radius}
                            fill="transparent"
                            stroke="#EF4444"
                            strokeWidth="18"
                            strokeDasharray={`${negStroke} ${circumference}`}
                            strokeDashoffset={negOffset}
                            strokeLinecap="round"
                          />
                          {/* Neutral segment (Blue/Slate) */}
                          <circle
                            cx="70"
                            cy="70"
                            r={radius}
                            fill="transparent"
                            stroke="#64748B"
                            strokeWidth="18"
                            strokeDasharray={`${neuStroke} ${circumference}`}
                            strokeDashoffset={-(negStroke)}
                            strokeLinecap="round"
                          />
                          {/* Positive segment (Green) */}
                          <circle
                            cx="70"
                            cy="70"
                            r={radius}
                            fill="transparent"
                            stroke="#10B981"
                            strokeWidth="18"
                            strokeDasharray={`${posStroke} ${circumference}`}
                            strokeDashoffset={-(negStroke + neuStroke)}
                            strokeLinecap="round"
                          />
                        </svg>
                        
                        {/* Center Text */}
                        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                          <span className="text-xl font-bold text-white tracking-tight">{currentData.sentiment.totalItems}</span>
                          <span className="text-[10px] text-slate-400 uppercase tracking-wider font-medium">Feedback<br/>Items</span>
                        </div>
                      </div>

                      {/* Legend */}
                      <div className="space-y-3 text-xs">
                        <div className="flex items-center gap-2">
                          <span className="w-3 h-3 rounded-sm bg-rose-500"></span>
                          <span className="text-slate-300 w-16">Negative</span>
                          <span className="font-semibold text-slate-200 font-mono">{currentData.sentiment.negative}%</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="w-3 h-3 rounded-sm bg-slate-500"></span>
                          <span className="text-slate-300 w-16">Neutral</span>
                          <span className="font-semibold text-slate-200 font-mono">{currentData.sentiment.neutral}%</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="w-3 h-3 rounded-sm bg-emerald-500"></span>
                          <span className="text-slate-300 w-16">Positive</span>
                          <span className="font-semibold text-slate-200 font-mono">{currentData.sentiment.positive}%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Example Customer Feedback Section */}
                <div className="space-y-3 pt-1">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center text-[10px]">
                        ✦
                      </div>
                      <h4 className="text-xs font-semibold text-slate-200">Example Customer Feedback</h4>
                    </div>
                    <button
                      onClick={() => setActiveModal('all_feedback')}
                      className="text-xs text-purple-400 hover:text-purple-300 font-medium flex items-center gap-1 transition"
                    >
                      <span>View All</span>
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                      </svg>
                    </button>
                  </div>

                  {/* 3 Feedback Quotes Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {currentData.customerFeedback.map((fb, idx) => (
                      <div
                        key={idx}
                        className="bg-[#111726] border border-slate-800/80 rounded-xl p-4 flex flex-col justify-between hover:border-slate-700 transition"
                      >
                        <div className="space-y-2">
                          <span className="text-rose-400 font-serif text-2xl leading-none">“</span>
                          <p className="text-xs text-slate-300 leading-relaxed font-normal">
                            {fb.quote}
                          </p>
                        </div>
                        <div className="mt-4 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
                          <span className="flex items-center gap-1.5 font-medium">
                            {fb.icon === 'apple' && <span></span>}
                            {fb.icon === 'play' && <span>▶</span>}
                            {fb.icon === 'ticket' && <span>✉</span>}
                            <span>{fb.source}</span>
                          </span>
                          <span className="text-slate-500 font-mono text-[10px]">{fb.date}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Insights Card */}
                <div className="space-y-2.5">
                  <div className="flex items-center gap-2">
                    <span className="text-amber-400 text-sm">💡</span>
                    <h4 className="text-xs font-semibold text-slate-200">AI Insights</h4>
                  </div>
                  <div className="bg-[#111726] border border-slate-800 rounded-xl p-4.5 space-y-2 text-xs text-slate-300">
                    {currentData.insights.map((insight, idx) => (
                      <div key={idx} className="flex items-start gap-2.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-purple-400 mt-1.5 flex-shrink-0"></span>
                        <p className="leading-relaxed">
                          {insight}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Recommended Actions */}
                <div className="space-y-2.5">
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-md bg-blue-500/20 text-blue-400 flex items-center justify-center text-[10px]">
                      👥
                    </div>
                    <h4 className="text-xs font-semibold text-slate-200">Recommended Actions</h4>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3">
                    {currentData.actions.map((act) => (
                      <button
                        key={act.id}
                        onClick={() => {
                          setSelectedFeatureAction(act.title);
                          setActiveModal('create_feature');
                        }}
                        className="bg-[#111726] hover:bg-[#151D30] border border-slate-800/90 hover:border-purple-500/40 rounded-xl p-3 flex items-center justify-between text-left transition group shadow-xs"
                      >
                        <div className="flex items-center gap-2.5 overflow-hidden">
                          <div className={`w-7 h-7 rounded-lg ${act.iconColor} flex items-center justify-center text-white flex-shrink-0 text-xs shadow-sm`}>
                            {act.icon === 'list' && <span>☰</span>}
                            {act.icon === 'card' && <span>💳</span>}
                            {act.icon === 'shield' && <span>🛡️</span>}
                            {act.icon === 'user' && <span>👤</span>}
                          </div>
                          <div className="overflow-hidden">
                            <div className="text-[10px] text-slate-400 font-medium">Create Feature</div>
                            <div className="text-xs font-semibold text-slate-200 truncate group-hover:text-purple-300 transition">
                              {act.title}
                            </div>
                          </div>
                        </div>
                        <svg className="w-4 h-4 text-slate-500 group-hover:text-purple-400 transition transform group-hover:translate-x-0.5 flex-shrink-0 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                        </svg>
                      </button>
                    ))}
                  </div>
                </div>

              </div>
            </div>

            {/* Chat Input Bar (Sticky at bottom of chat column) */}
            <div className="sticky bottom-0 pt-3 pb-1 bg-[#0B0F17]/95 backdrop-blur-md">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleAskQuestion(inputQuery);
                }}
                className="bg-[#111726] border border-slate-800 focus-within:border-purple-500/80 rounded-2xl px-4 py-2.5 flex items-center gap-3 shadow-xl transition"
              >
                {/* Attachment Icon */}
                <button
                  type="button"
                  onClick={() => alert('Attach feedback file (.csv, .json, or screenshot) to analyze with Semantic AI.')}
                  className="text-slate-400 hover:text-slate-200 p-1 rounded-lg transition"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" />
                  </svg>
                </button>

                {/* Input Text Box */}
                <input
                  type="text"
                  value={inputQuery}
                  onChange={(e) => setInputQuery(e.target.value)}
                  placeholder="Ask anything about your product data..."
                  className="flex-1 bg-transparent border-0 outline-none text-xs text-slate-200 placeholder-slate-500"
                />

                {/* Dropdown Filter Pill */}
                <div className="relative">
                  <button
                    type="button"
                    onClick={() => setShowFilterDropdown(!showFilterDropdown)}
                    className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#161E31] text-[11px] font-medium text-slate-300 border border-slate-700/60 hover:border-slate-600 transition"
                  >
                    <span>{dataFilter}</span>
                    <svg className="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                    </svg>
                  </button>

                  {showFilterDropdown && (
                    <div className="absolute right-0 bottom-full mb-2 w-40 bg-[#161F33] border border-slate-700 rounded-xl shadow-2xl py-1 z-30 text-xs">
                      {['All Data', 'App Store Only', 'Play Store Only', 'Support Tickets', 'Surveys'].map((opt) => (
                        <button
                          key={opt}
                          type="button"
                          onClick={() => {
                            setDataFilter(opt);
                            setShowFilterDropdown(false);
                          }}
                          className="w-full text-left px-3 py-1.5 hover:bg-purple-600 hover:text-white text-slate-300 transition"
                        >
                          {opt}
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                {/* Send Button */}
                <button
                  type="submit"
                  disabled={!inputQuery.trim() && !isGenerating}
                  className="w-8 h-8 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white flex items-center justify-center transition shadow-md shadow-purple-600/30 flex-shrink-0"
                >
                  <svg className="w-4 h-4 transform rotate-45 -translate-y-0.5 -translate-x-0.5" fill="none" stroke="currentColor" strokeWidth="2.2" viewBox="0 0 24 24">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                  </svg>
                </button>
              </form>
            </div>

          </div>

          {/* ========================================================
              2B. RIGHT SIDEBAR (Example Questions, Sources, Context)
          ======================================================== */}
          <aside className="w-80 border-l border-slate-800/80 bg-[#0E131F] flex flex-col justify-between overflow-y-auto p-4 space-y-6 select-none hidden lg:flex">
            
            {/* 1. Example Questions */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-slate-400 text-xs">📋</span>
                  <h4 className="text-xs font-semibold text-slate-200">Example Questions</h4>
                </div>
                <button
                  onClick={() => setActiveModal('view_all_questions')}
                  className="text-[11px] text-purple-400 hover:text-purple-300 font-medium flex items-center gap-0.5"
                >
                  <span>View All</span>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                  </svg>
                </button>
              </div>

              {/* Questions list */}
              <div className="space-y-2">
                {exampleQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleAskQuestion(q)}
                    className="w-full text-left p-2.5 rounded-xl bg-[#121827] hover:bg-[#162035] border border-slate-800/80 hover:border-purple-500/30 flex items-center justify-between text-xs text-slate-300 hover:text-purple-300 transition group"
                  >
                    <span className="line-clamp-2 pr-2 leading-snug">{q}</span>
                    <svg className="w-3.5 h-3.5 text-slate-500 group-hover:text-purple-400 transition transform group-hover:translate-x-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                    </svg>
                  </button>
                ))}
              </div>
            </div>

            {/* 2. Data Sources */}
            <div className="space-y-3 pt-2 border-t border-slate-800/80">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-semibold text-slate-200">Data Sources</h4>
                <button
                  onClick={() => setActiveModal('manage_sources')}
                  className="text-[11px] text-purple-400 hover:text-purple-300 font-medium"
                >
                  Manage
                </button>
              </div>

              <div className="space-y-2">
                {dataSources.map((ds, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between text-xs p-2 rounded-lg bg-[#121827]/70 border border-slate-800/60"
                  >
                    <div className="flex items-center gap-2.5 overflow-hidden">
                      <div className={`w-5 h-5 rounded-md ${ds.iconBg} flex items-center justify-center text-[10px] font-bold flex-shrink-0`}>
                        {ds.name.charAt(0)}
                      </div>
                      <span className="text-slate-300 truncate font-medium">{ds.name}</span>
                    </div>

                    <div className="flex items-center gap-2.5 flex-shrink-0">
                      <span className="text-[11px] text-slate-500 font-mono">{ds.count}</span>
                      <span className="text-[10px] text-emerald-400 font-medium flex items-center gap-1">
                        <svg className="w-3 h-3 text-emerald-400" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                          <path d="M5 13l4 4L19 7" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        Connected
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 3. Current Context */}
            <div className="space-y-3 pt-2 border-t border-slate-800/80">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-semibold text-slate-200">Current Context</h4>
                <button
                  onClick={() => setActiveModal('edit_context')}
                  className="text-[11px] text-purple-400 hover:text-purple-300 font-medium"
                >
                  Edit
                </button>
              </div>

              <div className="bg-[#121827] border border-slate-800/80 rounded-xl p-3 space-y-2.5 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-slate-500 flex items-center gap-1.5">
                    <span>🏢</span> Workspace
                  </span>
                  <span className="font-semibold text-slate-200">E-Commerce Platform</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-500 flex items-center gap-1.5">
                    <span>📅</span> Time Range
                  </span>
                  <span className="font-medium text-slate-300">Last 3 months</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-500 flex items-center gap-1.5">
                    <span>📊</span> Data Type
                  </span>
                  <span className="font-medium text-slate-300">All feedback data</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-500 flex items-center gap-1.5">
                    <span>👤</span> User Role
                  </span>
                  <span className="font-medium text-purple-400 font-mono">Product Manager</span>
                </div>
              </div>
            </div>

          </aside>
        </div>
      </div>

      {/* ========================================================
          3. INTERACTIVE MODALS
      ======================================================== */}
      {/* Modal: All Customer Feedback */}
      {activeModal === 'all_feedback' && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#111726] border border-slate-800 rounded-2xl w-full max-w-2xl max-h-[80vh] flex flex-col shadow-2xl">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-white">All Customer Feedback Items</h3>
                <p className="text-xs text-slate-400">Total 352 checkout feedback entries analyzed</p>
              </div>
              <button
                onClick={() => setActiveModal(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg"
              >
                ✕
              </button>
            </div>
            <div className="p-4 overflow-y-auto space-y-3">
              {[
                { source: 'App Store', text: 'Checkout is taking forever to process Apple Pay. Error 402 keeps showing up.', author: 'User #9281', rating: '1/5' },
                { source: 'Play Store', text: 'Cannot add a secondary card. Please give PayPal or Klarna support.', author: 'User #4812', rating: '2/5' },
                { source: 'Support Ticket', text: 'Payment gateway timed out after I entered OTP. Deducted amount but no order receipt.', author: 'User #7729', rating: '1/5' },
                { source: 'In-App Survey', text: 'Guest checkout would be so much faster than creating an account.', author: 'User #1938', rating: '3/5' },
                { source: 'App Store', text: 'Error messages just say "An error occurred". Be specific!', author: 'User #8841', rating: '2/5' },
              ].map((item, i) => (
                <div key={i} className="p-3 rounded-xl bg-[#0E131F] border border-slate-800/80 space-y-1">
                  <div className="flex items-center justify-between text-[11px] text-slate-400">
                    <span className="font-semibold text-purple-400">{item.source} • {item.author}</span>
                    <span className="text-rose-400 font-bold">{item.rating}</span>
                  </div>
                  <p className="text-xs text-slate-200">{item.text}</p>
                </div>
              ))}
            </div>
            <div className="p-4 border-t border-slate-800 flex justify-end">
              <button
                onClick={() => setActiveModal(null)}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-semibold"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Create Feature Action */}
      {activeModal === 'create_feature' && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#111726] border border-slate-800 rounded-2xl w-full max-w-lg p-5 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Create Feature in Roadmap</h3>
              <button onClick={() => setActiveModal(null)} className="text-slate-400 hover:text-white">✕</button>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <label className="text-slate-400 block mb-1">Feature Title</label>
                <input
                  type="text"
                  defaultValue={selectedFeatureAction}
                  className="w-full bg-[#0E131F] border border-slate-700 rounded-lg p-2.5 text-white text-xs outline-none focus:border-purple-500"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Assigned PM</label>
                <input
                  type="text"
                  readOnly
                  value="Priya Sharma (Product Manager)"
                  className="w-full bg-[#0E131F] border border-slate-800 rounded-lg p-2.5 text-slate-400 text-xs"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Linked AI Evidence</label>
                <p className="text-[11px] text-slate-400 bg-[#0E131F] p-2.5 rounded-lg border border-slate-800">
                  Linked to 352 checkout feedback items with 62% negative sentiment. Target sprint: Q4 Sprint 3.
                </p>
              </div>
            </div>
            <div className="pt-2 flex justify-end gap-2 text-xs">
              <button
                onClick={() => setActiveModal(null)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  alert(`Feature "${selectedFeatureAction}" added to Roadmap & PRD draft created!`);
                  setActiveModal(null);
                  if (onNavigate) onNavigate('Roadmap');
                }}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg font-semibold"
              >
                Create Feature & View Roadmap
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Manage Sources */}
      {activeModal === 'manage_sources' && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#111726] border border-slate-800 rounded-2xl w-full max-w-md p-5 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Manage Data Sources</h3>
              <button onClick={() => setActiveModal(null)} className="text-slate-400 hover:text-white">✕</button>
            </div>
            <p className="text-xs text-slate-400">All 6 connectors are actively synchronizing in real time.</p>
            <div className="space-y-2 text-xs">
              {dataSources.map((ds, i) => (
                <div key={i} className="flex items-center justify-between p-2 rounded-lg bg-[#0E131F]">
                  <span className="text-slate-200">{ds.name}</span>
                  <span className="text-emerald-400 font-mono text-[11px]">Synced 2m ago</span>
                </div>
              ))}
            </div>
            <div className="pt-2 flex justify-end">
              <button onClick={() => setActiveModal(null)} className="px-4 py-2 bg-purple-600 text-white rounded-lg text-xs font-semibold">
                Done
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: View All Questions */}
      {activeModal === 'view_all_questions' && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#111726] border border-slate-800 rounded-2xl w-full max-w-lg max-h-[75vh] flex flex-col shadow-2xl">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <h3 className="text-sm font-bold text-white">All Suggested Inquiries</h3>
              <button onClick={() => setActiveModal(null)} className="text-slate-400 hover:text-white">✕</button>
            </div>
            <div className="p-4 overflow-y-auto space-y-2">
              {exampleQuestions.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setActiveModal(null);
                    handleAskQuestion(q);
                  }}
                  className="w-full text-left p-3 rounded-xl bg-[#0E131F] hover:bg-[#162035] border border-slate-800 text-xs text-slate-200 hover:text-purple-300 transition"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
