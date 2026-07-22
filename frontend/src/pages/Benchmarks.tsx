import React from 'react';
import { BarChart3, Clock, Zap } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

const perfData = [
  { name: 'RSA-3072', keyGen: 120, encrypt: 0.1, decrypt: 2.5, sign: 2.8, verify: 0.1 },
  { name: 'ECC (P-256)', keyGen: 0.2, encrypt: 0, decrypt: 0, sign: 0.4, verify: 0.8 },
  { name: 'ML-KEM-768', keyGen: 0.05, encrypt: 0.03, decrypt: 0.04, sign: 0, verify: 0 },
  { name: 'ML-DSA-65', keyGen: 0.15, encrypt: 0, decrypt: 0, sign: 0.8, verify: 0.2 },
  { name: 'Hybrid (ECC+KEM)', keyGen: 0.25, encrypt: 0.03, decrypt: 0.04, sign: 0, verify: 0 },
];

const latencyData = [
  { clients: 10, classic: 45, pqc: 48, hybrid: 55 },
  { clients: 50, classic: 80, pqc: 85, hybrid: 98 },
  { clients: 100, classic: 150, pqc: 155, hybrid: 180 },
  { clients: 500, classic: 450, pqc: 480, hybrid: 520 },
  { clients: 1000, classic: 850, pqc: 890, hybrid: 980 },
];

export const Benchmarks: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <BarChart3 className="text-cyan-400" />
            Performance Benchmarks
          </h2>
          <p className="text-slate-400">Comparing Classic vs Post-Quantum vs Hybrid architectures.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Execution Time Chart */}
        <div className="glass-card p-6 rounded-xl border border-slate-800">
          <h3 className="text-lg font-semibold text-slate-200 mb-6 flex items-center gap-2">
            <Clock className="text-amber-400" size={20} />
            Cryptographic Operation Latency (ms)
          </h3>
          <div className="h-[350px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={perfData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '0.5rem', color: '#f8fafc' }}
                  itemStyle={{ color: '#f8fafc' }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Bar dataKey="keyGen" name="Key Gen" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="encrypt" name="Encapsulate/Encrypt" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                <Bar dataKey="decrypt" name="Decapsulate/Decrypt" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* System Scalability Chart */}
        <div className="glass-card p-6 rounded-xl border border-slate-800">
          <h3 className="text-lg font-semibold text-slate-200 mb-6 flex items-center gap-2">
            <Zap className="text-purple-400" size={20} />
            System Latency Under Load (ms)
          </h3>
          <div className="h-[350px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={latencyData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="clients" stroke="#94a3b8" fontSize={12} label={{ value: 'Concurrent Clients', position: 'insideBottom', offset: -5, fill: '#94a3b8' }} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '0.5rem', color: '#f8fafc' }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Line type="monotone" dataKey="classic" name="Classic (RSA/ECC)" stroke="#64748b" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="pqc" name="PQC (ML-KEM/DSA)" stroke="#10b981" strokeWidth={3} dot={{ r: 6 }} />
                <Line type="monotone" dataKey="hybrid" name="Hybrid Orchestrator" stroke="#0ea5e9" strokeWidth={3} dot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
};
