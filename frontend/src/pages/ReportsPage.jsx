import React, { useState, useEffect } from 'react';

export default function ReportsPage({ onNavigate }) {
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

  // Active Tab Filter
  const [activeTab, setActiveTab] = useState('Overview');
  const [selectedRange, setSelectedRange] = useState('May 13 – May 20, 2025');
  const [trendGranularity, setTrendGranularity] = useState('Daily');

  // Modals & Dropdown states
  const [showExportModal, setShowExportModal] = useState(false);
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [showDateDropdown, setShowDateDropdown] = useState(false);
  const [hoveredPoint, setHoveredPoint] = useState(null);

  // Filters
  const [filterPriority, setFilterPriority] = useState('All');
  const [filterCategory, setFilterCategory] = useState('All');

  // Trend data points for the dual chart
  const trendData = [
    { date: 'May 13', total: 145, resolved: 70 },
    { date: 'May 14', total: 230, resolved: 110 },
    { date: 'May 15', total: 310, resolved: 175 },
    { date: 'May 16', total: 440, resolved: 235 },
    { date: 'May 17', total: 580, resolved: 320 },
    { date: 'May 18', total: 720, resolved: 410 },
    { date: 'May 19', total: 980, resolved: 530 },
    { date: 'May 20', total: 1248, resolved: 642 },
  ];

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
              <div className="text-[10px] text-slate-400 tracking-wide font-medium">Product Intelligence Platform</div>
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
              <span>PM Dashboard</span>
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

            {/* Active Reports Menu Link */}
            <button
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-white bg-purple-700/80 shadow-md shadow-purple-900/30 font-semibold text-left transition-all"
            >
              <svg className="w-4 h-4 text-purple-200" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M18 20V10M12 20V4M6 20v-6" />
              </svg>
              <span>Reports</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('AI Assistant')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83" />
              </svg>
              <span>AI Assistant</span>
            </button>

            <button
              onClick={() => onNavigate && onNavigate('Workspaces')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
              <span>Workspace Members</span>
            </button>

            <button
              onClick={() => alert('Settings')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-colors text-left"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="3" />
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
              </svg>
              <span>Settings</span>
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
            <button
              aria-label="Collapse sidebar"
              onClick={() => alert('Toggle sidebar view')}
              className="text-slate-400 hover:text-slate-200 p-1 rounded-md"
              type="button"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
              </svg>
            </button>
          </div>
        </div>
      </aside>

      {/* ========================================================
          2. MAIN CONTENT AREA
      ======================================================== */}
      <div className="flex-1 flex flex-col min-w-0 bg-[#0B0F17] dark:bg-[#0B0F17]">
        {/* Top Header */}
        <header
          className="h-16 px-6 border-b border-slate-800/70 dark:border-[#1E293B] flex items-center justify-between sticky top-0 z-20 bg-[#0B0F17]/90 dark:bg-[#0B0F17]/90 backdrop-blur-md transition-colors"
          data-purpose="top-navigation"
        >
          {/* Left: Breadcrumbs & Workspace */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
              <span className="hover:underline cursor-pointer">Reports</span>
              <svg className="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
              <span className="text-slate-200 font-semibold">Overview</span>
            </div>
            <div className="h-4 w-px bg-slate-800 hidden sm:block"></div>
            <button
              onClick={() => onNavigate && onNavigate('Workspaces')}
              className="hidden sm:flex items-center gap-2 px-2.5 py-1 text-xs rounded-md bg-slate-900/80 border border-slate-800 text-slate-300 hover:bg-slate-800/80 transition-colors"
              type="button"
            >
              <span className="text-slate-400 font-normal">Workspace:</span>
              <span className="font-medium">E-Commerce Platform</span>
              <svg className="w-3.5 h-3.5 text-slate-400 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
            </button>
          </div>

          {/* Right Header Utilities & Consistent Toggle */}
          <div className="flex items-center gap-3">
            <button
              aria-label="Search"
              onClick={() => {
                const q = prompt('Search reports by metric, category, or date:');
                if (q) alert(`Searching for: ${q}`);
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
              onClick={() => alert('Reports Overview: Aggregated analytics across resolution rates, feedback priorities, and roadmap sprints.')}
              className="p-2 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800/50 transition"
              type="button"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" />
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
                <path d="M12 17h.01" />
              </svg>
            </button>

            {/* CONSISTENT TOGGLE BUTTON (Sliding Pill with Sun & Moon Icons) */}
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
            <div className="h-7 w-px bg-slate-800 mx-1"></div>
            <div className="flex items-center gap-2 pl-1 cursor-pointer">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-500 to-indigo-500 p-0.5 flex items-center justify-center">
                <div className="w-full h-full rounded-full bg-[#182030] flex items-center justify-center text-purple-400 font-bold text-xs">
                  PS
                </div>
              </div>
              <div className="hidden xl:block text-left leading-tight">
                <div className="text-xs font-semibold text-slate-200">Priya Sharma</div>
                <div className="text-[10px] text-slate-400">Product Manager</div>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 p-6 space-y-6 max-w-[1600px] w-full mx-auto">
          {/* Page Heading & Filters Bar */}
          <section className="space-y-4" data-purpose="page-title-and-filters">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-white">Reports Overview</h1>
                <p className="text-xs text-slate-400 mt-1">
                  Comprehensive insights across feedback, prioritization, PRDs, roadmap and resolution.
                </p>
              </div>

              {/* Date Selector & Export Actions */}
              <div className="flex items-center gap-2.5 self-start md:self-auto relative">
                {/* Date range selector button */}
                <button
                  onClick={() => setShowDateDropdown(!showDateDropdown)}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#141C2B] border border-slate-800 dark:border-[#223047] text-xs font-medium text-slate-200 shadow-sm hover:border-slate-700 transition"
                  type="button"
                >
                  <svg className="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <rect height="18" rx="2" ry="2" width="18" x="3" y="4" />
                    <line x1="16" x2="16" y1="2" y2="6" />
                    <line x1="8" x2="8" y1="2" y2="6" />
                    <line x1="3" x2="21" y1="10" y2="10" />
                  </svg>
                  <span>{selectedRange}</span>
                  <svg className="w-3.5 h-3.5 text-slate-400 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                  </svg>
                </button>

                {/* Date Dropdown Menu */}
                {showDateDropdown && (
                  <div className="absolute top-10 left-0 z-40 w-52 bg-[#121929] border border-slate-800 rounded-xl shadow-xl p-2 text-xs space-y-1">
                    {['May 13 – May 20, 2025', 'Last 7 Days', 'Last 30 Days', 'This Month', 'Q2 2025'].map((range) => (
                      <button
                        key={range}
                        onClick={() => {
                          setSelectedRange(range);
                          setShowDateDropdown(false);
                        }}
                        className={`w-full text-left px-3 py-1.5 rounded-lg transition ${
                          selectedRange === range ? 'bg-purple-600 text-white font-medium' : 'text-slate-300 hover:bg-slate-800'
                        }`}
                      >
                        {range}
                      </button>
                    ))}
                  </div>
                )}

                {/* Export Button */}
                <button
                  onClick={() => setShowExportModal(true)}
                  className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-medium text-xs shadow-md shadow-purple-600/20 transition-colors"
                  type="button"
                >
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" x2="12" y1="15" y2="3" />
                  </svg>
                  <span>Export</span>
                  <svg className="w-3 h-3 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Tab Pills & Filter Button */}
            <div className="flex items-center justify-between border-b border-slate-800/80 dark:border-[#1F293D] pb-2">
              <div className="flex items-center gap-2 overflow-x-auto">
                {['Overview', 'Feedback', 'PRDs', 'Roadmap', 'Resolution', 'Team Performance'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                      activeTab === tab
                        ? 'bg-[#1D2638] text-white border border-purple-500/40 shadow-xs'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>

              {/* Filters button */}
              <button
                onClick={() => setShowFilterModal(true)}
                className="flex items-center gap-1.5 text-xs font-medium text-slate-300 bg-[#141C2B] px-3 py-1.5 rounded-lg border border-slate-800 dark:border-[#223047] shadow-sm hover:border-slate-700 transition"
                type="button"
              >
                <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                  <line x1="4" x2="4" y1="21" y2="14" />
                  <line x1="4" x2="4" y1="10" y2="3" />
                  <line x1="12" x2="12" y1="21" y2="12" />
                  <line x1="12" x2="12" y1="8" y2="3" />
                  <line x1="20" x2="20" y1="21" y2="16" />
                  <line x1="20" x2="20" y1="12" y2="3" />
                  <line x1="1" x2="7" y1="14" y2="14" />
                  <line x1="9" x2="15" y1="8" y2="8" />
                  <line x1="17" x2="23" y1="16" y2="16" />
                </svg>
                <span>Filters</span>
                <svg className="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                </svg>
              </button>
            </div>
          </section>

          {/* ========================================================
              7 KPI METRICS CARDS ROW
          ======================================================== */}
          <section className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3" data-purpose="kpi-metric-cards">
            {/* Metric 1 */}
            <div className="bg-[#111827] p-3.5 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-400">Total Feedback</span>
                <div className="w-6 h-6 rounded-md bg-blue-500/10 text-blue-400 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                  </svg>
                </div>
              </div>
              <div className="mt-2">
                <div className="text-xl font-bold text-white tracking-tight">1,248</div>
                <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-medium mt-1">
                  <span>↑ 18.4%</span>
                  <span className="text-slate-500 font-normal">vs last 7 days</span>
                </div>
              </div>
            </div>

            {/* Metric 2 */}
            <div className="bg-[#111827] p-3.5 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-400">Resolved Feedback</span>
                <div className="w-6 h-6 rounded-md bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </div>
              </div>
              <div className="mt-2">
                <div className="text-xl font-bold text-white tracking-tight">642</div>
                <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-medium mt-1">
                  <span>↑ 22.7%</span>
                  <span className="text-slate-500 font-normal">vs last 7 days</span>
                </div>
              </div>
            </div>

            {/* Metric 3 */}
            <div className="bg-[#111827] p-3.5 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-400">Open Feedback</span>
                <div className="w-6 h-6 rounded-md bg-rose-500/10 text-rose-400 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" x2="12" y1="8" y2="12" />
                    <line x1="12" x2="12.01" y1="16" y2="16" />
                  </svg>
                </div>
              </div>
              <div className="mt-2">
                <div className="text-xl font-bold text-white tracking-tight">606</div>
                <div className="flex items-center gap-1 text-[10px] text-rose-400 font-medium mt-1">
                  <span>↓ 6.3%</span>
                  <span className="text-slate-500 font-normal">vs last 7 days</span>
                </div>
              </div>
            </div>

            {/* Metric 4 */}
            <div className="bg-[#111827] p-3.5 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-400">Resolution Rate</span>
                <div className="w-6 h-6 rounded-md bg-teal-500/10 text-teal-400 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" />
                    <path d="m9 12 2 2 4-4" />
                  </svg>
                </div>
              </div>
              <div className="mt-2">
                <div className="text-xl font-bold text-white tracking-tight">51.4%</div>
                <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-medium mt-1">
                  <span>↑ 7.8%</span>
                  <span className="text-slate-500 font-normal">vs last 7 days</span>
                </div>
              </div>
            </div>

            {/* Metric 5 */}
            <div className="bg-[#111827] p-3.5 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-400">Avg. Resolution Time</span>
                <div className="w-6 h-6 rounded-md bg-amber-500/10 text-amber-400 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12 6 12 12 16 14" />
                  </svg>
                </div>
              </div>
              <div className="mt-2">
                <div className="text-xl font-bold text-white tracking-tight">
                  3.6 <span className="text-xs font-medium text-slate-400">days</span>
                </div>
                <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-medium mt-1">
                  <span>↓ 0.8 days</span>
                  <span className="text-slate-500 font-normal">vs last 7 days</span>
                </div>
              </div>
            </div>

            {/* Metric 6 */}
            <div className="bg-[#111827] p-3.5 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-400">PRDs Generated</span>
                <div className="w-6 h-6 rounded-md bg-purple-500/10 text-purple-400 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <polygon points="12 2 2 7 12 12 22 7 12 2" />
                    <polyline points="2 17 12 22 22 17" />
                    <polyline points="2 12 12 17 22 12" />
                  </svg>
                </div>
              </div>
              <div className="mt-2">
                <div className="text-xl font-bold text-white tracking-tight">18</div>
                <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-medium mt-1">
                  <span>↑ 12.5%</span>
                  <span className="text-slate-500 font-normal">vs last 7 days</span>
                </div>
              </div>
            </div>

            {/* Metric 7 */}
            <div className="bg-[#111827] p-3.5 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-400">PRDs Validated</span>
                <div className="w-6 h-6 rounded-md bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="16" x2="8" y1="13" y2="13" />
                  </svg>
                </div>
              </div>
              <div className="mt-2">
                <div className="text-xl font-bold text-white tracking-tight">12</div>
                <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-medium mt-1">
                  <span>↑ 20%</span>
                  <span className="text-slate-500 font-normal">vs last 7 days</span>
                </div>
              </div>
            </div>
          </section>

          {/* ========================================================
              CHARTS ROW 1: DUAL LINE CHART + 2 DONUT CHARTS
          ======================================================== */}
          <section className="grid grid-cols-1 lg:grid-cols-12 gap-4" data-purpose="feedback-charts">
            {/* Feedback Trend Dual Line Chart (6 cols) */}
            <div className="lg:col-span-6 bg-[#111827] p-4 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-4">
                  <h2 className="text-sm font-semibold text-white">Feedback Trend</h2>
                  <div className="flex items-center gap-3 text-xs">
                    <span className="flex items-center gap-1.5 text-purple-400 text-[11px]">
                      <span className="w-2.5 h-2.5 rounded-full bg-purple-500"></span> Total Feedback
                    </span>
                    <span className="flex items-center gap-1.5 text-emerald-400 text-[11px]">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Resolved Feedback
                    </span>
                  </div>
                </div>

                {/* Granularity Dropdown */}
                <select
                  value={trendGranularity}
                  onChange={(e) => setTrendGranularity(e.target.value)}
                  className="px-2.5 py-1 text-xs rounded-md bg-[#162032] border border-slate-800 text-slate-300 font-medium outline-none cursor-pointer"
                >
                  <option>Daily</option>
                  <option>Weekly</option>
                  <option>Monthly</option>
                </select>
              </div>

              {/* Trend Chart Visual */}
              <div className="relative w-full h-56 pt-2">
                {/* Y-Axis labels and grid lines */}
                <div className="absolute inset-0 flex flex-col justify-between pointer-events-none text-[10px] text-slate-500">
                  <div className="flex items-center gap-2">
                    <span className="w-6 text-right">1200</span>
                    <div className="h-px bg-slate-800/60 w-full"></div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="w-6 text-right">900</span>
                    <div className="h-px bg-slate-800/60 w-full"></div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="w-6 text-right">600</span>
                    <div className="h-px bg-slate-800/60 w-full"></div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="w-6 text-right">300</span>
                    <div className="h-px bg-slate-800/60 w-full"></div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="w-6 text-right">0</span>
                    <div className="h-px bg-slate-800/60 w-full"></div>
                  </div>
                </div>

                {/* SVG Curves with Smooth Gradients */}
                <svg className="w-full h-full pl-8 pb-5 overflow-visible" preserveAspectRatio="none" viewBox="0 0 500 180">
                  <defs>
                    <linearGradient id="purpleGradReports" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.35" />
                      <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.0" />
                    </linearGradient>
                    <linearGradient id="emeraldGradReports" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%" stopColor="#10b981" stopOpacity="0.3" />
                      <stop offset="100%" stopColor="#10b981" stopOpacity="0.0" />
                    </linearGradient>
                  </defs>

                  {/* Total Feedback Filled Gradient */}
                  <path d="M 10 155 Q 80 140, 150 115 T 290 75 T 420 35 T 490 15 L 490 180 L 10 180 Z" fill="url(#purpleGradReports)" />
                  <path d="M 10 155 Q 80 140, 150 115 T 290 75 T 420 35 T 490 15" fill="none" stroke="#a855f7" strokeLinecap="round" strokeWidth="2.5" />

                  {/* Data dots purple */}
                  {[
                    { cx: 10, cy: 155, val: 145, date: 'May 13' },
                    { cx: 78, cy: 142, val: 230, date: 'May 14' },
                    { cx: 147, cy: 125, val: 310, date: 'May 15' },
                    { cx: 216, cy: 105, val: 440, date: 'May 16' },
                    { cx: 285, cy: 82, val: 580, date: 'May 17' },
                    { cx: 354, cy: 62, val: 720, date: 'May 18' },
                    { cx: 423, cy: 38, val: 980, date: 'May 19' },
                    { cx: 490, cy: 15, val: 1248, date: 'May 20' },
                  ].map((pt, i) => (
                    <circle
                      key={i}
                      cx={pt.cx}
                      cy={pt.cy}
                      r="4"
                      className="fill-purple-500 hover:r-6 cursor-pointer transition-all stroke-white stroke-1"
                      onMouseEnter={() => setHoveredPoint({ ...pt, type: 'Total Feedback' })}
                      onMouseLeave={() => setHoveredPoint(null)}
                    />
                  ))}

                  {/* Resolved Feedback Filled Gradient */}
                  <path d="M 10 170 Q 80 162, 150 150 T 290 130 T 420 95 T 490 70 L 490 180 L 10 180 Z" fill="url(#emeraldGradReports)" />
                  <path d="M 10 170 Q 80 162, 150 150 T 290 130 T 420 95 T 490 70" fill="none" stroke="#10b981" strokeLinecap="round" strokeWidth="2.5" />

                  {/* Data dots green */}
                  {[
                    { cx: 10, cy: 170, val: 70, date: 'May 13' },
                    { cx: 78, cy: 162, val: 110, date: 'May 14' },
                    { cx: 147, cy: 152, val: 175, date: 'May 15' },
                    { cx: 216, cy: 142, val: 235, date: 'May 16' },
                    { cx: 285, cy: 130, val: 320, date: 'May 17' },
                    { cx: 354, cy: 115, val: 410, date: 'May 18' },
                    { cx: 423, cy: 95, val: 530, date: 'May 19' },
                    { cx: 490, cy: 70, val: 642, date: 'May 20' },
                  ].map((pt, i) => (
                    <circle
                      key={i}
                      cx={pt.cx}
                      cy={pt.cy}
                      r="4"
                      className="fill-emerald-500 hover:r-6 cursor-pointer transition-all stroke-white stroke-1"
                      onMouseEnter={() => setHoveredPoint({ ...pt, type: 'Resolved' })}
                      onMouseLeave={() => setHoveredPoint(null)}
                    />
                  ))}
                </svg>

                {/* Hover Tooltip display */}
                {hoveredPoint && (
                  <div className="absolute top-2 left-1/2 -translate-x-1/2 bg-slate-900 border border-slate-700 px-2.5 py-1 rounded-md text-[11px] shadow-lg text-white">
                    <strong>{hoveredPoint.date}</strong>: {hoveredPoint.type} = <strong>{hoveredPoint.val}</strong>
                  </div>
                )}

                {/* X-Axis Labels */}
                <div className="flex justify-between pl-8 text-[10px] text-slate-500 pt-1">
                  {trendData.map((d, i) => (
                    <span key={i}>{d.date}</span>
                  ))}
                </div>
              </div>
            </div>

            {/* Feedback by Priority (3 cols) */}
            <div className="lg:col-span-3 bg-[#111827] p-4 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <h2 className="text-sm font-semibold text-white mb-3">Feedback by Priority</h2>
              <div className="flex items-center gap-4 my-auto">
                {/* Donut SVG */}
                <div className="relative w-28 h-28 flex-shrink-0 flex items-center justify-center">
                  <svg className="w-28 h-28 -rotate-90" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#1f293d" strokeWidth="14" />
                    {/* Critical P0 (Red) 26.1% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#ef4444" strokeDasharray="62.4 238.7" strokeDashoffset="0" strokeWidth="14" />
                    {/* High P1 (Orange) 36.2% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#f97316" strokeDasharray="86.5 238.7" strokeDashoffset="-62.4" strokeWidth="14" />
                    {/* Medium P2 (Blue) 25.0% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#3b82f6" strokeDasharray="59.7 238.7" strokeDashoffset="-148.9" strokeWidth="14" />
                    {/* Low P3 (Cyan) 12.7% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#06b6d4" strokeDasharray="30.3 238.7" strokeDashoffset="-208.6" strokeWidth="14" />
                  </svg>
                </div>

                {/* Priority Breakdown List */}
                <div className="flex-1 space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded-full bg-red-500"></span>Critical (P0)
                    </span>
                    <span className="font-semibold text-slate-200">
                      326 <span className="text-slate-400 font-normal">(26.1%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded-full bg-orange-500"></span>High (P1)
                    </span>
                    <span className="font-semibold text-slate-200">
                      452 <span className="text-slate-400 font-normal">(36.2%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded-full bg-blue-500"></span>Medium (P2)
                    </span>
                    <span className="font-semibold text-slate-200">
                      312 <span className="text-slate-400 font-normal">(25.0%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded-full bg-cyan-500"></span>Low (P3)
                    </span>
                    <span className="font-semibold text-slate-200">
                      158 <span className="text-slate-400 font-normal">(12.7%)</span>
                    </span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span className="text-slate-400">Total</span>
                <span className="font-bold text-white">1,248</span>
              </div>
            </div>

            {/* Feedback by Status (3 cols) */}
            <div className="lg:col-span-3 bg-[#111827] p-4 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <h2 className="text-sm font-semibold text-white mb-3">Feedback by Status</h2>
              <div className="flex items-center gap-4 my-auto">
                {/* Donut SVG */}
                <div className="relative w-28 h-28 flex-shrink-0 flex items-center justify-center">
                  <svg className="w-28 h-28 -rotate-90" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#1f293d" strokeWidth="14" />
                    {/* Open (Blue) 48.7% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#3b82f6" strokeDasharray="116.2 238.7" strokeDashoffset="0" strokeWidth="14" />
                    {/* In Progress (Orange) 23.0% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#f97316" strokeDasharray="54.9 238.7" strokeDashoffset="-116.2" strokeWidth="14" />
                    {/* Resolved (Emerald) 51.4% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#10b981" strokeDasharray="45.0 238.7" strokeDashoffset="-171.1" strokeWidth="14" />
                    {/* Closed (Slate/Gray) 13.2% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#64748b" strokeDasharray="22.6 238.7" strokeDashoffset="-216.1" strokeWidth="14" />
                  </svg>
                </div>

                {/* Status Breakdown List */}
                <div className="flex-1 space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded-full bg-blue-500"></span>Open
                    </span>
                    <span className="font-semibold text-slate-200">
                      606 <span className="text-slate-400 font-normal">(48.7%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded-full bg-orange-500"></span>In Progress
                    </span>
                    <span className="font-semibold text-slate-200">
                      286 <span className="text-slate-400 font-normal">(23.0%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span>Resolved
                    </span>
                    <span className="font-semibold text-slate-200">
                      642 <span className="text-slate-400 font-normal">(51.4%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded-full bg-slate-500"></span>Closed
                    </span>
                    <span className="font-semibold text-slate-200">
                      164 <span className="text-slate-400 font-normal">(13.2%)</span>
                    </span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span className="text-slate-400">Total</span>
                <span className="font-bold text-white">1,248</span>
              </div>
            </div>
          </section>

          {/* ========================================================
              DATA & SUMMARY ROW 2: CATEGORIES + PRD SUMMARY + ROADMAP
          ======================================================== */}
          <section className="grid grid-cols-1 lg:grid-cols-12 gap-4" data-purpose="categories-prd-roadmap">
            {/* Top Feedback Categories (4 cols) */}
            <div className="lg:col-span-4 bg-[#111827] p-4 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-semibold text-white">Top Feedback Categories</h2>
                <button onClick={() => alert('Viewing all categories')} className="text-xs text-purple-400 hover:text-purple-300 font-medium">
                  View all
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="text-slate-400 border-b border-slate-800/70 pb-2">
                      <th className="pb-2 font-medium">Category</th>
                      <th className="pb-2 font-medium">Feedback</th>
                      <th className="pb-2 font-medium">% of Total</th>
                      <th className="pb-2 font-medium text-right">Trend</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Checkout & Payments</td>
                      <td className="py-2.5 text-slate-300">342</td>
                      <td className="py-2.5 text-slate-400">27.4%</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-14 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 12 Q 15 15, 30 7 T 60 2" fill="none" stroke="#10b981" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Login & Authentication</td>
                      <td className="py-2.5 text-slate-300">218</td>
                      <td className="py-2.5 text-slate-400">17.5%</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-14 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 10 Q 20 4, 35 12 T 60 5" fill="none" stroke="#10b981" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Product Search</td>
                      <td className="py-2.5 text-slate-300">186</td>
                      <td className="py-2.5 text-slate-400">14.9%</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-14 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 4 Q 20 12, 40 5 T 60 14" fill="none" stroke="#ef4444" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Cart & Wishlist</td>
                      <td className="py-2.5 text-slate-300">164</td>
                      <td className="py-2.5 text-slate-400">13.1%</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-14 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 14 Q 25 15, 40 6 T 60 3" fill="none" stroke="#10b981" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Performance</td>
                      <td className="py-2.5 text-slate-300">128</td>
                      <td className="py-2.5 text-slate-400">10.3%</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-14 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 12 Q 20 14, 38 6 T 60 4" fill="none" stroke="#06b6d4" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* PRD Summary (4 cols) */}
            <div className="lg:col-span-4 bg-[#111827] p-4 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-semibold text-white">PRD Summary</h2>
                <button onClick={() => onNavigate && onNavigate('Requirements')} className="text-xs text-purple-400 hover:text-purple-300 font-medium">
                  View all
                </button>
              </div>

              <div className="flex items-center gap-5 my-auto">
                <div className="relative w-28 h-28 flex-shrink-0 flex items-center justify-center">
                  <svg className="w-28 h-28 -rotate-90" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#1f293d" strokeWidth="13" />
                    {/* Draft (Purple) 22.2% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#8b5cf6" strokeDasharray="53 238.7" strokeDashoffset="0" strokeWidth="13" />
                    {/* Pending Validation (Amber) 16.7% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#f59e0b" strokeDasharray="40 238.7" strokeDashoffset="-53" strokeWidth="13" />
                    {/* Validated (Emerald) 66.7% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#10b981" strokeDasharray="100 238.7" strokeDashoffset="-93" strokeWidth="13" />
                    {/* Shared (Blue) 50% */}
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#3b82f6" strokeDasharray="45 238.7" strokeDashoffset="-193" strokeWidth="13" />
                  </svg>
                  <div className="absolute text-center flex flex-col items-center justify-center">
                    <span className="text-lg font-bold text-white leading-none">18</span>
                    <span className="text-[9px] text-slate-400 mt-0.5 font-medium">Total PRDs</span>
                  </div>
                </div>

                <div className="flex-1 space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded bg-purple-500"></span>Draft
                    </span>
                    <span className="font-semibold text-slate-200">
                      4 <span className="text-slate-400 font-normal">(22.2%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded bg-amber-500"></span>Pending Validation
                    </span>
                    <span className="font-semibold text-slate-200">
                      3 <span className="text-slate-400 font-normal">(16.7%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded bg-emerald-500"></span>Validated
                    </span>
                    <span className="font-semibold text-slate-200">
                      12 <span className="text-slate-400 font-normal">(66.7%)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-slate-400">
                      <span className="w-2 h-2 rounded bg-blue-500"></span>Shared
                    </span>
                    <span className="font-semibold text-slate-200">
                      9 <span className="text-slate-400 font-normal">(50.0%)</span>
                    </span>
                  </div>
                </div>
              </div>

              {/* Bottom PRD sub metrics */}
              <div className="pt-3 border-t border-slate-800/80 grid grid-cols-3 gap-2 text-center text-xs">
                <div>
                  <div className="text-[10px] text-slate-400">Avg. Validation Time</div>
                  <div className="font-bold text-slate-200 mt-0.5">2.3 days</div>
                </div>
                <div>
                  <div className="text-[10px] text-slate-400">PRDs Shared</div>
                  <div className="font-bold text-slate-200 mt-0.5">9</div>
                </div>
                <div>
                  <div className="text-[10px] text-slate-400">Pending Review</div>
                  <div className="font-bold text-slate-200 mt-0.5">3</div>
                </div>
              </div>
            </div>

            {/* Roadmap Progress (4 cols) */}
            <div className="lg:col-span-4 bg-[#111827] p-4 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-semibold text-white">Roadmap Progress</h2>
                <button onClick={() => onNavigate && onNavigate('Roadmap')} className="text-xs text-purple-400 hover:text-purple-300 font-medium">
                  View all
                </button>
              </div>

              <div className="flex items-center gap-5 my-auto">
                {/* 68% Circular Gauge */}
                <div className="relative w-28 h-28 flex-shrink-0 flex items-center justify-center">
                  <svg className="w-28 h-28 -rotate-90" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#1f293d" strokeWidth="8" />
                    <circle cx="50" cy="50" fill="transparent" r="38" stroke="#3b82f6" strokeDasharray="162 238.7" strokeLinecap="round" strokeWidth="8" />
                  </svg>
                  <div className="absolute text-center flex flex-col items-center justify-center">
                    <span className="text-xl font-bold text-white leading-none">68%</span>
                    <span className="text-[9px] text-slate-400 mt-1 font-medium">Overall Progress</span>
                  </div>
                </div>

                {/* Breakdown Progress Bars */}
                <div className="flex-1 space-y-2 text-xs">
                  <div>
                    <div className="flex justify-between text-[11px] mb-0.5">
                      <span className="text-slate-400">Discovery & Analysis</span>
                      <span className="text-emerald-400 font-semibold flex items-center gap-1">
                        100%{' '}
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                      </span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: '100%' }}></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[11px] mb-0.5">
                      <span className="text-slate-400">PRD & Planning</span>
                      <span className="text-purple-400 font-semibold">85%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-purple-500 h-1.5 rounded-full" style={{ width: '85%' }}></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[11px] mb-0.5">
                      <span className="text-slate-400">Design & Architecture</span>
                      <span className="text-blue-400 font-semibold">60%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '60%' }}></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[11px] mb-0.5">
                      <span className="text-slate-400">Implementation</span>
                      <span className="text-cyan-400 font-semibold">45%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-cyan-500 h-1.5 rounded-full" style={{ width: '45%' }}></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[11px] mb-0.5">
                      <span className="text-slate-400">Testing & QA</span>
                      <span className="text-amber-400 font-semibold">25%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-amber-500 h-1.5 rounded-full" style={{ width: '25%' }}></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[11px] mb-0.5">
                      <span className="text-slate-400">Deployment</span>
                      <span className="text-slate-500 font-semibold">0%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-slate-600 h-1.5 rounded-full" style={{ width: '0%' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* ========================================================
              TABLES & ACTIVITY ROW 3: RESOLUTION + RECENT ACTIVITY
          ======================================================== */}
          <section className="grid grid-cols-1 lg:grid-cols-12 gap-4" data-purpose="resolution-and-activity">
            {/* Resolution Performance (7 cols) */}
            <div className="lg:col-span-7 bg-[#111827] p-4 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-semibold text-white">Resolution Performance</h2>
                <button onClick={() => alert('Viewing resolution analytics')} className="text-xs text-purple-400 hover:text-purple-300 font-medium">
                  View all
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="text-slate-400 border-b border-slate-800/70 pb-2">
                      <th className="pb-2 font-medium">Metric</th>
                      <th className="pb-2 font-medium">This Week</th>
                      <th className="pb-2 font-medium">Last Week</th>
                      <th className="pb-2 font-medium">Change</th>
                      <th className="pb-2 font-medium text-right">Trend</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Feedback Resolved</td>
                      <td className="py-2.5 text-slate-300 font-semibold">113</td>
                      <td className="py-2.5 text-slate-400">92</td>
                      <td className="py-2.5 text-emerald-400 font-medium">↑ 22.8%</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-16 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 13 Q 15 15, 30 8 T 60 2" fill="none" stroke="#10b981" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Avg. Resolution Time</td>
                      <td className="py-2.5 text-slate-300 font-semibold">3.6 days</td>
                      <td className="py-2.5 text-slate-400">4.4 days</td>
                      <td className="py-2.5 text-emerald-400 font-medium">↓ 0.8 days</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-16 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 12 Q 20 14, 40 7 T 60 4" fill="none" stroke="#10b981" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Resolution Rate</td>
                      <td className="py-2.5 text-slate-300 font-semibold">51.4%</td>
                      <td className="py-2.5 text-slate-400">43.6%</td>
                      <td className="py-2.5 text-emerald-400 font-medium">↑ 7.8%</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-16 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 14 Q 25 15, 42 6 T 60 2" fill="none" stroke="#10b981" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                    <tr>
                      <td className="py-2.5 font-medium text-slate-200">Reopened Feedback</td>
                      <td className="py-2.5 text-slate-300 font-semibold">24</td>
                      <td className="py-2.5 text-slate-400">31</td>
                      <td className="py-2.5 text-rose-400 font-medium">↓ 22.6%</td>
                      <td className="py-2.5 text-right">
                        <svg className="w-16 h-4 ml-auto" viewBox="0 0 60 16">
                          <path d="M0 4 Q 20 12, 40 6 T 60 14" fill="none" stroke="#ef4444" strokeWidth="1.8" />
                        </svg>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Recent Activity (5 cols) */}
            <div className="lg:col-span-5 bg-[#111827] p-4 rounded-xl border border-slate-800/90 dark:border-[#1E293B] shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-semibold text-white">Recent Activity</h2>
                <button onClick={() => alert('Viewing full audit log')} className="text-xs text-purple-400 hover:text-purple-300 font-medium">
                  View all
                </button>
              </div>

              <div className="space-y-3 my-auto">
                <div className="flex items-start gap-3">
                  <div className="w-7 h-7 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-semibold text-slate-200 truncate">Feedback #1248 resolved</p>
                      <span className="text-[10px] text-slate-400 flex-shrink-0 ml-2">May 20, 2025 10:30 AM</span>
                    </div>
                    <p className="text-[11px] text-slate-400 truncate">Checkout page error on coupon apply</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-7 h-7 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                      <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-semibold text-slate-200 truncate">PRD "One-click Checkout" validated</p>
                      <span className="text-[10px] text-slate-400 flex-shrink-0 ml-2">May 20, 2025 09:15 AM</span>
                    </div>
                    <p className="text-[11px] text-slate-400 truncate">Version 1.0</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-7 h-7 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                      <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-semibold text-slate-200 truncate">Roadmap updated</p>
                      <span className="text-[10px] text-slate-400 flex-shrink-0 ml-2">May 19, 2025 06:45 PM</span>
                    </div>
                    <p className="text-[11px] text-slate-400 truncate">3 tasks moved to In-progress</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-7 h-7 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                      <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-semibold text-slate-200 truncate">Feedback #1242 assigned</p>
                      <span className="text-[10px] text-slate-400 flex-shrink-0 ml-2">May 19, 2025 04:20 PM</span>
                    </div>
                    <p className="text-[11px] text-slate-400 truncate">Login failure on mobile devices</p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>

      {/* ========================================================
          MODALS
      ======================================================== */}
      {/* Export Modal */}
      {showExportModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#121929] border border-slate-800 rounded-xl max-w-sm w-full p-5 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Export Reports Overview</h3>
              <button onClick={() => setShowExportModal(false)} className="text-slate-400 hover:text-slate-200">
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-400">
              Download complete analytics for <strong>{selectedRange}</strong>:
            </p>

            <div className="space-y-2 text-xs">
              <button
                onClick={() => {
                  alert('Exporting PDF executive summary report...');
                  setShowExportModal(false);
                }}
                className="w-full flex items-center justify-between p-2.5 rounded-lg border border-slate-800 hover:bg-slate-800/60 transition text-left"
              >
                <div className="flex items-center gap-2">
                  <span>📑</span>
                  <span className="font-semibold text-slate-200">PDF Executive Summary</span>
                </div>
                <span className="text-[10px] text-slate-400">.pdf</span>
              </button>

              <button
                onClick={() => {
                  alert('Exporting raw Excel metrics dataset...');
                  setShowExportModal(false);
                }}
                className="w-full flex items-center justify-between p-2.5 rounded-lg border border-slate-800 hover:bg-slate-800/60 transition text-left"
              >
                <div className="flex items-center gap-2">
                  <span>📊</span>
                  <span className="font-semibold text-slate-200">Excel / CSV Raw Data</span>
                </div>
                <span className="text-[10px] text-slate-400">.csv</span>
              </button>

              <button
                onClick={() => {
                  alert('Generating presentation slides...');
                  setShowExportModal(false);
                }}
                className="w-full flex items-center justify-between p-2.5 rounded-lg border border-slate-800 hover:bg-slate-800/60 transition text-left"
              >
                <div className="flex items-center gap-2">
                  <span>📽️</span>
                  <span className="font-semibold text-slate-200">Slide Deck Presentation</span>
                </div>
                <span className="text-[10px] text-slate-400">.pptx</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Filter Modal */}
      {showFilterModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#121929] border border-slate-800 rounded-xl max-w-sm w-full p-5 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Filter Reports</h3>
              <button onClick={() => setShowFilterModal(false)} className="text-slate-400 hover:text-slate-200">
                ✕
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-300 mb-1">Priority Level</label>
                <select
                  value={filterPriority}
                  onChange={(e) => setFilterPriority(e.target.value)}
                  className="w-full px-3 py-1.5 rounded-lg border border-slate-700 bg-[#0B0F17] text-slate-200"
                >
                  <option value="All">All Priorities</option>
                  <option value="P0">Critical (P0)</option>
                  <option value="P1">High (P1)</option>
                  <option value="P2">Medium (P2)</option>
                  <option value="P3">Low (P3)</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-300 mb-1">Feedback Category</label>
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="w-full px-3 py-1.5 rounded-lg border border-slate-700 bg-[#0B0F17] text-slate-200"
                >
                  <option value="All">All Categories</option>
                  <option value="Checkout">Checkout & Payments</option>
                  <option value="Login">Login & Authentication</option>
                  <option value="Search">Product Search</option>
                  <option value="Cart">Cart & Wishlist</option>
                  <option value="Performance">Performance</option>
                </select>
              </div>
            </div>

            <div className="flex justify-between items-center pt-2 border-t border-slate-800">
              <button
                onClick={() => {
                  setFilterPriority('All');
                  setFilterCategory('All');
                  setShowFilterModal(false);
                }}
                className="text-xs text-purple-400 hover:underline"
              >
                Reset Filters
              </button>
              <button
                onClick={() => setShowFilterModal(false)}
                className="px-3.5 py-1.5 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-semibold"
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
