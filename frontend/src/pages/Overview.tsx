import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Shield, Server, Activity, Lock, Cpu, Network } from 'lucide-react';


export const Overview: React.FC = () => {
  const [stats] = useState({
    activeProfiles: 3,
    totalRequests: 1205,
    threatLevel: 'Low',
    averageLatency: '45ms'
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">System Overview</h2>
          <p className="text-slate-400">Live orchestrator status and metrics.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Active Profiles" value={stats.activeProfiles} icon={Shield} color="text-emerald-400" />
        <StatCard title="Total Requests" value={stats.totalRequests} icon={Activity} color="text-cyan-400" />
        <StatCard title="Avg Latency" value={stats.averageLatency} icon={Server} color="text-amber-400" />
        <StatCard title="Threat Level" value={stats.threatLevel} icon={Lock} color="text-emerald-400" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-6 rounded-xl border border-slate-800"
        >
          <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
            <Cpu className="text-cyan-400" size={20} />
            Active Cryptographic Suite
          </h3>
          <div className="space-y-4">
            <div className="bg-slate-900/50 p-4 rounded-lg border border-slate-700/50">
              <p className="text-sm text-slate-400 mb-1">Key Encapsulation Mechanism</p>
              <p className="text-xl font-mono text-cyan-300">ML-KEM (Kyber-768)</p>
            </div>
            <div className="bg-slate-900/50 p-4 rounded-lg border border-slate-700/50">
              <p className="text-sm text-slate-400 mb-1">Digital Signature Algorithm</p>
              <p className="text-xl font-mono text-purple-300">ML-DSA (Dilithium-3)</p>
            </div>
            <div className="bg-slate-900/50 p-4 rounded-lg border border-slate-700/50">
              <p className="text-sm text-slate-400 mb-1">Symmetric Encryption</p>
              <p className="text-xl font-mono text-emerald-300">AES-256-GCM</p>
            </div>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-6 rounded-xl border border-slate-800 flex flex-col items-center justify-center min-h-[300px]"
        >
           <h3 className="text-lg font-semibold text-slate-200 mb-6 self-start w-full flex items-center gap-2">
            <Network className="text-cyan-400" size={20} />
            Orchestration Flow
          </h3>
          <div className="flex items-center justify-center w-full gap-4">
             <div className="flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-slate-800 border-2 border-cyan-500 flex items-center justify-center text-cyan-400 shadow-[0_0_15px_rgba(14,165,233,0.3)]">
                  <Activity size={24} />
                </div>
                <span className="text-xs text-slate-400 mt-2">Context</span>
             </div>
             
             <div className="flex-1 h-1 bg-slate-800 relative">
               <motion.div 
                 className="absolute inset-y-0 left-0 bg-cyan-500"
                 animate={{ width: ["0%", "100%", "0%"], left: ["0%", "0%", "100%"] }}
                 transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
               />
             </div>

             <div className="flex flex-col items-center">
                <div className="w-20 h-20 rounded-full bg-slate-800 border-2 border-purple-500 flex items-center justify-center text-purple-400 shadow-[0_0_20px_rgba(168,85,247,0.3)]">
                  <Shield size={32} />
                </div>
                <span className="text-xs text-slate-400 mt-2">Q-Orchestrator</span>
             </div>

             <div className="flex-1 h-1 bg-slate-800 relative">
               <motion.div 
                 className="absolute inset-y-0 left-0 bg-emerald-500"
                 animate={{ width: ["0%", "100%", "0%"], left: ["0%", "0%", "100%"] }}
                 transition={{ duration: 2, repeat: Infinity, ease: "linear", delay: 1 }}
               />
             </div>

             <div className="flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-slate-800 border-2 border-emerald-500 flex items-center justify-center text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
                  <Lock size={24} />
                </div>
                <span className="text-xs text-slate-400 mt-2">Crypto Exec</span>
             </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

function StatCard({ title, value, icon: Icon, color }: { title: string, value: string | number, icon: any, color: string }) {
  return (
    <motion.div 
      whileHover={{ y: -5, scale: 1.02 }}
      className="glass-card p-6 rounded-xl border border-slate-800 flex items-center gap-4 cursor-pointer"
    >
      <div className={`p-3 rounded-lg bg-slate-900 ${color} shadow-[0_0_15px_currentColor] opacity-80`}>
        <Icon size={24} />
      </div>
      <div>
        <p className="text-sm text-slate-400">{title}</p>
        <p className="text-2xl font-bold text-slate-100">{value}</p>
      </div>
    </motion.div>
  );
}
