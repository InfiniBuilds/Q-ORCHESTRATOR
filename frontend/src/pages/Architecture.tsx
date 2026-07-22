import React from 'react';
import { Network, Shield, Server, Box, ArrowRightLeft } from 'lucide-react';
import { motion } from 'framer-motion';

export const Architecture: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Network className="text-cyan-400" />
            System Architecture
          </h2>
          <p className="text-slate-400">End-to-end flow of the Quantum Security Orchestrator.</p>
        </div>
      </div>

      <div className="glass-card p-8 rounded-xl border border-slate-800 min-h-[600px] flex items-center justify-center relative overflow-hidden">
        {/* Background Grid */}
        <div className="absolute inset-0 bg-grid-pattern opacity-30"></div>

        <div className="relative z-10 w-full max-w-5xl flex flex-col md:flex-row items-center justify-between gap-8">
          
          {/* Frontend Client */}
          <div className="flex flex-col items-center group">
            <div className="w-32 h-32 glass-card rounded-xl border border-cyan-500/50 flex flex-col items-center justify-center text-cyan-400 shadow-[0_0_20px_rgba(14,165,233,0.2)] group-hover:shadow-[0_0_30px_rgba(14,165,233,0.4)] transition-all">
              <Box size={40} className="mb-2" />
              <span className="font-bold">Client Apps</span>
            </div>
            <p className="text-sm text-slate-400 mt-4 text-center">Banking, IoT, etc.</p>
          </div>

          {/* Connection 1 */}
          <div className="flex-1 flex flex-col items-center justify-center relative min-w-[100px]">
            <ArrowRightLeft className="text-slate-500 mb-2" size={24} />
            <div className="h-0.5 w-full bg-slate-700 relative overflow-hidden">
               <motion.div 
                 className="absolute inset-0 bg-gradient-to-r from-transparent via-cyan-400 to-transparent w-full"
                 animate={{ x: ['-100%', '100%'] }}
                 transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
               />
            </div>
            <span className="text-xs text-slate-500 mt-2 absolute top-full">REST/JSON</span>
          </div>

          {/* Orchestrator Backend */}
          <div className="flex flex-col items-center group">
            <div className="w-40 h-40 glass-card rounded-xl border-2 border-purple-500 flex flex-col items-center justify-center text-purple-400 shadow-[0_0_25px_rgba(168,85,247,0.3)] group-hover:shadow-[0_0_35px_rgba(168,85,247,0.5)] transition-all relative">
              <Shield size={48} className="mb-2" />
              <span className="font-bold text-lg">Orchestrator</span>
              <div className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-slate-900 border border-purple-500 flex items-center justify-center">
                <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse" />
              </div>
            </div>
            <div className="bg-slate-900/80 border border-slate-700 p-3 rounded-lg mt-4 text-xs text-slate-300 w-48 text-center backdrop-blur-sm">
              <p>Risk Analyzer</p>
              <p>Context Builder</p>
              <p>Algorithm Selector</p>
            </div>
          </div>

          {/* Connection 2 */}
          <div className="flex-1 flex flex-col items-center justify-center relative min-w-[100px]">
            <ArrowRightLeft className="text-slate-500 mb-2" size={24} />
            <div className="h-0.5 w-full bg-slate-700 relative overflow-hidden">
               <motion.div 
                 className="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-400 to-transparent w-full"
                 animate={{ x: ['-100%', '100%'] }}
                 transition={{ duration: 1.5, repeat: Infinity, ease: 'linear', delay: 0.5 }}
               />
            </div>
            <span className="text-xs text-slate-500 mt-2 absolute top-full">Python Core</span>
          </div>

          {/* Crypto Executor */}
          <div className="flex flex-col items-center group">
            <div className="w-32 h-32 glass-card rounded-xl border border-emerald-500/50 flex flex-col items-center justify-center text-emerald-400 shadow-[0_0_20px_rgba(16,185,129,0.2)] group-hover:shadow-[0_0_30px_rgba(16,185,129,0.4)] transition-all">
              <Server size={40} className="mb-2" />
              <span className="font-bold">Crypto Exec</span>
            </div>
            <div className="bg-slate-900/80 border border-slate-700 p-3 rounded-lg mt-4 text-xs text-slate-300 w-40 text-center backdrop-blur-sm">
              <p className="text-cyan-400">ML-KEM</p>
              <p className="text-purple-400">ML-DSA</p>
              <p className="text-emerald-400">AES-GCM</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};
