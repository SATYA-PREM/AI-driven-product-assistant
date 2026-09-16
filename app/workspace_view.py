"""
workspace_view.py
-----------------
HTML View for the ProdIntel AI Workspaces Dashboard, matching the user's design.
Serves as an immediate preview endpoint at http://127.0.0.1:8000/workspaces
"""

from fastapi.responses import HTMLResponse

WORKSPACE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>ProdIntel AI - Workspaces Dashboard</title>
  <!-- Tailwind CSS v3 with Plugins -->
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#f5f3ff',
              100: '#ede9fe',
              500: '#8b5cf6',
              600: '#7c3aed',
              700: '#6d28d9',
            },
            darkBg: '#090d16',
            darkSurface: '#0f172a',
            darkCard: '#131b2e',
            darkBorder: '#1e293b',
            lightBg: '#f8fafc',
            lightSurface: '#ffffff',
            lightCard: '#ffffff',
            lightBorder: '#e2e8f0',
          },
          fontFamily: {
            sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
          }
        }
      }
    }
  </script>
  <!-- Google Fonts: Inter -->
  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
  <style data-purpose="custom-scrollbars">
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    .dark ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 9999px; }
    .dark ::-webkit-scrollbar-thumb:hover { background: #334155; }
  </style>
  <style data-purpose="theme-transitions">
    *, *::before, *::after {
      transition-property: background-color, border-color, color, fill, stroke;
      transition-duration: 200ms;
      transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    }
  </style>
</head>
<body class="bg-slate-50 dark:bg-darkBg text-slate-700 dark:text-slate-200 antialiased min-h-screen flex flex-col font-sans transition-colors duration-200">
  <div class="flex h-screen overflow-hidden">
    <!-- BEGIN: LeftSidebar -->
    <aside class="w-64 flex-shrink-0 bg-white dark:bg-[#0d1322] border-r border-slate-200 dark:border-[#1a2337] flex flex-col justify-between z-30 select-none shadow-[1px_0_4px_rgba(0,0,0,0.02)]" data-purpose="main-sidebar">
      <div class="flex flex-col h-full overflow-y-auto">
        <!-- Logo Header -->
        <div class="p-5 flex items-center gap-3 border-b border-slate-100 dark:border-[#172033]">
          <div class="h-9 w-9 rounded-xl bg-gradient-to-tr from-violet-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-violet-500/25 flex-shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24">
              <path d="M12 2a7 7 0 0 0-7 7c0 2.38 1.19 4.47 3 5.74V17a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-2.26c1.81-1.27 3-3.36 3-5.74a7 7 0 0 0-7-7M9 21h6"></path>
            </svg>
          </div>
          <div>
            <h1 class="font-bold text-base text-slate-900 dark:text-white leading-tight tracking-tight">ProdIntel AI</h1>
            <p class="text-[11px] font-medium text-slate-400 dark:text-slate-400 tracking-wide">Product Intelligence Platform</p>
          </div>
        </div>

        <!-- Primary Navigation Links -->
        <nav class="px-3 py-4 space-y-1" data-purpose="primary-navigation">
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="/">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            PM Dashboard
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="#">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            Insights
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="/">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            Feedback
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="#">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            Features
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="#">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            Prioritization
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="#">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            Requirements
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="#">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            Roadmap
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="#">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            Reports
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="#">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            AI Assistant
          </a>
          <!-- Section Divider: Workspace Sub-menu -->
          <div class="pt-5 pb-1">
            <span class="px-3 text-[10px] font-bold tracking-wider uppercase text-slate-400 dark:text-slate-400">Workspace</span>
          </div>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold bg-violet-50 text-violet-700 border border-violet-200/80 dark:bg-violet-600/20 dark:text-violet-300 dark:border-violet-500/20 shadow-xs" href="/workspaces">
            <svg class="w-4 h-4 text-violet-600 dark:text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
            Workspaces
          </a>
          <a class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100/80 dark:hover:bg-[#161f33] transition-colors" href="#" onclick="openSettingsModal()">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
            Settings
          </a>
        </nav>
      </div>

      <!-- Bottom Widget: Workspace Info, Storage, and User Profile -->
      <div class="p-3 border-t border-slate-200 dark:border-[#172033] space-y-3 bg-slate-50/50 dark:bg-transparent">
        <!-- Active Workspace Picker Pill -->
        <div onclick="openCreateModal()" class="p-2.5 rounded-lg bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] flex items-center justify-between cursor-pointer hover:border-violet-400 shadow-xs transition-colors">
          <div>
            <p class="text-[10px] text-slate-400 uppercase font-semibold">Current Workspace</p>
            <p class="text-xs font-semibold text-slate-800 dark:text-slate-100 truncate">E-Commerce Platform</p>
            <p class="text-[11px] text-slate-500 dark:text-slate-400">12 Members</p>
          </div>
          <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
        </div>

        <!-- Storage Progress Widget -->
        <div class="p-2.5 rounded-lg bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] shadow-xs">
          <div class="flex items-center justify-between text-xs mb-1.5">
            <span class="text-slate-600 dark:text-slate-400 font-medium">Storage</span>
            <span class="text-violet-600 dark:text-violet-400 font-bold">78%</span>
          </div>
          <div class="w-full bg-slate-100 dark:bg-[#202c46] h-1.5 rounded-full overflow-hidden">
            <div class="bg-gradient-to-r from-violet-600 to-indigo-600 h-full rounded-full" style="width: 78%"></div>
          </div>
          <div class="text-[10px] text-slate-500 dark:text-slate-400 mt-1 flex justify-between">
            <span>7.8 GB / 10 GB</span>
          </div>
        </div>

        <!-- User Profile Footer with humanoid avatar glyph -->
        <div class="pt-2 flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <div class="h-8 w-8 rounded-full bg-gradient-to-tr from-violet-600 to-fuchsia-600 flex items-center justify-center text-white ring-2 ring-violet-200 dark:ring-violet-400/30 shadow-xs">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path>
              </svg>
            </div>
            <div>
              <p class="text-xs font-semibold text-slate-900 dark:text-white leading-tight">Priya Sharma</p>
              <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium">Product Manager</p>
            </div>
          </div>
          <svg class="w-4 h-4 text-slate-400 cursor-pointer hover:text-slate-600 dark:hover:text-slate-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
        </div>
      </div>
    </aside>

    <!-- BEGIN: MainContentArea -->
    <div class="flex-1 flex flex-col min-w-0 overflow-y-auto bg-slate-50 dark:bg-darkBg">
      <!-- BEGIN: TopGlobalHeader -->
      <header class="sticky top-0 z-20 bg-white/95 dark:bg-[#090d16]/90 backdrop-blur border-b border-slate-200 dark:border-[#172033] px-8 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4 shadow-xs" data-purpose="top-global-header">
        <div>
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">Workspaces</h2>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Manage all your product workspaces in one place.</p>
        </div>
        <div class="flex items-center gap-3">
          <!-- Search Workspace Input -->
          <div class="relative w-64 md:w-72">
            <input class="w-full bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-[#222e47] rounded-lg pl-9 pr-3 py-2 text-xs text-slate-900 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 transition-all shadow-xs" placeholder="Search workspaces..." type="text"/>
            <svg class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          </div>
          <!-- Interactive Light / Dark Mode Toggle Switch -->
          <button aria-label="Toggle Light and Dark mode" class="p-2 rounded-lg bg-white dark:bg-[#141b2c] border border-slate-200 dark:border-[#243048] text-amber-500 dark:text-slate-300 hover:text-amber-600 dark:hover:text-violet-400 hover:border-slate-300 dark:hover:border-violet-400/40 shadow-xs transition-colors flex items-center justify-center" data-purpose="theme-toggle-button" id="themeToggleBtn" title="Switch Theme">
            <!-- Moon Icon (shown when dark) -->
            <svg class="w-4 h-4 hidden dark:block text-slate-300" fill="none" id="moonIcon" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
            </svg>
            <!-- Sun Icon (shown when in light mode) -->
            <svg class="w-4 h-4 block dark:hidden text-amber-500" fill="none" id="sunIcon" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
            </svg>
          </button>
          <!-- Notification Bell with Count Badge -->
          <div class="relative">
            <button class="p-2 rounded-lg bg-white dark:bg-[#141b2c] border border-slate-200 dark:border-[#243048] text-slate-600 dark:text-slate-300 hover:text-violet-600 dark:hover:text-violet-400 hover:border-slate-300 transition-colors shadow-xs">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
            </button>
            <span class="absolute -top-1 -right-1 h-4 w-4 bg-rose-500 text-white font-bold text-[10px] rounded-full flex items-center justify-center ring-2 ring-white dark:ring-darkBg">8</span>
          </div>
          <!-- Help / Support Icon Button -->
          <button class="p-2 rounded-lg bg-white dark:bg-[#141b2c] border border-slate-200 dark:border-[#243048] text-slate-600 dark:text-slate-300 hover:text-violet-600 dark:hover:text-violet-400 hover:border-slate-300 transition-colors shadow-xs">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
          </button>
          <!-- Primary CTA Button -->
          <button onclick="openCreateModal()" class="flex items-center gap-1.5 px-3.5 py-2 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white text-xs font-semibold rounded-lg shadow-sm shadow-violet-600/30 transition-all hover:shadow-md hover:shadow-violet-600/40">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
            <span>Create Workspace</span>
          </button>
        </div>
      </header>

      <!-- Scrollable Main Content Container -->
      <main class="p-8 space-y-6 flex-1">
        <!-- BEGIN: WorkspaceBannerCard -->
        <section class="p-6 rounded-2xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] shadow-sm" data-purpose="workspace-hero-banner">
          <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
            <!-- Left Info Block -->
            <div class="flex items-start gap-4">
              <!-- Cart Workspace Icon Badge -->
              <div class="h-14 w-14 rounded-2xl bg-gradient-to-br from-violet-600 to-purple-600 flex items-center justify-center text-white shadow-md shadow-violet-600/25 flex-shrink-0 ring-4 ring-violet-50 dark:ring-transparent">
                <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
              </div>
              <!-- Workspace Details -->
              <div class="space-y-2">
                <div class="flex items-center gap-3">
                  <h3 class="text-xl font-bold text-slate-900 dark:text-white">E-Commerce Platform</h3>
                  <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-violet-50 text-violet-700 dark:bg-violet-950 dark:text-violet-300 border border-violet-200 dark:border-violet-700">Active</span>
                </div>
                <p class="text-xs text-slate-600 dark:text-slate-400 max-w-2xl leading-relaxed">
                  Central workspace for analyzing customer feedback, discovering insights, and building better e-commerce experiences.
                </p>
                <!-- Metadata Row -->
                <div class="flex flex-wrap items-center gap-6 pt-1 text-xs text-slate-500 dark:text-slate-400">
                  <div class="flex items-center gap-2">
                    <div class="w-5 h-5 rounded-full bg-violet-600 text-white flex items-center justify-center text-[10px] shadow-xs">
                      <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <span><strong class="text-slate-800 dark:text-slate-200">Priya Sharma</strong> (You) <span class="text-slate-400">· Workspace Owner</span></span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                    <span class="text-slate-600 dark:text-slate-300">12 Members</span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                    <span class="text-slate-600 dark:text-slate-300">Created on Aug 01, 2025</span>
                  </div>
                </div>
              </div>
            </div>
            <!-- Top-Right Action Buttons -->
            <div class="flex items-center gap-2.5 self-start">
              <button onclick="openSettingsModal()" class="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#182338] dark:hover:bg-[#202c46] text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-[#273655] transition-colors shadow-xs">
                <svg class="w-3.5 h-3.5 text-slate-500 dark:text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
                <span>Workspace Settings</span>
              </button>
              <button onclick="openInviteModal()" class="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white shadow-sm shadow-violet-600/30 transition-all hover:shadow-md">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
                <span>Invite Members</span>
              </button>
            </div>
          </div>
          <!-- Quick Links Row -->
          <div class="mt-6 pt-5 border-t border-slate-100 dark:border-[#1a2339] flex flex-wrap items-center justify-between gap-4">
            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">Quick Links</span>
            <div class="flex flex-wrap items-center gap-2">
              <a class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs" href="#">
                <span class="w-2 h-2 rounded-full bg-violet-500"></span>
                Insights
              </a>
              <a class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs" href="/">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                Feedback
              </a>
              <a class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs" href="#">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                Features
              </a>
              <a class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs" href="#">
                <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                Roadmap
              </a>
              <a class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-[#162035] dark:hover:bg-[#1d2b47] border border-slate-200/90 dark:border-[#223150] text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors shadow-2xs" href="#">
                <span class="w-2 h-2 rounded-full bg-cyan-500"></span>
                Reports
              </a>
            </div>
          </div>
        </section>

        <!-- BEGIN: MetricsCardsGrid -->
        <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4" data-purpose="metrics-summary-grid">
          <!-- Card 1: Total Feedback -->
          <div class="p-4 rounded-xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] flex items-center justify-between shadow-sm hover:border-slate-300 transition-colors">
            <div>
              <p class="text-[11px] font-medium text-slate-500 dark:text-slate-400">Total Feedback</p>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">12,842</h4>
              <p class="text-[11px] font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1 mt-1">
                <span>↑ 18.6%</span>
                <span class="text-slate-400 font-normal">vs last 30 days</span>
              </p>
            </div>
            <div class="h-10 w-10 rounded-xl bg-purple-50 dark:bg-purple-500/20 text-purple-600 dark:text-purple-400 border border-purple-100 dark:border-purple-500/30 flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            </div>
          </div>
          <!-- Card 2: Total Features -->
          <div class="p-4 rounded-xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] flex items-center justify-between shadow-sm hover:border-slate-300 transition-colors">
            <div>
              <p class="text-[11px] font-medium text-slate-500 dark:text-slate-400">Total Features</p>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">56</h4>
              <p class="text-[11px] font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1 mt-1">
                <span>↑ 12.0%</span>
                <span class="text-slate-400 font-normal">vs last 30 days</span>
              </p>
            </div>
            <div class="h-10 w-10 rounded-xl bg-blue-50 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-500/30 flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 6h16M4 10h16M4 14h16M4 18h16" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            </div>
          </div>
          <!-- Card 3: Insights Generated -->
          <div class="p-4 rounded-xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] flex items-center justify-between shadow-sm hover:border-slate-300 transition-colors">
            <div>
              <p class="text-[11px] font-medium text-slate-500 dark:text-slate-400">Insights Generated</p>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">128</h4>
              <p class="text-[11px] font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1 mt-1">
                <span>↑ 15.7%</span>
                <span class="text-slate-400 font-normal">vs last 30 days</span>
              </p>
            </div>
            <div class="h-10 w-10 rounded-xl bg-emerald-50 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-500/30 flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            </div>
          </div>
          <!-- Card 4: Active Members -->
          <div class="p-4 rounded-xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] flex items-center justify-between shadow-sm hover:border-slate-300 transition-colors">
            <div>
              <p class="text-[11px] font-medium text-slate-500 dark:text-slate-400">Active Members</p>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">12</h4>
              <p class="text-[11px] font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1 mt-1">
                <span>↑ 20.0%</span>
                <span class="text-slate-400 font-normal">vs last 30 days</span>
              </p>
            </div>
            <div class="h-10 w-10 rounded-xl bg-amber-50 dark:bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-100 dark:border-amber-500/30 flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            </div>
          </div>
          <!-- Card 5: Data Sources -->
          <div class="p-4 rounded-xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] flex items-center justify-between shadow-sm hover:border-slate-300 transition-colors">
            <div>
              <p class="text-[11px] font-medium text-slate-500 dark:text-slate-400">Data Sources</p>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">8</h4>
              <p class="text-[11px] font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1 mt-1">
                <span>↑ 2 new</span>
                <span class="text-slate-400 font-normal">vs last 30 days</span>
              </p>
            </div>
            <div class="h-10 w-10 rounded-xl bg-cyan-50 dark:bg-cyan-500/20 text-cyan-600 dark:text-cyan-400 border border-cyan-100 dark:border-cyan-500/30 flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
            </div>
          </div>
        </section>

        <!-- BEGIN: MainContentTwoColumnSplit -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Left Column (2 Cols): Recent Activity Table -->
          <section class="lg:col-span-2 rounded-2xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] p-6 shadow-sm flex flex-col justify-between" data-purpose="recent-activity-section">
            <div>
              <div class="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-[#1a2339]">
                <h3 class="font-bold text-slate-900 dark:text-white text-base">Recent Activity</h3>
                <a class="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 hover:underline" href="#">View All Activity</a>
              </div>
              <div class="grid grid-cols-12 gap-2 py-3 px-2 text-[11px] font-semibold text-slate-400 dark:text-slate-400 uppercase tracking-wider">
                <div class="col-span-5">Activity</div>
                <div class="col-span-3">User</div>
                <div class="col-span-2">Module</div>
                <div class="col-span-2 text-right">Time</div>
              </div>
              <div class="divide-y divide-slate-100 dark:divide-[#182236] text-xs">
                <!-- Row 1 -->
                <div class="grid grid-cols-12 gap-2 py-3.5 px-2 items-center hover:bg-slate-50/80 dark:hover:bg-[#162035] rounded-lg transition-colors">
                  <div class="col-span-5 flex items-center gap-2.5 font-medium text-slate-800 dark:text-slate-200 truncate">
                    <span class="p-1.5 rounded-lg bg-purple-50 text-purple-600 dark:bg-purple-500/10 dark:text-purple-400 border border-purple-100 dark:border-transparent flex-shrink-0">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                    </span>
                    <span class="truncate">Added 320 new feedback items</span>
                  </div>
                  <div class="col-span-3 flex items-center gap-2 text-slate-700 dark:text-slate-300">
                    <div class="w-6 h-6 rounded-full bg-pink-100 dark:bg-pink-600/20 text-pink-600 dark:text-pink-400 flex items-center justify-center ring-1 ring-pink-200 dark:ring-pink-500/30">
                      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <span class="truncate">Priya Sharma</span>
                  </div>
                  <div class="col-span-2">
                    <span class="px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-100 dark:border-transparent dark:bg-blue-900/30 dark:text-blue-400">Feedback</span>
                  </div>
                  <div class="col-span-2 text-right text-slate-400">2 hours ago</div>
                </div>
                <!-- Row 2 -->
                <div class="grid grid-cols-12 gap-2 py-3.5 px-2 items-center hover:bg-slate-50/80 dark:hover:bg-[#162035] rounded-lg transition-colors">
                  <div class="col-span-5 flex items-center gap-2.5 font-medium text-slate-800 dark:text-slate-200 truncate">
                    <span class="p-1.5 rounded-lg bg-emerald-50 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-400 border border-emerald-100 dark:border-transparent flex-shrink-0">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                    </span>
                    <span class="truncate">AI generated 15 new insights</span>
                  </div>
                  <div class="col-span-3 flex items-center gap-2 text-slate-700 dark:text-slate-300">
                    <div class="w-6 h-6 rounded-full bg-violet-100 dark:bg-violet-600/20 text-violet-600 dark:text-violet-400 flex items-center justify-center ring-1 ring-violet-200 dark:ring-violet-500/40 text-[10px] font-bold">
                      AI
                    </div>
                    <span class="truncate font-medium">AI Assistant</span>
                  </div>
                  <div class="col-span-2">
                    <span class="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-100 dark:border-transparent dark:bg-emerald-900/30 dark:text-emerald-400">Insights</span>
                  </div>
                  <div class="col-span-2 text-right text-slate-400">3 hours ago</div>
                </div>
                <!-- Row 3 -->
                <div class="grid grid-cols-12 gap-2 py-3.5 px-2 items-center hover:bg-slate-50/80 dark:hover:bg-[#162035] rounded-lg transition-colors">
                  <div class="col-span-5 flex items-center gap-2.5 font-medium text-slate-800 dark:text-slate-200 truncate">
                    <span class="p-1.5 rounded-lg bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-400 border border-blue-100 dark:border-transparent flex-shrink-0">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
                    </span>
                    <span class="truncate">Created feature "One-click checkout"</span>
                  </div>
                  <div class="col-span-3 flex items-center gap-2 text-slate-700 dark:text-slate-300">
                    <div class="w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-600/20 text-blue-600 dark:text-blue-500 flex items-center justify-center ring-1 ring-blue-200 dark:ring-blue-500/30">
                      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <span class="truncate">Arjun Mehta</span>
                  </div>
                  <div class="col-span-2">
                    <span class="px-2 py-0.5 rounded text-[11px] font-medium bg-cyan-50 text-cyan-700 border border-cyan-100 dark:border-transparent dark:bg-cyan-900/30 dark:text-cyan-400">Features</span>
                  </div>
                  <div class="col-span-2 text-right text-slate-400">5 hours ago</div>
                </div>
                <!-- Row 4 -->
                <div class="grid grid-cols-12 gap-2 py-3.5 px-2 items-center hover:bg-slate-50/80 dark:hover:bg-[#162035] rounded-lg transition-colors">
                  <div class="col-span-5 flex items-center gap-2.5 font-medium text-slate-800 dark:text-slate-200 truncate">
                    <span class="p-1.5 rounded-lg bg-amber-50 text-amber-600 dark:bg-amber-500/10 dark:text-amber-400 border border-amber-100 dark:border-transparent flex-shrink-0">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
                    </span>
                    <span class="truncate">Updated priority for 3 features</span>
                  </div>
                  <div class="col-span-3 flex items-center gap-2 text-slate-700 dark:text-slate-300">
                    <div class="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-600/20 text-emerald-600 dark:text-emerald-500 flex items-center justify-center ring-1 ring-emerald-200 dark:ring-emerald-500/30">
                      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <span class="truncate">Neha Kapoor</span>
                  </div>
                  <div class="col-span-2">
                    <span class="px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-100 dark:border-transparent dark:bg-amber-900/30 dark:text-amber-400">Prioritization</span>
                  </div>
                  <div class="col-span-2 text-right text-slate-400">1 day ago</div>
                </div>
                <!-- Row 5 -->
                <div class="grid grid-cols-12 gap-2 py-3.5 px-2 items-center hover:bg-slate-50/80 dark:hover:bg-[#162035] rounded-lg transition-colors">
                  <div class="col-span-5 flex items-center gap-2.5 font-medium text-slate-800 dark:text-slate-200 truncate">
                    <span class="p-1.5 rounded-lg bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400 border border-indigo-100 dark:border-transparent flex-shrink-0">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
                    </span>
                    <span class="truncate">Added 2 new requirements</span>
                  </div>
                  <div class="col-span-3 flex items-center gap-2 text-slate-700 dark:text-slate-300">
                    <div class="w-6 h-6 rounded-full bg-teal-100 dark:bg-teal-600/20 text-teal-600 dark:text-teal-500 flex items-center justify-center ring-1 ring-teal-200 dark:ring-teal-500/30">
                      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <span class="truncate">Rohit Singh</span>
                  </div>
                  <div class="col-span-2">
                    <span class="px-2 py-0.5 rounded text-[11px] font-medium bg-indigo-50 text-indigo-700 border border-indigo-100 dark:border-transparent dark:bg-indigo-900/30 dark:text-indigo-400">Requirements</span>
                  </div>
                  <div class="col-span-2 text-right text-slate-400">1 day ago</div>
                </div>
                <!-- Row 6 -->
                <div class="grid grid-cols-12 gap-2 py-3.5 px-2 items-center hover:bg-slate-50/80 dark:hover:bg-[#162035] rounded-lg transition-colors">
                  <div class="col-span-5 flex items-center gap-2.5 font-medium text-slate-800 dark:text-slate-200 truncate">
                    <span class="p-1.5 rounded-lg bg-rose-50 text-rose-600 dark:bg-rose-500/10 dark:text-rose-400 border border-rose-100 dark:border-transparent flex-shrink-0">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
                    </span>
                    <span class="truncate">Updated roadmap timeline</span>
                  </div>
                  <div class="col-span-3 flex items-center gap-2 text-slate-700 dark:text-slate-300">
                    <div class="w-6 h-6 rounded-full bg-pink-100 dark:bg-pink-600/20 text-pink-600 dark:text-pink-500 flex items-center justify-center ring-1 ring-pink-200 dark:ring-pink-500/30">
                      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <span class="truncate">Priya Sharma</span>
                  </div>
                  <div class="col-span-2">
                    <span class="px-2 py-0.5 rounded text-[11px] font-medium bg-rose-50 text-rose-700 border border-rose-100 dark:border-transparent dark:bg-rose-900/30 dark:text-rose-400">Roadmap</span>
                  </div>
                  <div class="col-span-2 text-right text-slate-400">2 days ago</div>
                </div>
                <!-- Row 7 -->
                <div class="grid grid-cols-12 gap-2 py-3.5 px-2 items-center hover:bg-slate-50/80 dark:hover:bg-[#162035] rounded-lg transition-colors">
                  <div class="col-span-5 flex items-center gap-2.5 font-medium text-slate-800 dark:text-slate-200 truncate">
                    <span class="p-1.5 rounded-lg bg-cyan-50 text-cyan-600 dark:bg-cyan-500/10 dark:text-cyan-400 border border-cyan-100 dark:border-transparent flex-shrink-0">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path></svg>
                    </span>
                    <span class="truncate">Generated Feedback Summary Report</span>
                  </div>
                  <div class="col-span-3 flex items-center gap-2 text-slate-700 dark:text-slate-300">
                    <div class="w-6 h-6 rounded-full bg-violet-100 dark:bg-violet-600/20 text-violet-600 dark:text-violet-400 flex items-center justify-center ring-1 ring-violet-200 dark:ring-violet-500/40 text-[10px] font-bold">
                      AI
                    </div>
                    <span class="truncate font-medium">AI Assistant</span>
                  </div>
                  <div class="col-span-2">
                    <span class="px-2 py-0.5 rounded text-[11px] font-medium bg-purple-50 text-purple-700 border border-purple-100 dark:border-transparent dark:bg-purple-900/30 dark:text-purple-400">Reports</span>
                  </div>
                  <div class="col-span-2 text-right text-slate-400">2 days ago</div>
                </div>
              </div>
            </div>
          </section>

          <!-- Right Column (1 Col): Members List & Data Sources -->
          <div class="space-y-6">
            <!-- Card: Members (12) -->
            <section class="p-6 rounded-2xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] shadow-sm" data-purpose="members-list-card">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-[#1a2339]">
                <h3 class="font-bold text-slate-900 dark:text-white text-base">Members (12)</h3>
                <a class="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 hover:underline" href="#">View All</a>
              </div>
              <div class="divide-y divide-slate-100 dark:divide-[#182236] text-xs">
                <!-- Member 1 -->
                <div class="py-3 flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-pink-500 to-rose-500 text-white flex items-center justify-center font-bold text-xs ring-2 ring-pink-100 dark:ring-pink-500/20 shadow-xs">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <div>
                      <p class="font-semibold text-slate-900 dark:text-slate-100">Priya Sharma</p>
                      <p class="text-[11px] text-slate-500 dark:text-slate-400">Product Manager (Owner)</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-violet-100 text-violet-700 border border-violet-200/60 dark:border-transparent dark:bg-violet-950 dark:text-violet-300">Owner</span>
                    <button class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path></svg>
                    </button>
                  </div>
                </div>
                <!-- Member 2 -->
                <div class="py-3 flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-500 text-white flex items-center justify-center font-bold text-xs ring-2 ring-blue-100 dark:ring-blue-500/20 shadow-xs">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <div>
                      <p class="font-semibold text-slate-900 dark:text-slate-100">Arjun Mehta</p>
                      <p class="text-[11px] text-slate-500 dark:text-slate-400">Product Analyst</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-100 text-blue-700 border border-blue-200/60 dark:border-transparent dark:bg-blue-950 dark:text-blue-300">Admin</span>
                    <button class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path></svg>
                    </button>
                  </div>
                </div>
                <!-- Member 3 -->
                <div class="py-3 flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-emerald-500 to-teal-500 text-white flex items-center justify-center font-bold text-xs ring-2 ring-emerald-100 dark:ring-emerald-500/20 shadow-xs">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <div>
                      <p class="font-semibold text-slate-900 dark:text-slate-100">Neha Kapoor</p>
                      <p class="text-[11px] text-slate-500 dark:text-slate-400">UX Designer</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600 border border-slate-200 dark:border-transparent dark:bg-[#182338] dark:text-slate-300">Member</span>
                    <button class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path></svg>
                    </button>
                  </div>
                </div>
                <!-- Member 4 -->
                <div class="py-3 flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-amber-500 to-orange-500 text-white flex items-center justify-center font-bold text-xs ring-2 ring-amber-100 dark:ring-amber-500/20 shadow-xs">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <div>
                      <p class="font-semibold text-slate-900 dark:text-slate-100">Rohit Singh</p>
                      <p class="text-[11px] text-slate-500 dark:text-slate-400">Data Analyst</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600 border border-slate-200 dark:border-transparent dark:bg-[#182338] dark:text-slate-300">Member</span>
                    <button class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path></svg>
                    </button>
                  </div>
                </div>
                <!-- Member 5 -->
                <div class="py-3 flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-cyan-500 to-sky-500 text-white flex items-center justify-center font-bold text-xs ring-2 ring-cyan-100 dark:ring-cyan-500/20 shadow-xs">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path clip-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" fill-rule="evenodd"></path></svg>
                    </div>
                    <div>
                      <p class="font-semibold text-slate-900 dark:text-slate-100">Ananya Das</p>
                      <p class="text-[11px] text-slate-500 dark:text-slate-400">QA Engineer</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600 border border-slate-200 dark:border-transparent dark:bg-[#182338] dark:text-slate-300">Member</span>
                    <button class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path></svg>
                    </button>
                  </div>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-100 dark:border-[#1a2339] text-center">
                <button onclick="openInviteModal()" class="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 dark:hover:text-violet-300 flex items-center justify-center gap-1.5 w-full py-2 rounded-lg border border-dashed border-slate-300 dark:border-[#223150] hover:border-violet-400 hover:bg-violet-50/50 dark:hover:bg-transparent transition-colors">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                  <span>Invite Members</span>
                </button>
              </div>
            </section>

            <!-- Card: Data Sources (8) -->
            <section class="p-6 rounded-2xl bg-white dark:bg-[#121929] border border-slate-200/90 dark:border-[#1c273e] shadow-sm" data-purpose="data-sources-card">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-[#1a2339]">
                <h3 class="font-bold text-slate-900 dark:text-white text-base">Data Sources (8)</h3>
                <a class="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 hover:underline" href="#">View All</a>
              </div>
              <div class="divide-y divide-slate-100 dark:divide-[#182236] text-xs">
                <div class="py-2.5 flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-blue-500 shadow-xs"></span>
                    <span class="text-slate-700 dark:text-slate-300 font-medium">User Interviews</span>
                  </div>
                  <span class="font-semibold text-slate-900 dark:text-slate-100">1,245</span>
                </div>
                <div class="py-2.5 flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-purple-500 shadow-xs"></span>
                    <span class="text-slate-700 dark:text-slate-300 font-medium">Surveys</span>
                  </div>
                  <span class="font-semibold text-slate-900 dark:text-slate-100">1,240</span>
                </div>
                <div class="py-2.5 flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-cyan-500 shadow-xs"></span>
                    <span class="text-slate-700 dark:text-slate-300 font-medium">Support Tickets</span>
                  </div>
                  <span class="font-semibold text-slate-900 dark:text-slate-100">3,642</span>
                </div>
                <div class="py-2.5 flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-indigo-500 shadow-xs"></span>
                    <span class="text-slate-700 dark:text-slate-300 font-medium">Social Media</span>
                  </div>
                  <span class="font-semibold text-slate-900 dark:text-slate-100">1,098</span>
                </div>
                <div class="py-2.5 flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-xs"></span>
                    <span class="text-slate-700 dark:text-slate-300 font-medium">App Store Reviews</span>
                  </div>
                  <span class="font-semibold text-slate-900 dark:text-slate-100">2,185</span>
                </div>
                <div class="py-2.5 flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-sky-500 shadow-xs"></span>
                    <span class="text-slate-700 dark:text-slate-300 font-medium">Email Feedback</span>
                  </div>
                  <span class="font-semibold text-slate-900 dark:text-slate-100">956</span>
                </div>
                <div class="py-2.5 flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-xs"></span>
                    <span class="text-slate-700 dark:text-slate-300 font-medium">Play Store Reviews</span>
                  </div>
                  <span class="font-semibold text-slate-900 dark:text-slate-100">1,876</span>
                </div>
                <div class="py-2.5 flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-amber-500 shadow-xs"></span>
                    <span class="text-slate-700 dark:text-slate-300 font-medium">Internal Notes</span>
                  </div>
                  <span class="font-semibold text-slate-900 dark:text-slate-100">600</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-100 dark:border-[#1a2339] text-center">
                <button onclick="openAddSourceModal()" class="text-xs font-semibold text-violet-600 dark:text-violet-400 hover:text-violet-700 dark:hover:text-violet-300 flex items-center justify-center gap-1.5 w-full py-2 rounded-lg border border-dashed border-slate-300 dark:border-[#223150] hover:border-violet-400 hover:bg-violet-50/50 dark:hover:bg-transparent transition-colors">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                  <span>Add Data Source</span>
                </button>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  </div>

  <!-- MODAL: Create Workspace -->
  <div id="createModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white dark:bg-[#121929] border border-slate-200 dark:border-[#1c273e] rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-[#1a2339] pb-3">
        <h3 class="text-base font-bold text-slate-900 dark:text-white">Create New Workspace</h3>
        <button onclick="closeModal('createModal')" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">✕</button>
      </div>
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Workspace Name</label>
          <input id="wsNameInput" type="text" placeholder="e.g. Mobile Banking App" class="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500" />
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Description</label>
          <textarea id="wsDescInput" rows="3" placeholder="Describe the workspace..." class="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"></textarea>
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t border-slate-100 dark:border-[#1a2339]">
          <button onclick="closeModal('createModal')" class="px-4 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">Cancel</button>
          <button onclick="submitNewWorkspace()" class="px-4 py-2 rounded-lg bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white text-xs font-semibold shadow-sm">Create Workspace</button>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL: Invite Members -->
  <div id="inviteModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white dark:bg-[#121929] border border-slate-200 dark:border-[#1c273e] rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-[#1a2339] pb-3">
        <h3 class="text-base font-bold text-slate-900 dark:text-white">Invite Team Member</h3>
        <button onclick="closeModal('inviteModal')" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">✕</button>
      </div>
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Email Address</label>
          <input id="inviteEmailInput" type="email" placeholder="name@company.com" class="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500" />
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Role</label>
          <select id="inviteRoleSelect" class="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] bg-slate-50 dark:bg-[#0c1220] text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500">
            <option>Member</option>
            <option>Admin</option>
            <option>Owner</option>
          </select>
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t border-slate-100 dark:border-[#1a2339]">
          <button onclick="closeModal('inviteModal')" class="px-4 py-2 rounded-lg border border-slate-200 dark:border-[#1c273e] text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">Cancel</button>
          <button onclick="submitInvite()" class="px-4 py-2 rounded-lg bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white text-xs font-semibold shadow-sm">Send Invite</button>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL: Settings -->
  <div id="settingsModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white dark:bg-[#121929] border border-slate-200 dark:border-[#1c273e] rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-[#1a2339] pb-3">
        <h3 class="text-base font-bold text-slate-900 dark:text-white">Workspace Settings</h3>
        <button onclick="closeModal('settingsModal')" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">✕</button>
      </div>
      <div class="space-y-3 text-xs">
        <div class="p-3 rounded-lg bg-slate-50 dark:bg-[#0c1220] border border-slate-200 dark:border-[#1c273e]">
          <span class="font-semibold text-slate-700 dark:text-slate-300">Active Workspace:</span>
          <span class="text-violet-600 dark:text-violet-400 font-bold ml-1">E-Commerce Platform</span>
        </div>
        <div class="p-3 rounded-lg bg-slate-50 dark:bg-[#0c1220] border border-slate-200 dark:border-[#1c273e]">
          <span class="font-semibold text-slate-700 dark:text-slate-300">Storage Plan:</span>
          <span class="text-slate-900 dark:text-white font-medium ml-1">Pro Tier (10 GB allocated, 7.8 GB used)</span>
        </div>
        <div class="p-3 rounded-lg bg-slate-50 dark:bg-[#0c1220] border border-slate-200 dark:border-[#1c273e]">
          <span class="font-semibold text-slate-700 dark:text-slate-300">Owner Access:</span>
          <span class="text-emerald-600 dark:text-emerald-400 font-medium ml-1">Full Administrative Privileges</span>
        </div>
      </div>
      <div class="flex justify-end pt-2 border-t border-slate-100 dark:border-[#1a2339]">
        <button onclick="closeModal('settingsModal')" class="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-700 text-white text-xs font-semibold shadow-sm">Done</button>
      </div>
    </div>
  </div>

  <script data-purpose="theme-toggle-script">
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const htmlElement = document.documentElement;

    themeToggleBtn.addEventListener('click', () => {
      const isDark = htmlElement.classList.toggle('dark');
      try {
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
      } catch (e) {}
    });

    try {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'dark') {
        htmlElement.classList.add('dark');
      } else if (savedTheme === 'light') {
        htmlElement.classList.remove('dark');
      }
    } catch(e) {}

    function openCreateModal() {
      document.getElementById('createModal').classList.remove('hidden');
    }
    function openInviteModal() {
      document.getElementById('inviteModal').classList.remove('hidden');
    }
    function openSettingsModal() {
      document.getElementById('settingsModal').classList.remove('hidden');
    }
    function openAddSourceModal() {
      alert('Connecting new data source (Zendesk, Salesforce, App Stores, etc.)');
    }
    function closeModal(id) {
      document.getElementById(id).classList.add('hidden');
    }
    function submitNewWorkspace() {
      const name = document.getElementById('wsNameInput').value;
      alert(`Workspace "${name || 'New Workspace'}" created successfully!`);
      closeModal('createModal');
    }
    function submitInvite() {
      const email = document.getElementById('inviteEmailInput').value;
      const role = document.getElementById('inviteRoleSelect').value;
      alert(`Invited ${email || 'colleague'} as ${role}!`);
      closeModal('inviteModal');
    }
  </script>
</body>
</html>
"""

def get_workspace_dashboard() -> HTMLResponse:
    return HTMLResponse(content=WORKSPACE_HTML)
