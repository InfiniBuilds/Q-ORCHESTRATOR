import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldCheck, FileText, Key, Lock, ArrowRight, CheckCircle2 } from 'lucide-react';

const STAGES = [
  { id: 1, title: 'Plaintext Input', icon: FileText, desc: 'Original sensitive data', color: 'text-slate-300' },
  { id: 2, title: 'Key Generation', icon: Key, desc: 'ML-KEM Keypair Gen', color: 'text-amber-400' },
  { id: 3, title: 'Key Encapsulation', icon: Lock, desc: 'Shared Secret Derivation', color: 'text-purple-400' },
  { id: 4, title: 'AES-GCM Encryption', icon: ShieldCheck, desc: 'Symmetric Encryption', color: 'text-cyan-400' },
  { id: 5, title: 'Digital Signature', icon: FileText, desc: 'ML-DSA Signing', color: 'text-emerald-400' },
  { id: 6, title: 'Verification', icon: CheckCircle2, desc: 'Signature Validation', color: 'text-blue-400' },
  { id: 7, title: 'Decryption', icon: FileText, desc: 'Recovered Plaintext', color: 'text-slate-300' },
];

export const EncryptionFlow: React.FC = () => {
  const [activeStage, setActiveStage] = useState(1);

  const nextStage = () => {
    if (activeStage < STAGES.length) setActiveStage(prev => prev + 1);
  };

  const resetFlow = () => setActiveStage(1);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <ShieldCheck className="text-cyan-400" />
            Post-Quantum Encryption Workflow
          </h2>
          <p className="text-slate-400">Step-by-step visualization of the hybrid cryptographic pipeline.</p>
        </div>
        <div className="flex gap-4">
          <button onClick={resetFlow} className="px-4 py-2 rounded border border-slate-700 hover:bg-slate-800 text-slate-300 transition-colors">Reset</button>
          <button 
            onClick={nextStage} 
            disabled={activeStage === STAGES.length}
            className="px-4 py-2 rounded bg-cyan-600 hover:bg-cyan-500 text-white font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            Next Stage <ArrowRight size={16} />
          </button>
        </div>
      </div>

      <div className="glass-card p-8 rounded-xl border border-slate-800 relative overflow-hidden min-h-[500px] flex flex-col items-center">
        
        {/* Progress Bar */}
        <div className="w-full flex justify-between relative mb-16 px-4">
          <div className="absolute top-1/2 left-8 right-8 h-1 bg-slate-800 -translate-y-1/2 z-0" />
          <motion.div 
            className="absolute top-1/2 left-8 h-1 bg-cyan-500 -translate-y-1/2 z-0 transition-all duration-500" 
            style={{ width: `calc(${(activeStage - 1) / (STAGES.length - 1) * 100}% - 2rem)` }}
          />
          
          {STAGES.map((stage) => (
            <div key={stage.id} className="relative z-10 flex flex-col items-center gap-2">
              <div 
                className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-colors duration-500 ${
                  activeStage >= stage.id 
                    ? 'bg-slate-900 border-cyan-500 text-cyan-400 shadow-[0_0_10px_rgba(14,165,233,0.5)]' 
                    : 'bg-slate-900 border-slate-700 text-slate-500'
                }`}
              >
                <stage.icon size={20} />
              </div>
              <span className={`text-xs font-medium absolute -bottom-6 whitespace-nowrap ${
                activeStage >= stage.id ? 'text-cyan-400' : 'text-slate-500'
              }`}>
                {stage.title}
              </span>
            </div>
          ))}
        </div>

        {/* Stage Content */}
        <div className="flex-1 w-full max-w-3xl flex items-center justify-center relative mt-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeStage}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="w-full"
            >
              <div className="bg-slate-900/80 border border-slate-700 p-8 rounded-xl text-center shadow-xl backdrop-blur-md">
                <div className={`w-20 h-20 mx-auto rounded-full bg-slate-800/80 border border-slate-700 flex items-center justify-center mb-6 shadow-lg`}>
                   {React.createElement(STAGES[activeStage - 1].icon, { size: 40, className: STAGES[activeStage - 1].color })}
                </div>
                <h3 className="text-2xl font-bold text-slate-100 mb-2">{STAGES[activeStage - 1].title}</h3>
                <p className="text-slate-400 mb-8">{STAGES[activeStage - 1].desc}</p>
                
                {/* Dynamic Content based on stage */}
                <div className="bg-slate-950 p-6 rounded-lg border border-slate-800 text-left font-mono text-sm overflow-hidden relative">
                  {activeStage === 1 && (
                    <div className="text-emerald-400">{"{ \"message\": \"Highly confidential quantum data\" }"}</div>
                  )}
                  {activeStage === 2 && (
                    <div className="text-amber-400 space-y-2">
                      <p>Generating ML-KEM Keypair...</p>
                      <p className="text-slate-500 truncate">pk: 0x8a9b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b...</p>
                      <p className="text-slate-500 truncate">sk: [REDACTED]</p>
                    </div>
                  )}
                  {activeStage === 3 && (
                    <div className="text-purple-400 space-y-2">
                      <p>Encapsulating Secret...</p>
                      <p className="truncate">Ciphertext (c): 0x1f2e3d4c5b6a7988...</p>
                      <p className="truncate text-cyan-300">Shared Secret (K): 0xffeeddccbbaa9988...</p>
                    </div>
                  )}
                  {activeStage === 4 && (
                    <div className="text-cyan-400 space-y-2">
                      <p>Encrypting with AES-256-GCM using Derived Key (K)...</p>
                      <p className="truncate text-slate-400 mt-2">0x4b3a291807f6e5d4c3b2a1908f7e6d5c4b3a291807f6e5d4...</p>
                    </div>
                  )}
                  {activeStage === 5 && (
                    <div className="text-emerald-400 space-y-2">
                      <p>Signing ciphertext with ML-DSA (Dilithium)...</p>
                      <p className="truncate text-slate-400 mt-2">Sig: 0x9876543210abcdef9876543210abcdef...</p>
                    </div>
                  )}
                  {activeStage === 6 && (
                    <div className="text-blue-400 flex items-center justify-center py-4">
                      <CheckCircle2 size={32} className="mr-3" />
                      <span className="text-lg">Signature Verified Successfully</span>
                    </div>
                  )}
                  {activeStage === 7 && (
                    <div className="text-emerald-400">
                      <p className="text-slate-400 mb-2">// Decrypted payload</p>
                      {"{ \"message\": \"Highly confidential quantum data\" }"}
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};
