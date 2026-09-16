import React, { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Activity,
  AlertTriangle,
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  CalendarDays,
  CheckCircle2,
  ChevronDown,
  Clock,
  Download,
  Eye,
  FileText,
  Filter,
  Layers,
  MessageSquare,
  MoreHorizontal,
  Plus,
  Search,
  SlidersHorizontal,
  Sparkles,
  Star,
  Target,
  Users,
  X,
} from 'lucide-react';

const COLORS = {
  purple: '#8b5cf6',
  violet: '#a78bfa',
  green: '#22c55e', 
  amber: '#eab308', 
  red: '#ef4444',    
  blue: '#3b82f6',
  orange: '#f97316',
  cyan: '#06b6d4',
};

const FEATURES_ROWS = [
  { 
    id: 1, 
    name: 'One-click checkout', 
    desc: 'Allow users to complete purchase in one click.', 
    category: 'Checkout & Payments', 
    priority: 'Critical', 
    status: 'In Progress', 
    usersImpacted: '8,542', 
    feedbackCount: '352', 
    createdOn: 'Aug 28, 2025', 
    lastUpdated: 'Aug 31, 2025',
    source: 'In-App Feedback',
    owner: 'Priya Sharma',
    longDesc: 'Users want a faster checkout experience. This feature allows them to place orders with previously saved details in a single click.',
    topFeedback: [
      'Checkout process is too slow and payment fails freq...',
      'Please add one-click purchase option',
      'Need faster checkout for returning customers'
    ]
  },
  { 
    id: 2, 
    name: 'Multiple payment options', 
    desc: 'Support more UPI and digital wallets.', 
    category: 'Payments', 
    priority: 'High', 
    status: 'Implemented', 
    usersImpacted: '6,231', 
    feedbackCount: '289', 
    createdOn: 'Aug 20, 2025', 
    lastUpdated: 'Aug 30, 2025',
    source: 'Support Tickets',
    owner: 'Arjun Mehta',
    longDesc: 'Integration with regional gateways such as PhonePe, Google Pay, and Paytm.',
    topFeedback: ['Add more payment options like UPI and digital wallets.']
  },
  { 
    id: 3, 
    name: 'Order tracking in real-time', 
    desc: 'Provide real-time updates for orders.', 
    category: 'Order Management', 
    priority: 'High', 
    status: 'In Progress', 
    usersImpacted: '5,412', 
    feedbackCount: '241', 
    createdOn: 'Aug 18, 2025', 
    lastUpdated: 'Aug 29, 2025',
    source: 'In-App Feedback',
    owner: 'Rohit Singh',
    longDesc: 'Live map tracking and carrier webhook syncing for real-time order status.',
    topFeedback: ['Delivery tracking is not updating in real-time.']
  },
  { 
    id: 4, 
    name: 'Dark mode', 
    desc: 'Add dark theme for better experience.', 
    category: 'UI / UX', 
    priority: 'Medium', 
    status: 'Planned', 
    usersImpacted: '3,842', 
    feedbackCount: '186', 
    createdOn: 'Aug 15, 2025', 
    lastUpdated: 'Aug 28, 2025',
    source: 'Email',
    owner: 'Neha Kapoor',
    longDesc: 'Full dark theme support across mobile applications and web portal.',
    topFeedback: ['Need dark mode option in the app.']
  },
  { 
    id: 5, 
    name: 'Wishlist', 
    desc: 'Save products to wishlist.', 
    category: 'Product Discovery', 
    priority: 'Medium', 
    status: 'Planned', 
    usersImpacted: '3,210', 
    feedbackCount: '153', 
    createdOn: 'Aug 10, 2025', 
    lastUpdated: 'Aug 25, 2025',
    source: 'In-App Feedback',
    owner: 'Priya Sharma',
    longDesc: 'Allow users to save items for future purchases or share lists.',
    topFeedback: ['It would be great to have a wish list for products.']
  },
  { 
    id: 6, 
    name: 'Guest checkout', 
    desc: 'Checkout without account creation.', 
    category: 'Checkout & Payments', 
    priority: 'High', 
    status: 'Implemented', 
    usersImpacted: '4,125', 
    feedbackCount: '132', 
    createdOn: 'Aug 05, 2025', 
    lastUpdated: 'Aug 22, 2025',
    source: 'Support Tickets',
    owner: 'Arjun Mehta',
    longDesc: 'Frictionless checkout experience without mandatory sign-up.',
    topFeedback: ['Allow guest checkout to reduce cart abandonment.']
  },
  { 
    id: 7, 
    name: 'Price drop alerts', 
    desc: 'Notify users when price drops.', 
    category: 'Notifications', 
    priority: 'Low', 
    status: 'Not Started', 
    usersImpacted: '2,134', 
    feedbackCount: '98', 
    createdOn: 'Jul 28, 2025', 
    lastUpdated: 'Aug 15, 2025',
    source: 'Email',
    owner: 'Rohit Singh',
    longDesc: 'Push and email notifications when items in wishlist drop in price.',
    topFeedback: ['Want notifications for price drops on saved items.']
  },
  { 
    id: 8, 
    name: 'Product size guide', 
    desc: 'Show size guide for clothing products.', 
    category: 'Product Info', 
    priority: 'Low', 
    status: 'Not Started', 
    usersImpacted: '1,316', 
    feedbackCount: '64', 
    createdOn: 'Jul 22, 2025', 
    lastUpdated: 'Aug 10, 2025',
    source: 'In-App Feedback',
    owner: 'Neha Kapoor',
    longDesc: 'Interactive size charts and measurements modal for apparel.',
    topFeedback: ['Need accurate size guide to avoid wrong fit returns.']
  }
];

