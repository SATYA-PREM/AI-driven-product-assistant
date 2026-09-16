import { useState, useEffect } from 'react';
import {
  BarChart2,
  Brain,
  ChevronLeft,
  ChevronRight,
  FileText,
  Lightbulb,
  LayoutDashboard,
  LayoutGrid,
  Map,
  MessageSquare,
  Settings,
  Sparkles,
  Star,
  Users,
} from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { getStoredWorkspaces } from '../../utils/workspaceAccess';

export default function Sidebar({ workspaceId: propWorkspaceId }) {
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isInsightsOpen, setIsInsightsOpen] = useState(false);
  const [isFeedbackOpen, setIsFeedbackOpen] = useState(false);

  const workspaces = getStoredWorkspaces();
  const activeWorkspace = workspaces.find((ws) => ws.id === propWorkspaceId) || workspaces[0] || {
    id: 'ecommerce-platform',
    name: 'E-Commerce Platform',
    membersCount: 12
  };

  const wsId = propWorkspaceId || activeWorkspace.id;
  const basePath = `/workspace/${wsId}`;

  // Automatically open accordion menus if current route matches
  useEffect(() => {
    if (location.pathname.includes('/intelligence/insights')) {
      setIsInsightsOpen(true);
    }
    if (location.pathname.includes('/intelligence/feedback')) {
      setIsFeedbackOpen(true);
    }
  }, [location.pathname]);

  const isActive = (path) => location.pathname === path;
  
  const isInsightsActive = location.pathname.includes('/intelligence/insights');
  const isFeedbackActive = location.pathname.includes('/intelligence/feedback');

  const isHashActive = (hash) => location.hash === hash || (location.hash === '' && hash === '#Overview');

  const feedbackSubItems = [
    { label: 'All Feedback', path: `${basePath}/intelligence/feedback/all` },
    { label: 'My Feedback', path: `${basePath}/intelligence/feedback/my` },
    { label: 'Unresolved', path: `${basePath}/intelligence/feedback/unresolved` },
    { label: 'Resolved', path: `${basePath}/intelligence/feedback/resolved` },
    { label: 'Snoozed', path: `${basePath}/intelligence/feedback/snoozed` },
  ];

  const navItems = [
    { icon: LayoutGrid, label: 'Features', path: `${basePath}/intelligence/features` },
    { icon: Star, label: 'Prioritization', path: `${basePath}/development/phases` },
    { icon: FileText, label: 'Requirements (PRDs)', path: `${basePath}/development/validation` },
    { icon: Map, label: 'Roadmap', path: `${basePath}/development/tasks` },
    { icon: BarChart2, label: 'Reports', path: `${basePath}/reports` },
    { icon: Sparkles, label: 'AI Assistant', path: `${basePath}/assistant` },
    { icon: Users, label: 'Workspace Members', path: '/workspaces' },
    { icon: Settings, label: 'Settings', path: '/profile' },
  ];

  const insightSubItems = [
    { label: 'Overview', hash: '#Overview' },
    { label: 'Pain Points', hash: '#PainPoints' },
    { label: 'Trends', hash: '#Trends' },
    { label: 'Themes', hash: '#Themes' },
    { label: 'Sentiment', hash: '#Sentiment' },
    { label: 'Segments', hash: '#Segments' },
    { label: 'Comparisons', hash: '#Comparisons' },
  ];

  return (
    <aside className={`${isCollapsed ? 'w-[74px]' : 'w-[250px]'} h-screen bg-[#070a12] border-r border-[#151b2a] flex flex-col justify-between py-4 px-3 shrink-0 font-sans transition-[width] duration-300 z-30 select-none relative`}>
      
      {/* Top Brand */}
      <div className="min-h-0 flex flex-col flex-1 overflow-hidden">
        <div className={`flex items-center justify-between ${isCollapsed ? 'justify-center' : 'px-2'} mb-6 group`}>
          <Link 
            to={`${basePath}/overview`} 
            className="flex items-center gap-3 min-w-0"
            title="ProdIntel AI"
          >
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-tr from-[#5b3df5] to-[#7c3aed] shadow-md shadow-[#5b3df5]/30">
              <Brain className="text-white" size={20} />
            </div>
            {!isCollapsed && (
              <div className="flex min-w-0 flex-col">
                <span className="truncate text-[15px] font-bold leading-tight text-white tracking-tight">ProdIntel AI</span>
                <span className="truncate text-[10px] font-medium tracking-wide text-slate-400">Product Intelligence Platform</span>
              </div>
            )}
          </Link>

          {!isCollapsed && (
            <button 
              type="button"
              onClick={() => setIsCollapsed(true)}
              className="text-slate-500 hover:text-white transition-colors p-1"
            >
              <ChevronRight size={14} />
            </button>
          )}
        </div>

        {/* Navigation links */}
        <nav className="space-y-1 overflow-y-auto scrollbar-hide flex-1 pr-0.5 pb-4">
          
          {/* 1. PM Dashboard */}
          <Link
            to={`${basePath}/overview`}
            title={isCollapsed ? 'PM Dashboard' : undefined}
            className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs transition-all duration-150 group ${isCollapsed ? 'justify-center' : 'justify-between'} ${
              isActive(`${basePath}/overview`) 
                ? 'bg-[#5b3df5] text-white shadow-lg shadow-[#5b3df5]/30 font-semibold' 
                : 'text-slate-400 hover:bg-[#111726] hover:text-slate-200 font-medium'
            }`}
          >
            <div className="flex items-center gap-3 min-w-0">
              <LayoutDashboard size={17} className={isActive(`${basePath}/overview`) ? 'text-white' : 'text-slate-400 group-hover:text-slate-200'} />
              {!isCollapsed && <span className="truncate">PM Dashboard</span>}
            </div>
          </Link>

          {/* 2. Insights Accordion Menu */}
          <div className="flex flex-col">
            <button
              onClick={() => {
                if (isCollapsed) setIsCollapsed(false); 
                setIsInsightsOpen(!isInsightsOpen);
              }}
              title={isCollapsed ? 'Insights' : undefined}
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-xs transition-all duration-150 group ${isCollapsed ? 'justify-center' : 'justify-between'} ${
                isInsightsActive 
                  ? 'bg-[#5b3df5] text-white shadow-lg shadow-[#5b3df5]/30 font-semibold' 
                  : 'text-slate-400 hover:bg-[#111726] hover:text-slate-200 font-medium'
              }`}
            >
              <div className="flex items-center gap-3 min-w-0">
                <Lightbulb size={17} className={isInsightsActive ? 'text-white' : 'text-slate-400 group-hover:text-slate-200'} />
                {!isCollapsed && <span className="truncate">Insights</span>}
              </div>
              {!isCollapsed && (
                <ChevronRight 
                  size={14} 
                  className={`shrink-0 transition-transform duration-300 ${isInsightsActive ? 'text-white/80' : 'text-slate-500'} ${isInsightsOpen ? 'rotate-90' : ''}`} 
                />
              )}
            </button>
            
            <div 
              className={`grid transition-all duration-300 ease-in-out ${
                isInsightsOpen && !isCollapsed ? 'grid-rows-[1fr] opacity-100 mt-1' : 'grid-rows-[0fr] opacity-0 mt-0'
              }`}
            >
              <div className="overflow-hidden flex flex-col gap-0.5 ml-9 mr-1">
                {insightSubItems.map((sub, idx) => {
                  const subActive = isInsightsActive && isHashActive(sub.hash);
                  return (
                    <Link
                      key={idx}
                      to={`${basePath}/intelligence/insights${sub.hash}`}
                      className={`text-[11.5px] py-2 px-3 rounded-lg transition-colors ${
                        subActive 
                          ? 'bg-[#1a2236] text-[#a78bfa] font-semibold' 
                          : 'text-slate-500 hover:text-slate-300 hover:bg-[#111726]'
                      }`}
                    >
                      {sub.label}
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>

          {/* 3. Feedback Accordion Menu */}
          <div className="flex flex-col">
            <button
              onClick={() => {
                if (isCollapsed) setIsCollapsed(false); 
                setIsFeedbackOpen(!isFeedbackOpen);
              }}
              title={isCollapsed ? 'Feedback' : undefined}
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-xs transition-all duration-150 group ${isCollapsed ? 'justify-center' : 'justify-between'} ${
                isFeedbackActive 
                  ? 'bg-[#5b3df5] text-white shadow-lg shadow-[#5b3df5]/30 font-semibold' 
                  : 'text-slate-400 hover:bg-[#111726] hover:text-slate-200 font-medium'
              }`}
            >
              <div className="flex items-center gap-3 min-w-0">
                <MessageSquare size={17} className={isFeedbackActive ? 'text-white' : 'text-slate-400 group-hover:text-slate-200'} />
                {!isCollapsed && <span className="truncate">Feedback</span>}
              </div>
              {!isCollapsed && (
                <ChevronRight 
                  size={14} 
                  className={`shrink-0 transition-transform duration-300 ${isFeedbackActive ? 'text-white/80' : 'text-slate-500'} ${isFeedbackOpen ? 'rotate-90' : ''}`} 
                />
              )}
            </button>
            
            <div 
              className={`grid transition-all duration-300 ease-in-out ${
                isFeedbackOpen && !isCollapsed ? 'grid-rows-[1fr] opacity-100 mt-1' : 'grid-rows-[0fr] opacity-0 mt-0'
              }`}
            >
              <div className="overflow-hidden flex flex-col gap-0.5 ml-9 mr-1">
                {feedbackSubItems.map((sub, idx) => {
                  const subActive = location.pathname === sub.path;
                  return (
                    <Link
                      key={idx}
                      to={sub.path}
                      className={`text-[11.5px] py-2 px-3 rounded-lg transition-colors ${
                        subActive 
                          ? 'bg-[#1a2236] text-[#a78bfa] font-semibold' 
                          : 'text-slate-500 hover:text-slate-300 hover:bg-[#111726]'
                      }`}
                    >
                      {sub.label}
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>

          {/* 4. Rest of the navigation items */}
          {navItems.map(({ icon: Icon, label, path }) => {
            const active = isActive(path);
            return (
              <Link
                key={label}
                to={path}
                title={isCollapsed ? label : undefined}
                className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs transition-all duration-150 group ${isCollapsed ? 'justify-center' : 'justify-between'} ${
                  active 
                    ? 'bg-[#5b3df5] text-white shadow-lg shadow-[#5b3df5]/30 font-semibold' 
                    : 'text-slate-400 hover:bg-[#111726] hover:text-slate-200 font-medium'
                }`}
              >
                <div className="flex items-center gap-3 min-w-0">
                  <Icon size={17} className={active ? 'text-white' : 'text-slate-400 group-hover:text-slate-200'} />
                  {!isCollapsed && <span className="truncate">{label}</span>}
                </div>
                {!isCollapsed && active && (
                  <ChevronRight size={14} className="text-white/80 shrink-0" />
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Bottom widgets */}
      <div className="mt-3 space-y-3.5 pt-3 shrink-0">
        {!isCollapsed && (
          <>
            {/* Current Workspace Card */}
            <div className="bg-[#0e1322] border border-[#1a2236] rounded-xl p-3">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-[#5b3df5]/20 border border-[#5b3df5]/30 flex items-center justify-center shrink-0">
                  <LayoutGrid className="w-4 h-4 text-[#a78bfa]" />
                </div>
                <div className="min-w-0 flex-1">
                  <span className="text-[10px] text-slate-400 block leading-tight">Current Workspace</span>
                  <p className="text-xs font-bold text-white truncate mt-0.5">{activeWorkspace.name}</p>
                  <p className="text-[10px] text-slate-400 truncate mt-0.5">{activeWorkspace.membersCount || 12} Members</p>
                </div>
              </div>
            </div>

            {/* Workspace Usage */}
            <div className="space-y-1.5 px-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 text-[11px]">Workspace Usage</span>
                <span className="text-slate-300 font-bold text-[11px]">78%</span>
              </div>
              <div className="h-1.5 w-full bg-[#171e31] rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-[#5b3df5] to-[#8b5cf6] rounded-full w-[78%]"></div>
              </div>
              <div className="text-[10px] font-medium text-slate-500">7.8 GB / 10 GB</div>
            </div>
          </>
        )}

        {/* Collapse toggle */}
        <button
          type="button"
          onClick={() => setIsCollapsed(!isCollapsed)}
          className={`flex w-full items-center gap-2.5 rounded-lg px-2 py-1.5 text-xs text-slate-400 hover:text-slate-200 transition-colors ${isCollapsed ? 'justify-center' : ''}`}
        >
          {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
          {!isCollapsed && <span className="text-xs font-medium">Collapse</span>}
        </button>
      </div>

    </aside>
  );
}