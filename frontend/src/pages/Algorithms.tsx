import React from 'react';
import { List } from 'lucide-react';

const ALGORITHMS = [
  {
    category: 'Key Encapsulation Mechanisms (KEM)',
    items: [
      { name: 'ML-KEM-512', security: 'AES-128 Eq.', pkSize: 800, ctSize: 768, speed: 'Very Fast', status: 'NIST Standard' },
      { name: 'ML-KEM-768', security: 'AES-192 Eq.', pkSize: 1184, ctSize: 1088, speed: 'Fast', status: 'NIST Standard' },
      { name: 'ML-KEM-1024', security: 'AES-256 Eq.', pkSize: 1568, ctSize: 1568, speed: 'Moderate', status: 'NIST Standard' },
      { name: 'FrodoKEM-640', security: 'AES-128 Eq.', pkSize: 9616, ctSize: 9720, speed: 'Slow', status: 'Alternate' },
    ]
  },
  {
    category: 'Digital Signature Algorithms (DSA)',
    items: [
      { name: 'ML-DSA-44', security: 'AES-128 Eq.', pkSize: 1312, sigSize: 2420, speed: 'Fast', status: 'NIST Standard' },
      { name: 'ML-DSA-65', security: 'AES-192 Eq.', pkSize: 1952, sigSize: 3293, speed: 'Moderate', status: 'NIST Standard' },
      { name: 'ML-DSA-87', security: 'AES-256 Eq.', pkSize: 2592, sigSize: 4595, speed: 'Slow', status: 'NIST Standard' },
      { name: 'SLH-DSA (SPHINCS+)', security: 'Varies', pkSize: 32, sigSize: 17088, speed: 'Very Slow', status: 'NIST Standard' },
    ]
  },
  {
    category: 'Classic Algorithms (Vulnerable to Shor\'s Algorithm)',
    items: [
      { name: 'RSA-3072', security: 'Legacy 128-bit', pkSize: 384, ctSize: 384, speed: 'Slow Gen, Fast Enc', status: 'Phase Out' },
      { name: 'ECDH (P-256)', security: 'Legacy 128-bit', pkSize: 32, ctSize: 32, speed: 'Very Fast', status: 'Phase Out' },
    ]
  }
];

export const Algorithms: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <List className="text-cyan-400" />
            Algorithm Comparison
          </h2>
          <p className="text-slate-400">Detailed specifications of supported cryptographic algorithms.</p>
        </div>
      </div>

      <div className="space-y-8">
        {ALGORITHMS.map((group, idx) => (
          <div key={idx} className="glass-card p-6 rounded-xl border border-slate-800">
            <h3 className="text-lg font-semibold text-slate-200 mb-4">{group.category}</h3>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 text-sm">
                    <th className="pb-3 font-medium">Algorithm</th>
                    <th className="pb-3 font-medium">Security Level</th>
                    <th className="pb-3 font-medium">Public Key Size</th>
                    <th className="pb-3 font-medium">Cipher/Sig Size</th>
                    <th className="pb-3 font-medium">Performance</th>
                    <th className="pb-3 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {group.items.map((item, i) => (
                    <tr key={i} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                      <td className="py-4 text-slate-200 font-medium">{item.name}</td>
                      <td className="py-4">
                        <span className={`px-2 py-1 rounded text-xs ${item.security.includes('Legacy') ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                          {item.security}
                        </span>
                      </td>
                      <td className="py-4 text-slate-300 font-mono">{item.pkSize} B</td>
                      <td className="py-4 text-slate-300 font-mono">{(item as any).ctSize || (item as any).sigSize} B</td>
                      <td className="py-4 text-slate-400">{item.speed}</td>
                      <td className="py-4">
                        <span className={`px-2 py-1 rounded text-xs ${item.status === 'Phase Out' ? 'bg-amber-500/20 text-amber-400' : 'bg-cyan-500/20 text-cyan-400'}`}>
                          {item.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