function cn(...classes) {
  return classes.filter(Boolean).join(';');
}

/* =========================================
   COMPONENTS
   ========================================= */
function LineChart({ series = [], labels = [], height = 200, max = 100 }) {
  const width = 720; 
  const pad = { left: 35, right: 15, top: 15, bottom: 25 }; 
  const innerW = width - pad.left - pad.right; 
  const innerH = height - pad.top - pad.bottom;
  
  const x = (i, count) => pad.left + (count <= 1 ? 0 : (i / (count - 1)) * innerW);
  const y = (v) => pad.top + (1 - v / max) * innerH;

  const buildPath = (values) => values.map((v, i) => `${i === 0 ? 'M' : 'L'} ${x(i, values.length).toFixed(2)} ${y(v).toFixed(2)}`).join(' ');

  return (
    <div className="w-full relative">
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto" preserveAspectRatio="none">
        {[0, 0.5, 1].map((t, idx) => {
          const yy = pad.top + t * innerH;
          return <line key={idx} x1={pad.left} x2={width - pad.right} y1={yy} y2={yy} stroke="#1e293b" strokeDasharray="4 4" />;
        })}
        {labels.map((lbl, i) => (
          <text key={i} x={x(i, labels.length)} y={height - 5} textAnchor="middle" fill="#64748b" fontSize="9">{lbl}</text>
        ))}
        {series.map((s) => (
          <path key={s.key} d={buildPath(s.values)} fill="none" stroke={s.color} strokeWidth={2.5} strokeLinejoin="round" />
        ))}
      </svg>
    </div>
  );
}

function Donut({ segments, centerTop, centerBottom, size = 130 }) {
  const radius = 45; const stroke = 18; const circumference = 2 * Math.PI * radius; let offset = 0;
  return (
    <div className="relative shrink-0 transition-transform duration-500 hover:scale-105 cursor-pointer group/donut" style={{ width: size, height: size }}>
      <svg viewBox="0 0 120 120" className="h-full w-full -rotate-90">
        <circle cx="60" cy="60" r={radius} fill="none" stroke="#1e293b" strokeWidth={stroke} />
        {segments.map((s) => {
          const dash = (s.value / 100) * circumference; const currentOffset = offset; offset += dash;
          return (<circle key={s.label} cx="60" cy="60" r={radius} fill="none" stroke={s.color} strokeWidth={stroke} strokeDasharray={`${dash} ${circumference - dash}`} strokeDashoffset={-currentOffset} />);
        })}
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-[8px] text-slate-400">{centerTop}</span>
        <span className="text-[16px] font-bold text-slate-100">{centerBottom}</span>
      </div>
    </div>
  );
}

