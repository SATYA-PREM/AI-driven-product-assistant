import React, { useState, useEffect, useMemo } from 'react';

export default function WorkspacesPage() {
  // Theme state: dark / light with localStorage persistence
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('theme');
      if (saved) return saved === 'dark';
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  // Search input state
  const [searchQuery, setSearchQuery] = useState('');

  // Active navigation link
  const [activeNav, setActiveNav] = useState('Workspaces');

  // Interactive Modals
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showAddSourceModal, setShowAddSourceModal] = useState(false);

  // Form states
  const [newWsName, setNewWsName] = useState('');
  const [newWsDesc, setNewWsDesc] = useState('');
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState('Member');
  const [newSourceName, setNewSourceName] = useState('');
  const [newSourceCount, setNewSourceCount] = useState('');

  // Synchronize dark class on <html>
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

  // Workspace Info
  const workspaceInfo = {
    name: 'E-Commerce Platform',
    status: 'Active',
    description:
      'Central workspace for analyzing customer feedback, discovering insights, and building better e-commerce experiences.',
    owner: 'Priya Sharma',
    memberCount: 12,
    createdDate: 'Aug 01, 2025',
    storageUsedGB: 7.8,
    storageTotalGB: 10,
    storagePercent: 78,
  };

  // 5 Metrics Cards Data
  const metrics = [
    {
      id: 'feedback',
      title: 'Total Feedback',
      value: '12,842',
      trend: '↑ 18.6%',
      subtext: 'vs last 30 days',
      trendColor: 'text-emerald-600 dark:text-emerald-400',
      iconBox: 'bg-purple-50 dark:bg-purple-500/20 text-purple-600 dark:text-purple-400 border border-purple-100 dark:border-purple-500/30',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      id: 'features',
      title: 'Total Features',
      value: '56',
      trend: '↑ 12.0%',
      subtext: 'vs last 30 days',
      trendColor: 'text-emerald-600 dark:text-emerald-400',
      iconBox: 'bg-blue-50 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-500/30',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M4 6h16M4 10h16M4 14h16M4 18h16" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      id: 'insights',
      title: 'Insights Generated',
      value: '128',
      trend: '↑ 15.7%',
      subtext: 'vs last 30 days',
      trendColor: 'text-emerald-600 dark:text-emerald-400',
      iconBox: 'bg-emerald-50 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-500/30',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      id: 'members',
      title: 'Active Members',
      value: '12',
      trend: '↑ 20.0%',
      subtext: 'vs last 30 days',
      trendColor: 'text-emerald-600 dark:text-emerald-400',
      iconBox: 'bg-amber-50 dark:bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-100 dark:border-amber-500/30',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      id: 'sources',
      title: 'Data Sources',
      value: '8',
      trend: '↑ 2 new',
      subtext: 'vs last 30 days',
      trendColor: 'text-emerald-600 dark:text-emerald-400',
      iconBox: 'bg-cyan-50 dark:bg-cyan-500/20 text-cyan-600 dark:text-cyan-400 border border-cyan-100 dark:border-cyan-500/30',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
  ];

  // Recent Activities
  const [activitiesList] = useState([
    {
      id: 1,
      activity: 'Added 320 new feedback items',
      iconBg: 'bg-purple-50 text-purple-600 dark:bg-purple-500/10 dark:text-purple-400 border border-purple-100 dark:border-transparent',
      icon: (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
      user: 'Priya Sharma',
      userType: 'avatar',
      avatarBg: 'bg-pink-100 dark:bg-pink-600/20 text-pink-600 dark:text-pink-400 ring-1 ring-pink-200 dark:ring-pink-500/30',
      module: 'Feedback',
      moduleBadge: 'bg-blue-50 text-blue-700 border border-blue-100 dark:border-transparent dark:bg-blue-900/30 dark:text-blue-400',
      time: '2 hours ago',
    },
    {
      id: 2,
      activity: 'AI generated 15 new insights',
      iconBg: 'bg-emerald-50 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-400 border border-emerald-100 dark:border-transparent',
      icon: (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M13 10V3L4 14h7v7l9-11h-7z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
      user: 'AI Assistant',
      userType: 'ai',
      module: 'Insights',
      moduleBadge: 'bg-emerald-50 text-emerald-700 border border-emerald-100 dark:border-transparent dark:bg-emerald-900/30 dark:text-emerald-400',
      time: '3 hours ago',
    },
    {
      id: 3,
      activity: 'Created feature "One-click checkout"',
      iconBg: 'bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-400 border border-blue-100 dark:border-transparent',
      icon: (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
      user: 'Arjun Mehta',
      userType: 'avatar',
      avatarBg: 'bg-blue-100 dark:bg-blue-600/20 text-blue-600 dark:text-blue-500 ring-1 ring-blue-200 dark:ring-blue-500/30',
      module: 'Features',
      moduleBadge: 'bg-cyan-50 text-cyan-700 border border-cyan-100 dark:border-transparent dark:bg-cyan-900/30 dark:text-cyan-400',
      time: '5 hours ago',
    },
    {
      id: 4,
      activity: 'Updated priority for 3 features',
      iconBg: 'bg-amber-50 text-amber-600 dark:bg-amber-500/10 dark:text-amber-400 border border-amber-100 dark:border-transparent',
      icon: (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
      user: 'Neha Kapoor',
      userType: 'avatar',
      avatarBg: 'bg-emerald-100 dark:bg-emerald-600/20 text-emerald-600 dark:text-emerald-500 ring-1 ring-emerald-200 dark:ring-emerald-500/30',
      module: 'Prioritization',
      moduleBadge: 'bg-amber-50 text-amber-700 border border-amber-100 dark:border-transparent dark:bg-amber-900/30 dark:text-amber-400',
      time: '1 day ago',
    },
    {
      id: 5,
      activity: 'Added 2 new requirements',
      iconBg: 'bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400 border border-indigo-100 dark:border-transparent',
      icon: (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
      user: 'Rohit Singh',
      userType: 'avatar',
      avatarBg: 'bg-teal-100 dark:bg-teal-600/20 text-teal-600 dark:text-teal-500 ring-1 ring-teal-200 dark:ring-teal-500/30',
      module: 'Requirements',
      moduleBadge: 'bg-indigo-50 text-indigo-700 border border-indigo-100 dark:border-transparent dark:bg-indigo-900/30 dark:text-indigo-400',
      time: '1 day ago',
    },
    {
      id: 6,
      activity: 'Updated roadmap timeline',
      iconBg: 'bg-rose-50 text-rose-600 dark:bg-rose-500/10 dark:text-rose-400 border border-rose-100 dark:border-transparent',
      icon: (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
      user: 'Priya Sharma',
      userType: 'avatar',
      avatarBg: 'bg-pink-100 dark:bg-pink-600/20 text-pink-600 dark:text-pink-500 ring-1 ring-pink-200 dark:ring-pink-500/30',
      module: 'Roadmap',
      moduleBadge: 'bg-rose-50 text-rose-700 border border-rose-100 dark:border-transparent dark:bg-rose-900/30 dark:text-rose-400',
      time: '2 days ago',
    },
    {
      id: 7,
      activity: 'Generated Feedback Summary Report',
      iconBg: 'bg-cyan-50 text-cyan-600 dark:bg-cyan-500/10 dark:text-cyan-400 border border-cyan-100 dark:border-transparent',
      icon: (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
      user: 'AI Assistant',
      userType: 'ai',
      module: 'Reports',
      moduleBadge: 'bg-purple-50 text-purple-700 border border-purple-100 dark:border-transparent dark:bg-purple-900/30 dark:text-purple-400',
      time: '2 days ago',
    },
  ]);

  // Members List (5 shown, 12 total)
  const [membersList, setMembersList] = useState([
    {
      name: 'Priya Sharma',
      role: 'Product Manager (Owner)',
      badge: 'Owner',
      badgeClass: 'bg-violet-100 text-violet-700 border border-violet-200/60 dark:border-transparent dark:bg-violet-950 dark:text-violet-300 font-semibold',
      gradient: 'from-pink-500 to-rose-500',
      ring: 'ring-pink-100 dark:ring-pink-500/20',
    },
    {
      name: 'Arjun Mehta',
      role: 'Product Analyst',
      badge: 'Admin',
      badgeClass: 'bg-blue-100 text-blue-700 border border-blue-200/60 dark:border-transparent dark:bg-blue-950 dark:text-blue-300 font-semibold',
      gradient: 'from-blue-500 to-indigo-500',
      ring: 'ring-blue-100 dark:ring-blue-500/20',
    },
    {
      name: 'Neha Kapoor',
      role: 'UX Designer',
      badge: 'Member',
      badgeClass: 'bg-slate-100 text-slate-600 border border-slate-200 dark:border-transparent dark:bg-[#182338] dark:text-slate-300 font-medium',
      gradient: 'from-emerald-500 to-teal-500',
      ring: 'ring-emerald-100 dark:ring-emerald-500/20',
    },
    {
      name: 'Rohit Singh',
      role: 'Data Analyst',
      badge: 'Member',
      badgeClass: 'bg-slate-100 text-slate-600 border border-slate-200 dark:border-transparent dark:bg-[#182338] dark:text-slate-300 font-medium',
      gradient: 'from-amber-500 to-orange-500',
      ring: 'ring-amber-100 dark:ring-amber-500/20',
    },
    {
      name: 'Ananya Das',
      role: 'QA Engineer',
      badge: 'Member',
      badgeClass: 'bg-slate-100 text-slate-600 border border-slate-200 dark:border-transparent dark:bg-[#182338] dark:text-slate-300 font-medium',
      gradient: 'from-cyan-500 to-sky-500',
      ring: 'ring-cyan-100 dark:ring-cyan-500/20',
    },
  ]);

  // Data Sources List (8)
  const [dataSources, setDataSources] = useState([
    { name: 'User Interviews', count: '1,245', dotColor: 'bg-blue-500' },
    { name: 'Surveys', count: '1,240', dotColor: 'bg-purple-500' },
    { name: 'Support Tickets', count: '3,642', dotColor: 'bg-cyan-500' },
    { name: 'Social Media', count: '1,098', dotColor: 'bg-indigo-500' },
    { name: 'App Store Reviews', count: '2,185', dotColor: 'bg-emerald-500' },
    { name: 'Email Feedback', count: '956', dotColor: 'bg-sky-500' },
    { name: 'Play Store Reviews', count: '1,876', dotColor: 'bg-emerald-400' },
    { name: 'Internal Notes', count: '600', dotColor: 'bg-amber-500' },
  ]);

  // Primary Navigation Items
  const navItems = [
    {
      name: 'PM Dashboard',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      name: 'Insights',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M13 10V3L4 14h7v7l9-11h-7z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      name: 'Feedback',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      name: 'Features',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      name: 'Prioritization',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      name: 'Requirements',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      name: 'Roadmap',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      name: 'Reports',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
    {
      name: 'AI Assistant',
      icon: (
        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      ),
    },
  ];

  // Filter activities based on search
  const filteredActivities = useMemo(() => {
    if (!searchQuery.trim()) return activitiesList;
    const q = searchQuery.toLowerCase();
    return activitiesList.filter(
      (a) =>
        a.activity.toLowerCase().includes(q) ||
        a.user.toLowerCase().includes(q) ||
        a.module.toLowerCase().includes(q)
    );
  }, [activitiesList, searchQuery]);

  // Handlers
  const handleCreateWorkspace = (e) => {
    e.preventDefault();
    if (!newWsName.trim()) return;
    alert(`Workspace "${newWsName}" created successfully!`);
    setNewWsName('');
    setNewWsDesc('');
    setShowCreateModal(false);
  };

  const handleInviteMember = (e) => {
    e.preventDefault();
    if (!inviteEmail.trim()) return;
    const newMember = {
      name: inviteEmail.split('@')[0],
      role: `${inviteRole}`,
      badge: inviteRole === 'Admin' ? 'Admin' : inviteRole === 'Owner' ? 'Owner' : 'Member',
      badgeClass:
        inviteRole === 'Admin'
          ? 'bg-blue-100 text-blue-700 border border-blue-200/60 dark:border-transparent dark:bg-blue-950 dark:text-blue-300 font-semibold'
          : 'bg-slate-100 text-slate-600 border border-slate-200 dark:border-transparent dark:bg-[#182338] dark:text-slate-300 font-medium',
      gradient: 'from-violet-500 to-indigo-500',
      ring: 'ring-violet-100 dark:ring-violet-500/20',
    };
    setMembersList([...membersList, newMember]);
    alert(`Invited ${inviteEmail} as ${inviteRole}!`);
    setInviteEmail('');
    setShowInviteModal(false);
  };

  const handleAddSource = (e) => {
    e.preventDefault();
    if (!newSourceName.trim()) return;
    setDataSources([
      ...dataSources,
      {
        name: newSourceName,
        count: newSourceCount.trim() || '0',
        dotColor: 'bg-violet-500',
      },
    ]);
    setNewSourceName('');
    setNewSourceCount('');
    setShowAddSourceModal(false);
  };

  return (
    <div className={`flex h-screen overflow-hidden font-sans antialiased transition-colors duration-200 ${isDark ? 'dark bg-[#090d16] text-slate-200' : 'bg-slate-50 text-slate-700'}`}>
      {/* ========================================================
          1. LEFT SIDEBAR
      ======================================================== */}
      <aside className="w-64 flex-shrink-0 bg-white dark:bg-[#0d1322] border-r border-slate-200 dark:border-[#1a2337] flex flex-col justify-between z-30 select-none shadow-[1px_0_4px_rgba(0,0,0,0.02)]">
        {/* Top Section: Brand & Primary Nav */}
        <div className="flex flex-col h-full overflow-y-auto">
          {/* Logo Header */}
          <div className="p-5 flex items-center gap-3 border-b border-slate-100 dark:border-[#172033]">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-violet-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-violet-500/25 flex-shrink-0">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M12 2a7 7 0 0 0-7 7c0 2.38 1.19 4.47 3 5.74V17a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-2.26c1.81-1.27 3-3.36 3-5.74a7 7 0 0 0-7-7M9 21h6" />
              </svg>
            </div>
            <div>
              <h1 className="font-bold text-base text-slate-900 dark:text-white leading-tight tracking-tight">ProdIntel AI</h1>
              <p className="text-[11px] font-medium text-slate-400 dark:text-slate-400 tracking-wide">Product Intelligence Platform</p>
            </div>
          </div>

          {/* Primary Navigation Links */}
          <nav className="px-3 py-4 space-y-1">
            {navItems.map((item) => {
              const isActive = activeNav === item.name;
              return (
                <button
                  key={item.name}
                  onClick={() => setActiveNav(item.name)}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-left ${
                    isActive
                      ? 'bg-violet-50 text-violet-700 dark:bg-violet-600/20 dark:text-violet-300'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33]'
                  }`}
                >
                  {item.icon}
                  <span>{item.name}</span>
                </button>
              );
            })}

            {/* Section Divider: Workspace Sub-menu */}
            <div className="pt-5 pb-1">
              <span className="px-3 text-[10px] font-bold tracking-wider uppercase text-slate-400 dark:text-slate-400">
                Workspace
              </span>
            </div>

            {/* Active Workspaces Button */}
            <button
              onClick={() => setActiveNav('Workspaces')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold bg-violet-50 text-violet-700 border border-violet-200/80 dark:bg-violet-600/20 dark:text-violet-300 dark:border-violet-500/20 shadow-xs text-left"
            >
              <svg className="w-4 h-4 text-violet-600 dark:text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
              <span>Workspaces</span>
            </button>

            {/* Settings Link */}
            <button
              onClick={() => setShowSettingsModal(true)}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors text-left"
            >
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
              <span>Settings</span>
            </button>
          </nav>
        </div>

        {/* Bottom Widget: Current Workspace, Storage, User Profile */}
        <div className="p-3 border-t border-slate-200 dark:border-[#172033] space-y-3 bg-slate-50/50 dark:bg-transparent">
          {/* Active Workspace Picker Pill */}
          <div
            onClick={() => setShowCreateModal(true)}
            className="p-2.5 rounded-lg bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] flex items-center justify-between cursor-pointer hover:border-violet-400 shadow-xs transition-colors"
          >
            <div>
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Current Workspace</p>
              <p className="text-xs font-semibold text-slate-800 dark:text-slate-100 truncate">{workspaceInfo.name}</p>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">{workspaceInfo.memberCount} Members</p>
            </div>
            <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
            </svg>
          </div>

          {/* Storage Progress Widget */}
          <div className="p-2.5 rounded-lg bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] shadow-xs">
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="text-slate-600 dark:text-slate-400 font-medium">Storage</span>
              <span className="text-violet-600 dark:text-violet-400 font-bold">{workspaceInfo.storagePercent}%</span>
            </div>
            <div className="w-full bg-slate-100 dark:bg-[#202c46] h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-gradient-to-r from-violet-600 to-indigo-600 h-full rounded-full transition-all duration-500"
                style={{ width: `${workspaceInfo.storagePercent}%` }}
              ></div>
            </div>
            <div className="text-[10px] text-slate-500 dark:text-slate-400 mt-1 flex justify-between">
              <span>{workspaceInfo.storageUsedGB} GB / {workspaceInfo.storageTotalGB} GB</span>
            </div>
          </div>

          {/* User Profile Footer */}
          <div className="pt-2 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-violet-600 to-fuchsia-600 flex items-center justify-center text-white ring-2 ring-violet-200 dark:ring-violet-400/30 shadow-xs">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path clipRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fillRule="evenodd" />
                </svg>
              </div>
              <div>
                <p className="text-xs font-semibold text-slate-900 dark:text-white leading-tight">Priya Sharma</p>
                <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">Product Manager</p>
              </div>
            </div>
            <button
              onClick={() => setShowSettingsModal(true)}
              className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
            </button>
          </div>
        </div>
      </aside>

      {/* ========================================================
          2. MAIN CONTENT AREA
      ======================================================== */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto bg-slate-50 dark:bg-[#090d16]">
        {/* BEGIN: TopGlobalHeader */}
        <header className="sticky top-0 z-20 bg-white/95 dark:bg-[#090d16]/90 backdrop-blur border-b border-slate-200 dark:border-[#172033] px-8 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4 shadow-xs">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">Workspaces</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Manage all your product workspaces in one place.</p>
          </div>

          <div className="flex items-center gap-3">
            {/* Search Workspace Input */}
            <div className="relative w-64 md:w-72">
              <input
                type="text"
                placeholder="Search workspaces..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-[#222e47] rounded-lg pl-9 pr-3 py-2 text-xs text-slate-900 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 transition-all shadow-xs"
              />
              <svg className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
            </div>

            {/* Interactive Light / Dark Mode Toggle Switch */}
            <button
              onClick={() => setIsDark(!isDark)}
              aria-label="Toggle Light and Dark mode"
              title="Switch Theme"
              className="p-2 rounded-lg bg-white dark:bg-[#141b2c] border border-slate-200 dark:border-[#243048] text-amber-500 dark:text-slate-300 hover:text-amber-600 dark:hover:text-violet-400 hover:border-slate-300 dark:hover:border-violet-400/40 shadow-xs transition-colors flex items-center justify-center"
            >
              {isDark ? (
                /* Moon Icon (when dark) */
                <svg className="w-4 h-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                </svg>
              ) : (
                /* Sun Icon (when light) */
                <svg className="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                </svg>
              )}
            </button>

            {/* Notification Bell with Count Badge */}
            <div className="relative">
              <button className="p-2 rounded-lg bg-white dark:bg-[#141b2c] border border-slate-200 dark:border-[#243048] text-slate-600 dark:text-slate-300 hover:text-violet-600 dark:hover:text-violet-400 hover:border-slate-300 transition-colors shadow-xs">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                </svg>
              </button>
              <span className="absolute -top-1 -right-1 h-4 w-4 bg-rose-500 text-white font-bold text-[10px] rounded-full flex items-center justify-center ring-2 ring-white dark:ring-[#090d16]">
                8
              </span>
            </div>

            {/* Help / Support Icon Button */}
            <button
              onClick={() => alert('ProdIntel AI Workspaces Documentation & Help Guide')}
              className="p-2 rounded-lg bg-white dark:bg-[#141b2c] border border-slate-200 dark:border-[#243048] text-slate-600 dark:text-slate-300 hover:text-violet-600 dark:hover:text-violet-400 hover:border-slate-300 transition-colors shadow-xs"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
            </button>

            {/* Primary CTA Button */}
            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white text-xs font-semibold rounded-lg shadow-sm shadow-violet-600/30 transition-all hover:shadow-md hover:shadow-violet-600/40"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M12 4v16m8-8H4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
              </svg>
              <span>Create Workspace</span>
            </button>
          </div>
        </header>

        {/* Scrollable Main Content Container */}
        <main className="p-8 space-y-6 flex-1">
          {/* ========================================================
              WORKSPACE HERO BANNER CARD
          ======================================================== */}
          <section className="p-6 rounded-2xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] shadow-sm">
            <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
              {/* Left Info Block */}
              <div className="flex items-start gap-4">
                {/* Cart Workspace Icon Badge */}
                <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-violet-600 to-purple-600 flex items-center justify-center text-white shadow-md shadow-violet-600/25 flex-shrink-0 ring-4 ring-violet-50 dark:ring-transparent">
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                  </svg>
                </div>

                {/* Workspace Details */}
                <div className="space-y-2">
                  <div className="flex items-center gap-3">
                    <h3 className="text-xl font-bold text-slate-900 dark:text-white">{workspaceInfo.name}</h3>
                    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-violet-50 text-violet-700 dark:bg-violet-950 dark:text-violet-300 border border-violet-200 dark:border-violet-700">
                      {workspaceInfo.status}
                    </span>
                  </div>

                  <p className="text-xs text-slate-600 dark:text-slate-400 max-w-2xl leading-relaxed">
                    {workspaceInfo.description}
                  </p>

                  {/* Metadata Row */}
                  <div className="flex flex-wrap items-center gap-6 pt-1 text-xs text-slate-500 dark:text-slate-400">
                    {/* Owner with humanoid glyph */}
                    <div className="flex items-center gap-2">
                      <div className="w-5 h-5 rounded-full bg-violet-600 text-white flex items-center justify-center text-[10px] shadow-xs">
                        <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                          <path clipRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fillRule="evenodd" />
                        </svg>
                      </div>
                      <span>
                        <strong className="text-slate-800 dark:text-slate-200">{workspaceInfo.owner}</strong> (You){' '}
                        <span className="text-slate-400">· Workspace Owner</span>
                      </span>
                    </div>

                    {/* Member Count */}
                    <div className="flex items-center gap-1.5">
                      <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                      </svg>
                      <span className="text-slate-600 dark:text-slate-300">{workspaceInfo.memberCount} Members</span>
                    </div>

                    {/* Creation Date */}
                    <div className="flex items-center gap-1.5">
                      <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                      </svg>
                      <span className="text-slate-600 dark:text-slate-300">Created on {workspaceInfo.createdDate}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Top-Right Action Buttons */}
              <div className="flex items-center gap-2.5 self-start">
                <button
                  onClick={() => setShowSettingsModal(true)}
                  className="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#182338] dark:hover:bg-[#202c46] text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-[#273655] transition-colors shadow-xs"
                >
                  <svg className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                    <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                  </svg>
                  <span>Workspace Settings</span>
                </button>

                <button
                  onClick={() => setShowInviteModal(true)}
                  className="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white shadow-sm shadow-violet-600/30 transition-all hover:shadow-md"
                >
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                  </svg>
                  <span>Invite Members</span>
                </button>
              </div>
            </div>

            {/* Quick Links Row */}
            <div className="mt-6 pt-5 border-t border-slate-100 dark:border-[#1a2339] flex flex-wrap items-center justify-between gap-4">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Quick Links</span>
              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={() => setActiveNav('Insights')}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs"
                >
                  <span className="w-2 h-2 rounded-full bg-violet-500"></span>
                  Insights
                </button>

                <button
                  onClick={() => setActiveNav('Feedback')}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs"
                >
                  <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                  Feedback
                </button>

                <button
                  onClick={() => setActiveNav('Features')}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs"
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                  Features
                </button>

                <button
                  onClick={() => setActiveNav('Roadmap')}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs"
                >
                  <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                  Roadmap
                </button>

                <button
                  onClick={() => setActiveNav('Reports')}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs"
                >
                  <span className="w-2 h-2 rounded-full bg-cyan-500"></span>
                  Reports
                </button>
              </div>
            </div>
          </section>

          {/* ========================================================
              METRICS CARDS GRID (5 Cards)
          ======================================================== */}
          <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {metrics.map((card) => (
              <div
                key={card.id}
                className="p-4 rounded-xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] flex items-center justify-between shadow-sm hover:border-slate-300 dark:hover:border-slate-700 transition-colors"
              >
                <div>
                  <p className="text-[11px] font-medium text-slate-500 dark:text-slate-400">{card.title}</p>
                  <h4 className="text-xl font-bold text-slate-900 dark:text-white mt-1">{card.value}</h4>
                  <p className={`text-[11px] font-medium ${card.trendColor} flex items-center gap-1 mt-1`}>
                    <span>{card.trend}</span>
                    <span className="text-slate-400 font-normal">{card.subtext}</span>
                  </p>
                </div>
                <div className={`h-10 w-10 rounded-xl flex items-center justify-center ${card.iconBox}`}>
                  {card.icon}
                </div>
              </div>
            ))}
          </section>

          {/* ========================================================
              2-COLUMN SPLIT: Activity on Left, Members & Sources on Right
          ======================================================== */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column (2 Cols): Recent Activity Table */}
            <section className="lg:col-span-2 rounded-2xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] p-6 shadow-sm flex flex-col justify-between">
              <div>
                {/* Header with 'View All Activity' */}
                <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-[#1a2339]">
                  <h3 className="font-bold text-slate-900 dark:text-white text-base">Recent Activity</h3>
                  <button
                    onClick={() => alert('Viewing all platform activity logs.')}
                    className="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 hover:underline"
                  >
                    View All Activity
                  </button>
                </div>

                {/* Activity Table Headers */}
                <div className="grid grid-cols-12 gap-2 py-3 px-2 text-[11px] font-semibold text-slate-400 dark:text-slate-400 uppercase tracking-wider">
                  <div className="col-span-5">Activity</div>
                  <div className="col-span-3">User</div>
                  <div className="col-span-2">Module</div>
                  <div className="col-span-2 text-right">Time</div>
                </div>

                {/* Activity Rows List */}
                <div className="divide-y divide-slate-100 dark:divide-[#182236] text-xs">
                  {filteredActivities.length === 0 ? (
                    <div className="py-8 text-center text-slate-400 text-xs">
                      No matching activities found for "{searchQuery}".
                    </div>
                  ) : (
                    filteredActivities.map((row) => (
                      <div
                        key={row.id}
                        className="grid grid-cols-12 gap-2 py-3.5 px-2 items-center hover:bg-slate-50/80 dark:hover:bg-[#162035] rounded-lg transition-colors"
                      >
                        {/* Activity Description */}
                        <div className="col-span-5 flex items-center gap-2.5 font-medium text-slate-800 dark:text-slate-200 truncate">
                          <span className={`p-1.5 rounded-lg flex-shrink-0 ${row.iconBg}`}>{row.icon}</span>
                          <span className="truncate">{row.activity}</span>
                        </div>

                        {/* User Column */}
                        <div className="col-span-3 flex items-center gap-2 text-slate-700 dark:text-slate-300">
                          {row.userType === 'ai' ? (
                            <div className="w-6 h-6 rounded-full bg-violet-100 dark:bg-violet-600/20 text-violet-600 dark:text-violet-400 flex items-center justify-center ring-1 ring-violet-200 dark:ring-violet-500/40 text-[10px] font-bold">
                              AI
                            </div>
                          ) : (
                            <div className={`w-6 h-6 rounded-full flex items-center justify-center ${row.avatarBg}`}>
                              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                                <path clipRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fillRule="evenodd" />
                              </svg>
                            </div>
                          )}
                          <span className={`truncate ${row.userType === 'ai' ? 'font-medium' : ''}`}>{row.user}</span>
                        </div>

                        {/* Module Tag */}
                        <div className="col-span-2">
                          <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${row.moduleBadge}`}>
                            {row.module}
                          </span>
                        </div>

                        {/* Time Column */}
                        <div className="col-span-2 text-right text-slate-400">{row.time}</div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </section>

            {/* Right Column (1 Col): Members List & Data Sources */}
            <div className="space-y-6">
              {/* Card: Members (12) */}
              <section className="p-6 rounded-2xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] shadow-sm">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-[#1a2339]">
                  <h3 className="font-bold text-slate-900 dark:text-white text-base">Members ({membersList.length + 7})</h3>
                  <button
                    onClick={() => alert('Viewing all workspace members.')}
                    className="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 hover:underline"
                  >
                    View All
                  </button>
                </div>

                {/* List of Members */}
                <div className="divide-y divide-slate-100 dark:divide-[#182236] text-xs">
                  {membersList.map((m, idx) => (
                    <div key={idx} className="py-3 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 rounded-full bg-gradient-to-tr ${m.gradient} text-white flex items-center justify-center font-bold text-xs ring-2 ${m.ring} shadow-xs`}>
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path clipRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fillRule="evenodd" />
                          </svg>
                        </div>
                        <div>
                          <p className="font-semibold text-slate-900 dark:text-slate-100">{m.name}</p>
                          <p className="text-[11px] text-slate-500 dark:text-slate-400">{m.role}</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] ${m.badgeClass}`}>{m.badge}</span>
                        <button
                          onClick={() => alert(`Manage settings for ${m.name}`)}
                          className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1"
                        >
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Card Action Footer: Invite Members */}
                <div className="mt-4 pt-3 border-t border-slate-100 dark:border-[#1a2339] text-center">
                  <button
                    onClick={() => setShowInviteModal(true)}
                    className="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 dark:hover:text-violet-300 flex items-center justify-center gap-1.5 w-full py-2 rounded-lg border border-dashed border-slate-300 dark:border-[#223150] hover:border-violet-400 hover:bg-violet-50/50 dark:hover:bg-transparent transition-colors"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path d="M12 4v16m8-8H4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                    </svg>
                    <span>Invite Members</span>
                  </button>
                </div>
              </section>

              {/* Card: Data Sources (8) */}
              <section className="p-6 rounded-2xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] shadow-sm">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-[#1a2339]">
                  <h3 className="font-bold text-slate-900 dark:text-white text-base">Data Sources ({dataSources.length})</h3>
                  <button
                    onClick={() => alert('Viewing all connected data sources.')}
                    className="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 hover:underline"
                  >
                    View All
                  </button>
                </div>

                {/* Source Items */}
                <div className="divide-y divide-slate-100 dark:divide-[#182236] text-xs">
                  {dataSources.map((ds, idx) => (
                    <div key={idx} className="py-2.5 flex items-center justify-between">
                      <div className="flex items-center gap-2.5">
                        <span className={`w-2.5 h-2.5 rounded-full ${ds.dotColor} shadow-xs`}></span>
                        <span className="text-slate-700 dark:text-slate-300 font-medium">{ds.name}</span>
                      </div>
                      <span className="font-semibold text-slate-900 dark:text-slate-100">{ds.count}</span>
                    </div>
                  ))}
                </div>

                {/* Footer Button: Add Data Source */}
                <div className="mt-4 pt-3 border-t border-slate-100 dark:border-[#1a2339] text-center">
                  <button
                    onClick={() => setShowAddSourceModal(true)}
                    className="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 dark:hover:text-violet-300 flex items-center justify-center gap-1.5 w-full py-2 rounded-lg border border-dashed border-slate-300 dark:border-[#223150] hover:border-violet-400 hover:bg-violet-50/50 dark:hover:bg-transparent transition-colors"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path d="M12 4v16m8-8H4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                    </svg>
                    <span>Add Data Source</span>
                  </button>
                </div>
              </section>
            </div>
          </div>
        </main>
      </div>

      {/* ========================================================
          MODAL 1: Create Workspace
      ======================================================== */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-white dark:bg-[#121929] border border-slate-200 dark:border-[#1c273e] rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-[#1a2339] pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">Create New Workspace</h3>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateWorkspace} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Workspace Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Mobile Banking App"
                  value={newWsName}
                  onChange={(e) => setNewWsName(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Description
                </label>
                <textarea
                  rows="3"
                  placeholder="Describe the product goals and data scope..."
                  value={newWsDesc}
                  onChange={(e) => setNewWsDesc(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
                ></textarea>
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-slate-100 dark:border-[#1a2339]">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white text-xs font-semibold shadow-sm"
                >
                  Create Workspace
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ========================================================
          MODAL 2: Invite Members
      ======================================================== */}
      {showInviteModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-[#121929] border border-slate-200 dark:border-[#1c273e] rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-[#1a2339] pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">Invite Team Member</h3>
              <button
                onClick={() => setShowInviteModal(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleInviteMember} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Email Address
                </label>
                <input
                  type="email"
                  required
                  placeholder="name@company.com"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Role</label>
                <select
                  value={inviteRole}
                  onChange={(e) => setInviteRole(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
                >
                  <option value="Member">Member</option>
                  <option value="Admin">Admin</option>
                  <option value="Owner">Owner</option>
                </select>
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-slate-100 dark:border-[#1a2339]">
                <button
                  type="button"
                  onClick={() => setShowInviteModal(false)}
                  className="px-4 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white text-xs font-semibold shadow-sm"
                >
                  Send Invite
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ========================================================
          MODAL 3: Add Data Source
      ======================================================== */}
      {showAddSourceModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-[#121929] border border-slate-200 dark:border-[#1c273e] rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-[#1a2339] pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">Add Data Source</h3>
              <button
                onClick={() => setShowAddSourceModal(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddSource} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Source Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Zendesk Tickets, Product Hunt Reviews"
                  value={newSourceName}
                  onChange={(e) => setNewSourceName(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Initial Item Count / Status
                </label>
                <input
                  type="text"
                  placeholder="e.g. 1,420"
                  value={newSourceCount}
                  onChange={(e) => setNewSourceCount(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-slate-100 dark:border-[#1a2339]">
                <button
                  type="button"
                  onClick={() => setShowAddSourceModal(false)}
                  className="px-4 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white text-xs font-semibold shadow-sm"
                >
                  Connect Source
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ========================================================
          MODAL 4: Workspace Settings
      ======================================================== */}
      {showSettingsModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-[#121929] border border-slate-200 dark:border-[#1c273e] rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-[#1a2339] pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">Workspace Settings</h3>
              <button
                onClick={() => setShowSettingsModal(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                ✕
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 rounded-lg bg-slate-50 dark:bg-[#0c1220] border border-slate-200 dark:border-[#1c273e]">
                <span className="font-semibold text-slate-700 dark:text-slate-300">Active Workspace:</span>{' '}
                <span className="text-violet-600 dark:text-violet-400 font-bold">{workspaceInfo.name}</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-50 dark:bg-[#0c1220] border border-slate-200 dark:border-[#1c273e]">
                <span className="font-semibold text-slate-700 dark:text-slate-300">Storage Plan:</span>{' '}
                <span className="text-slate-900 dark:text-white font-medium">Pro Tier (10 GB allocated, 7.8 GB used)</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-50 dark:bg-[#0c1220] border border-slate-200 dark:border-[#1c273e]">
                <span className="font-semibold text-slate-700 dark:text-slate-300">Owner Access:</span>{' '}
                <span className="text-emerald-600 dark:text-emerald-400 font-medium">Full Administrative Privileges</span>
              </div>
            </div>

            <div className="flex justify-end pt-2 border-t border-slate-100 dark:border-[#1a2339]">
              <button
                onClick={() => setShowSettingsModal(false)}
                className="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-700 text-white text-xs font-semibold shadow-sm"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
