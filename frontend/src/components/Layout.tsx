import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Landmark, 
  Cpu, 
  ShieldCheck, 
  Activity, 
  BarChart3, 
  List, 
  Terminal, 
  Network
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const navItems = [
  { name: 'Overview', path: '/', icon: LayoutDashboard },
  { name: 'Banking Sim', path: '/banking', icon: Landmark },
  { name: 'IoT Sim', path: '/iot', icon: Cpu },
  { name: 'Encryption Flow', path: '/encryption', icon: ShieldCheck },
  { name: 'Security Engine', path: '/security-engine', icon: Activity },
  { name: 'Benchmarks', path: '/benchmarks', icon: BarChart3 },
  { name: 'Algorithms', path: '/algorithms', icon: List },
  { name: 'Event Logs', path: '/logs', icon: Terminal },
  { name: 'Architecture', path: '/architecture', icon: Network },
];

export const Layout: React.FC = () => {
  return (
    <div className="flex h-screen w-full bg-slate-950 text-slate-50 overflow-hidden">
      {/* Sidebar */}
      <motion.aside 
        initial={{ x: -250 }}
        animate={{ x: 0 }}
        className="w-64 flex flex-col border-r border-slate-800 glass z-10"
      >
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <div className="flex items-center gap-2 text-cyan-400 font-bold text-lg tracking-wider text-glow">
            <ShieldCheck size={24} />
            Q-ORCHESTRATOR
          </div>
        </div>
        
        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) => cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-md transition-all duration-200",
                isActive 
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20" 
                  : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/50"
              )}
            >
              <item.icon size={18} />
              <span className="font-medium text-sm">{item.name}</span>
            </NavLink>
          ))}
        </nav>
        
        <div className="p-4 border-t border-slate-800">
          <div className="glass-card rounded-lg p-4 flex flex-col items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_10px_rgba(16,185,129,0.8)]" />
            <span className="text-xs text-slate-400 font-medium">System Online</span>
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative overflow-hidden bg-grid-pattern">
        {/* Top Header */}
        <header className="h-16 border-b border-slate-800/50 glass flex items-center px-8 justify-between z-10">
          <h1 className="text-lg font-semibold text-slate-200">Quantum Security Dashboard</h1>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-xs font-mono bg-slate-900/50 border border-slate-700 px-3 py-1.5 rounded-full">
              <span className="text-slate-400">Current Threat Level:</span>
              <span className="text-emerald-400">LOW</span>
            </div>
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-sm font-bold shadow-[0_0_15px_rgba(14,165,233,0.4)]">
              ADMIN
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-y-auto p-6 relative z-0">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