function LegendRow({ label, value, color }) {
  return (
    <div className="flex items-center justify-between gap-4 py-0.5 text-[10px]">
      <span className="flex items-center gap-1.5 text-slate-300">
        <span className="h-2 w-2 rounded-[2px]" style={{ background: color }} />
        {label}
      </span>
      <span className="font-bold text-slate-200">{value}</span>
    </div>
  );
}

function PriorityBadge({ value }) {
  const map = { 
    Critical: 'bg-red-500/10 text-red-400 border-red-500/20', 
    High: 'bg-orange-500/10 text-orange-400 border-orange-500/20', 
    Medium: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    Low: 'bg-blue-500/10 text-blue-400 border-blue-500/20'
  };
  return <span className={cn('inline-flex border rounded-md px-2 py-0.5 text-[9px] font-semibold', map[value] || 'bg-slate-800 text-slate-300')}>{value}</span>;
}

function StatusBadge({ value }) {
  const map = {
    'Implemented': 'bg-green-500/10 text-green-400 border-green-500/20',
    'In Progress': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    'Planned': 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    'Not Started': 'bg-slate-700/30 text-slate-400 border-slate-600/30'
  };
  return <span className={cn('inline-flex border rounded-md px-2 py-0.5 text-[9px] font-semibold', map[value] || 'bg-slate-800 text-slate-300')}>{value}</span>;
}

/* =========================================
   MAIN FEATURES DASHBOARD
   ========================================= */
