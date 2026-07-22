import React, { useState, useEffect } from 'react';
import { Terminal } from 'lucide-react';
import { mockEventLogs } from '@/api';
import { motion, AnimatePresence } from 'framer-motion';

export const EventLogs: React.FC = () => {
  const [logs, setLogs] = useState([...mockEventLogs]);

  useEffect(() => {
    // Poll the mock logs every second to see if new ones were added
    const interval = setInterval(() => {
      setLogs([...mockEventLogs]);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6 h-[calc(100vh-8rem)] flex flex-col">
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Terminal className="text-cyan-400" />
            Live Backend Event Logs
          </h2>
          <p className="text-slate-400">Real-time audit trail of orchestrator operations.</p>
        </div>
      </div>

      <div className="flex-1 glass-card p-2 rounded-xl border border-slate-800 flex flex-col overflow-hidden">
        <div className="bg-[#0c1017] flex-1 rounded-lg border border-slate-800 p-4 font-mono text-sm overflow-y-auto">
          <div className="space-y-2">
            <AnimatePresence>
              {logs.map((log) => (
                <motion.div 
                  key={log.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex flex-col md:flex-row md:items-center gap-2 md:gap-4 border-b border-slate-800/50 pb-2 mb-2"
                >
                  <span className="text-cyan-600 shrink-0">[{log.timestamp.split('T')[1].slice(0,-1)}]</span>
                  <span className={`shrink-0 font-bold ${
                    log.event.includes('ERROR') ? 'text-red-400' : 
                    log.event.includes('SYSTEM') ? 'text-emerald-400' : 
                    'text-purple-400'
                  }`}>
                    {log.event.padEnd(25, ' ')}
                  </span>
                  <span className="text-slate-300 break-all">{log.details}</span>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
};
