import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Landmark, ShieldCheck, Fingerprint, Lock, Zap, Key } from 'lucide-react';
import { BankingAPI } from '@/api';

export const BankingSim: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [formData, setFormData] = useState({
    transaction_type: 'HIGH_VALUE_TRANSFER',
    amount: 50000,
    trusted_device: false,
    authenticated: true
  });

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await BankingAPI.simulate(formData);
      setTimeout(() => {
        setResult(res);
        setLoading(false);
      }, 1500); // Artificial delay to show animation
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Landmark className="text-cyan-400" />
            Banking Transaction Simulation
          </h2>
          <p className="text-slate-400">Simulate secure transactions protected by ML-KEM and ML-DSA.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Input Form */}
        <div className="lg:col-span-1">
          <div className="glass-card p-6 rounded-xl border border-slate-800">
            <h3 className="text-lg font-semibold text-slate-200 mb-4">Transaction Details</h3>
            <form onSubmit={handleSimulate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Transaction Type</label>
                <select 
                  className="w-full bg-slate-900 border border-slate-700 rounded-md p-2 text-slate-200 focus:outline-none focus:border-cyan-500"
                  value={formData.transaction_type}
                  onChange={e => setFormData({...formData, transaction_type: e.target.value})}
                >
                  <option value="BALANCE_CHECK">Balance Check</option>
                  <option value="LOCAL_TRANSFER">Local Transfer</option>
                  <option value="INTERNATIONAL_TRANSFER">International Transfer</option>
                  <option value="BILL_PAYMENT">Bill Payment</option>
                  <option value="LOAN_PAYMENT">Loan Payment</option>
                  <option value="HIGH_VALUE_TRANSFER">High Value Transfer</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Amount ($)</label>
                <input 
                  type="number"
                  className="w-full bg-slate-900 border border-slate-700 rounded-md p-2 text-slate-200 focus:outline-none focus:border-cyan-500"
                  value={formData.amount}
                  onChange={e => setFormData({...formData, amount: Number(e.target.value)})}
                />
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-900/50 border border-slate-700 rounded-md">
                <span className="text-sm text-slate-300">Trusted Device</span>
                <button 
                  type="button"
                  className={`w-12 h-6 rounded-full transition-colors relative ${formData.trusted_device ? 'bg-cyan-500' : 'bg-slate-700'}`}
                  onClick={() => setFormData({...formData, trusted_device: !formData.trusted_device})}
                >
                  <motion.div 
                    className="w-4 h-4 bg-white rounded-full absolute top-1"
                    animate={{ left: formData.trusted_device ? '26px' : '4px' }}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-900/50 border border-slate-700 rounded-md">
                <span className="text-sm text-slate-300">User Authenticated</span>
                <button 
                  type="button"
                  className={`w-12 h-6 rounded-full transition-colors relative ${formData.authenticated ? 'bg-emerald-500' : 'bg-slate-700'}`}
                  onClick={() => setFormData({...formData, authenticated: !formData.authenticated})}
                >
                  <motion.div 
                    className="w-4 h-4 bg-white rounded-full absolute top-1"
                    animate={{ left: formData.authenticated ? '26px' : '4px' }}
                  />
                </button>
              </div>

              <button 
                type="submit" 
                disabled={loading}
                className="w-full py-3 mt-4 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 rounded-md font-bold text-white shadow-[0_0_15px_rgba(14,165,233,0.4)] transition-all disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Execute Transaction'}
              </button>
            </form>
          </div>
        </div>

        {/* Results & Animation */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <AnimatePresence mode="wait">
            {loading ? (
              <motion.div 
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="glass-card p-12 rounded-xl border border-slate-800 flex-1 flex flex-col items-center justify-center text-cyan-400"
              >
                <div className="relative w-32 h-32 flex items-center justify-center">
                  <motion.div 
                    className="absolute inset-0 border-4 border-t-cyan-500 border-r-purple-500 border-b-emerald-500 border-l-transparent rounded-full"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                  />
                  <Lock size={40} className="animate-pulse" />
                </div>
                <h3 className="mt-8 text-xl font-mono text-glow">Negotiating Post-Quantum Keys...</h3>
                <p className="text-slate-400 mt-2">ML-KEM Key Encapsulation in progress</p>
              </motion.div>
            ) : result ? (
              <motion.div 
                key="result"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-6"
              >
                <div className="glass-card p-6 rounded-xl border border-emerald-500/50 shadow-[0_0_20px_rgba(16,185,129,0.15)] col-span-full">
                  <div className="flex items-center gap-4 text-emerald-400 mb-4">
                    <div className="p-3 bg-emerald-500/20 rounded-full">
                      <ShieldCheck size={32} />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold">Transaction Secured</h3>
                      <p className="text-slate-400">Quantum-resistant cryptographic pipeline completed.</p>
                    </div>
                  </div>
                </div>

                <ResultCard title="Security Profile" value={result.selected_profile} icon={ShieldCheck} color="text-cyan-400" />
                <ResultCard title="Required Security Rank" value={result.security_rank} icon={Zap} color="text-purple-400" />
                <ResultCard title="Signature Verified" value={result.signature_verified ? 'TRUE (ML-DSA)' : 'FALSE'} icon={Fingerprint} color={result.signature_verified ? 'text-emerald-400' : 'text-red-400'} />
                <ResultCard title="Session Key Size" value={`${result.session_key_size} bytes`} icon={Key} color="text-amber-400" />
                
                <div className="glass-card p-6 rounded-xl border border-slate-800 col-span-full font-mono text-sm">
                  <h4 className="text-slate-400 mb-2">Recovered Plaintext:</h4>
                  <div className="bg-slate-900 p-4 rounded border border-slate-700 text-emerald-300 break-all">
                    {result.recovered_plaintext}
                  </div>
                </div>
              </motion.div>
            ) : (
              <div className="glass-card p-12 rounded-xl border border-slate-800 flex-1 flex flex-col items-center justify-center opacity-50">
                <Landmark size={64} className="text-slate-600 mb-4" />
                <p className="text-slate-400">Enter transaction details and execute to view cryptographic workflow.</p>
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

function ResultCard({ title, value, icon: Icon, color }: { title: string, value: string, icon: any, color: string }) {
  return (
    <div className="glass-card p-6 rounded-xl border border-slate-800 flex items-start gap-4">
      <Icon size={24} className={`${color} mt-1`} />
      <div>
        <p className="text-sm text-slate-400">{title}</p>
        <p className={`text-lg font-bold font-mono mt-1 ${color}`}>{value}</p>
      </div>
    </div>
  );
}