export default function FeaturesDashboard() {
  const [selectedFeature, setSelectedFeature] = useState(FEATURES_ROWS[0]);
  const [isLoading, setIsLoading] = useState(false);
  const [toastMessage, setToastMessage] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const triggerToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  const filteredFeatures = useMemo(() => {
    return FEATURES_ROWS.filter(f => f.name.toLowerCase().includes(searchQuery.toLowerCase()) || f.category.toLowerCase().includes(searchQuery.toLowerCase()));
  }, [searchQuery]);

  return (
    <div className="min-h-screen w-full bg-[#070a10] text-slate-300 font-sans flex flex-col justify-between overflow-y-auto pb-16">
      
      <div className="p-6 space-y-6 max-w-[1600px] w-full mx-auto">
        
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-2">
          <div>
            <div className="flex items-center gap-2 text-[11px] text-slate-400 mb-1">
              <span>Insights</span>
              <span>›</span>
              <span className="text-white font-medium">Features</span>
            </div>
            <h1 className="text-[22px] font-bold text-white tracking-tight">Features</h1>
            <p className="text-[11px] text-slate-400 mt-0.5">Discover, analyze, and manage product features based on user feedback.</p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <button onClick={() => triggerToast('Date range selector opened')} className="flex items-center gap-2 bg-[#111827] border border-[#263348] px-3.5 py-1.5 rounded-lg text-[10px] text-slate-300 hover:border-violet-500 transition-all">
              <CalendarDays className="w-3.5 h-3.5 text-slate-400"/> Jul 1 – Aug 31, 2025 <ChevronDown className="w-3 h-3 text-slate-500"/>
            </button>
            <button onClick={() => triggerToast('Filters panel opened')} className="flex items-center gap-2 bg-[#111827] border border-[#263348] px-3.5 py-1.5 rounded-lg text-[10px] text-slate-300 hover:border-violet-500 transition-all">
              <Filter className="w-3.5 h-3.5 text-slate-400"/> Filters
            </button>
            <button onClick={() => triggerToast('Exporting Report...')} className="flex items-center gap-2 bg-[#111827] border border-[#263348] px-3.5 py-1.5 rounded-lg text-[10px] text-slate-300 hover:border-violet-500 transition-all">
              <Download className="w-3.5 h-3.5 text-slate-400"/> Export
            </button>
            <button onClick={() => triggerToast('Feature creation modal opened')} className="flex items-center gap-2 bg-violet-600 hover:bg-violet-700 px-4 py-1.5 rounded-lg text-[10px] font-medium text-white shadow-lg shadow-violet-950 transition-all hover:scale-105">
              <Plus className="w-3.5 h-3.5"/> Add Feature
            </button>
          </div>
        </div>

        {/* Top KPI Cards Grid */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-[#111827] border border-[#263348] rounded-xl p-4 flex flex-col justify-between transition-all hover:border-violet-500/50">
            <div className="flex items-center justify-between">
              <div className="h-8 w-8 rounded-lg bg-violet-500/10 text-violet-400 flex items-center justify-center"><Layers className="h-4 w-4" /></div>
              <span className="text-[10px] text-green-400 font-medium">↑ 12.0% vs Jun</span>
            </div>
            <div className="mt-4"><p className="text-[11px] text-slate-400">Total Features</p><h3 className="text-[18px] font-bold text-white">56</h3></div>
          </div>

          <div className="bg-[#111827] border border-[#263348] rounded-xl p-4 flex flex-col justify-between transition-all hover:border-violet-500/50">
            <div className="flex items-center justify-between">
              <div className="h-8 w-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center"><Activity className="h-4 w-4" /></div>
              <span className="text-[10px] text-green-400 font-medium">↑ 8.6% vs Jun</span>
            </div>
            <div className="mt-4"><p className="text-[11px] text-slate-400">Active Features</p><h3 className="text-[18px] font-bold text-white">38</h3></div>
          </div>

          <div className="bg-[#111827] border border-[#263348] rounded-xl p-4 flex flex-col justify-between transition-all hover:border-violet-500/50">
            <div className="flex items-center justify-between">
              <div className="h-8 w-8 rounded-lg bg-green-500/10 text-green-400 flex items-center justify-center"><CheckCircle2 className="h-4 w-4" /></div>
              <span className="text-[10px] text-green-400 font-medium">↑ 16.7% vs Jun</span>
            </div>
            <div className="mt-4"><p className="text-[11px] text-slate-400">Implemented</p><h3 className="text-[18px] font-bold text-white">14</h3></div>
          </div>

          <div className="bg-[#111827] border border-[#263348] rounded-xl p-4 flex flex-col justify-between transition-all hover:border-violet-500/50">
            <div className="flex items-center justify-between">
              <div className="h-8 w-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center"><Clock className="h-4 w-4" /></div>
              <span className="text-[10px] text-green-400 font-medium">↑ 6.7% vs Jun</span>
            </div>
            <div className="mt-4"><p className="text-[11px] text-slate-400">In Progress</p><h3 className="text-[18px] font-bold text-white">16</h3></div>
          </div>

          <div className="bg-[#111827] border border-[#263348] rounded-xl p-4 flex flex-col justify-between transition-all hover:border-violet-500/50">
            <div className="flex items-center justify-between">
              <div className="h-8 w-8 rounded-lg bg-red-500/10 text-red-400 flex items-center justify-center"><AlertTriangle className="h-4 w-4" /></div>
              <span className="text-[10px] text-red-400 font-medium">↓ 7.7% vs Jun</span>
            </div>
            <div className="mt-4"><p className="text-[11px] text-slate-400">Planned</p><h3 className="text-[18px] font-bold text-white">12</h3></div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 xl:grid-cols-[1.4fr_1fr_1fr] gap-4">
          
          {/* Trend Chart */}
          <div className="bg-[#111827] border border-[#263348] rounded-xl p-5 flex flex-col justify-between">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-[12px] font-semibold text-white">Feature Trend Over Time</h3>
              <span className="text-[10px] text-slate-400">Daily ▾</span>
            </div>
            <LineChart 
              labels={['Jul 1', 'Jul 15', 'Jul 29', 'Aug 12', 'Aug 31']} 
              max={80} 
              series={[
                { key: 'total', color: COLORS.purple, values: [20, 35, 30, 48, 56] },
                { key: 'impl', color: COLORS.green, values: [5, 8, 10, 12, 14] },
                { key: 'prog', color: COLORS.blue, values: [8, 12, 11, 14, 16] },
              ]} 
            />
          </div>

          {/* Status Donut */}
          <div className="bg-[#111827] border border-[#263348] rounded-xl p-5 flex flex-col justify-between">
            <h3 className="text-[12px] font-semibold text-white mb-3">Features by Status</h3>
            <div className="flex items-center justify-around py-1">
              <Donut 
                segments={[
                  { label: 'Implemented', value: 25, color: COLORS.green },
                  { label: 'In Progress', value: 28, color: COLORS.blue },
                  { label: 'Planned', value: 21, color: COLORS.amber },
                  { label: 'Not Started', value: 26, color: COLORS.red }
                ]}
                centerTop="Total"
                centerBottom="56"
                size={120}
              />
              <div className="space-y-1">
                <LegendRow label="Implemented" value="14 (25.0%)" color={COLORS.green} />
                <LegendRow label="In Progress" value="16 (28.6%)" color={COLORS.blue} />
                <LegendRow label="Planned" value="12 (21.4%)" color={COLORS.amber} />
                <LegendRow label="Not Started" value="14 (25.0%)" color={COLORS.red} />
              </div>
            </div>
          </div>

          {/* Priority Donut */}
          <div className="bg-[#111827] border border-[#263348] rounded-xl p-5 flex flex-col justify-between">
            <h3 className="text-[12px] font-semibold text-white mb-3">Features by Priority</h3>
            <div className="flex items-center justify-around py-1">
              <Donut 
                segments={[
                  { label: 'Critical', value: 18, color: COLORS.red },
                  { label: 'High', value: 32, color: COLORS.orange },
                  { label: 'Medium', value: 30, color: COLORS.amber },
                  { label: 'Low', value: 12, color: COLORS.green }
                ]}
                centerTop="Total"
                centerBottom="56"
                size={120}
              />
              <div className="space-y-1">
                <LegendRow label="Critical" value="10 (17.9%)" color={COLORS.red} />
                <LegendRow label="High" value="18 (32.1%)" color={COLORS.orange} />
                <LegendRow label="Medium" value="17 (30.4%)" color={COLORS.amber} />
                <LegendRow label="Low" value="7 (12.5%)" color={COLORS.green} />
              </div>
            </div>
          </div>

        </div>

        {/* Data Table & Details Drawer */}
        <div className="grid grid-cols-1 xl:grid-cols-[1fr_360px] gap-4">
          
          <div className="bg-[#111827] border border-[#263348] rounded-xl overflow-hidden flex flex-col justify-between shadow-xl">
            <div>
              <div className="p-3 border-b border-[#263348] flex items-center justify-between gap-3 bg-[#0d131f]">
                <div className="flex items-center gap-2">
                  <button className="bg-[#161f31] border border-[#263348] px-3 py-1 rounded text-[10px] text-slate-300">All Statuses ▾</button>
                  <button className="bg-[#161f31] border border-[#263348] px-3 py-1 rounded text-[10px] text-slate-300">All Priorities ▾</button>
                  <button className="bg-[#161f31] border border-[#263348] px-3 py-1 rounded text-[10px] text-slate-300">All Categories ▾</button>
                </div>
                <div className="relative">
                  <Search className="absolute left-2.5 top-2 h-3.5 w-3.5 text-slate-400" />
                  <input 
                    type="text" 
                    placeholder="Search features..." 
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="bg-[#161f31] border border-[#263348] rounded-lg pl-8 pr-3 py-1 text-[10px] text-white focus:outline-none w-48" 
                  />
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-[11px]">
                  <thead className="bg-[#161f31] text-slate-400 border-b border-[#263348]">
                    <tr>
                      <th className="px-4 py-2.5 font-medium">Feature</th>
                      <th className="px-3 py-2.5 font-medium">Category</th>
                      <th className="px-3 py-2.5 font-medium">Priority</th>
                      <th className="px-3 py-2.5 font-medium">Status</th>
                      <th className="px-3 py-2.5 font-medium">Users Impacted</th>
                      <th className="px-3 py-2.5 font-medium">Feedback</th>
                      <th className="px-3 py-2.5 font-medium text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1e293b]">
                    {filteredFeatures.map((row) => (
                      <tr 
                        key={row.id} 
                        onClick={() => setSelectedFeature(row)} 
                        className={cn("cursor-pointer transition-colors hover:bg-[#161f31]", selectedFeature.id === row.id ? "bg-[#161f31] border-l-4 border-violet-500" : "")}
                      >
                        <td className="px-4 py-3">
                          <div className="font-semibold text-white">{row.name}</div>
                          <div className="text-[10px] text-slate-400 truncate max-w-[200px]">{row.desc}</div>
                        </td>
                        <td className="px-3 py-3 text-slate-300">{row.category}</td>
                        <td className="px-3 py-3"><PriorityBadge value={row.priority} /></td>
                        <td className="px-3 py-3"><StatusBadge value={row.status} /></td>
                        <td className="px-3 py-3 text-slate-200 font-medium">{row.usersImpacted}</td>
                        <td className="px-3 py-3 text-violet-400 font-medium">{row.feedbackCount}</td>
                        <td className="px-3 py-3 text-right">
                          <Eye className="h-4 w-4 inline text-slate-400 hover:text-white" />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="p-3 border-t border-[#263348] text-[10px] text-slate-400 bg-[#0d131f] flex justify-between items-center">
              <span>Showing 1 to {filteredFeatures.length} of 56 features</span>
              <span>10 / page</span>
            </div>
          </div>

          {/* Feature Details Drawer */}
          <div className="bg-[#111827] border border-[#263348] rounded-xl p-5 flex flex-col justify-between shadow-xl">
            <div>
              <div className="flex items-center justify-between border-b border-[#1e293b] pb-3 mb-4">
                <h3 className="text-[12px] font-bold text-white flex items-center gap-2">
                  <FileText className="h-4 w-4 text-violet-400"/> Feature Details
                </h3>
                <button onClick={() => triggerToast('Drawer minimized')} className="text-slate-400 hover:text-white"><X className="h-4 w-4"/></button>
              </div>

              <div className="space-y-4 text-[11px]">
                <div>
                  <h4 className="text-[13px] font-bold text-white mb-1">{selectedFeature.name}</h4>
                  <p className="text-[10px] text-slate-400">{selectedFeature.desc}</p>
                </div>

                <div className="flex items-center gap-2">
                  <PriorityBadge value={selectedFeature.priority} />
                  <StatusBadge value={selectedFeature.status} />
                  <span className="text-[10px] text-slate-300 bg-[#161f31] px-2 py-0.5 rounded border border-[#263348]">{selectedFeature.category}</span>
                </div>

                <div className="space-y-2 py-3 border-t border-b border-[#1e293b] text-slate-300">
                  <div className="flex justify-between"><span className="text-slate-400">Users Impacted</span><span className="font-semibold text-white">{selectedFeature.usersImpacted}</span></div>
                  <div className="flex justify-between"><span className="text-slate-400">Total Feedback</span><span className="font-semibold text-white">{selectedFeature.feedbackCount}</span></div>
                  <div className="flex justify-between"><span className="text-slate-400">Created On</span><span>{selectedFeature.createdOn}</span></div>
                  <div className="flex justify-between"><span className="text-slate-400">Last Updated</span><span>{selectedFeature.lastUpdated}</span></div>
                  <div className="flex justify-between"><span className="text-slate-400">Source</span><span>{selectedFeature.source}</span></div>
                  <div className="flex justify-between"><span className="text-slate-400">Owner</span><span className="text-violet-400 font-medium">{selectedFeature.owner}</span></div>
                </div>

                <div>
                  <span className="text-[10px] text-slate-400 font-semibold block mb-1">Description</span>
                  <p className="text-[10px] text-slate-300 bg-[#161f31] p-2.5 rounded border border-[#263348] leading-relaxed">
                    {selectedFeature.longDesc}
                  </p>
                </div>

                <div>
                  <span className="text-[10px] text-slate-400 font-semibold block mb-1.5">Top Related Feedback</span>
                  <div className="space-y-1.5">
                    {selectedFeature.topFeedback.map((fb, idx) => (
                      <div key={idx} className="text-[10px] bg-[#161f31]/60 p-2 rounded border border-[#263348] text-slate-300 truncate">
                        💬 "{fb}"
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <button 
              onClick={() => triggerToast('Redirecting to full feature report...')} 
              className="w-full mt-5 bg-violet-600 hover:bg-violet-700 text-white rounded-lg py-2.5 text-[11px] font-medium transition-all shadow-lg flex items-center justify-center gap-2 hover:scale-[1.01]"
            >
              <span>View full details</span> →
            </button>
          </div>

        </div>

      </div>

      {toastMessage && (
        <div className="fixed bottom-8 right-8 z-50 flex items-center gap-2 bg-[#111827] border border-violet-500 px-4 py-3 rounded-xl shadow-2xl animate-in slide-in-from-bottom-5">
          <Sparkles className="w-4 h-4 text-violet-400 animate-spin"/>
          <span className="text-[11px] text-white">{toastMessage}</span>
        </div>
      )}
    </div>
  );
}