import React, { useState } from 'react';
import { Activity, Shield } from 'lucide-react';
import { OrchestratorAPI } from '@/api';

export const SecurityEngine: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [formData, setFormData] = useState({
    domain: 'FINANCE',
    criticality: 0.9,
    sensitivity: 0.95,
    anomaly_score: 0.1,
    trust_deficit: 0.2,
    exposure: 0.3,
    cpu_constraint: 0.8,
    memory_constraint: 0.7,
    energy_constraint: 1.0,
    bandwidth_constraint: 0.9,
    latency_constraint: 0.9,
    plaintext: 'Test Data'
  });

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await OrchestratorAPI.orchestrate(formData);
      setResult(res);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSlider = (field: string, value: string) => {
    setFormData({ ...formData, [field]: parseFloat(value) });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Activity className="text-cyan-400" />
            Security Requirement Engine
          </h2>
          <p className="text-slate-400">Dynamically compute security profiles based on context and constraints.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6 rounded-xl border border-slate-800">
          <form onSubmit={handleSimulate} className="space-y-6">
            
            <div>
               <label className="block text-sm font-medium text-slate-400 mb-2">Domain</label>
               <select 
                  className="w-full bg-slate-900 border border-slate-700 rounded-md p-2 text-slate-200 focus:outline-none focus:border-cyan-500"
                  value={formData.domain}
                  onChange={e => setFormData({...formData, domain: e.target.value})}
               >
                 <option value="FINANCE">Finance</option>
                 <option value="HEALTHCARE">Healthcare</option>
                 <option value="IOT">IoT</option>
                 <option value="GOVERNMENT">Government</option>
               </select>
            </div>

            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-slate-300 border-b border-slate-800 pb-2">Security Context</h3>
              <SliderInput label="Criticality" value={formData.criticality} onChange={(v) => handleSlider('criticality', v)} color="accent-red-500" />
              <SliderInput label="Sensitivity" value={formData.sensitivity} onChange={(v) => handleSlider('sensitivity', v)} color="accent-amber-500" />
              <SliderInput label="Anomaly Score" value={formData.anomaly_score} onChange={(v) => handleSlider('anomaly_score', v)} color="accent-purple-500" />
              <SliderInput label="Trust Deficit" value={formData.trust_deficit} onChange={(v) => handleSlider('trust_deficit', v)} color="accent-rose-500" />
              <SliderInput label="Exposure" value={formData.exposure} onChange={(v) => handleSlider('exposure', v)} color="accent-orange-500" />
            </div>

            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-slate-300 border-b border-slate-800 pb-2">Resource Constraints</h3>
              <SliderInput label="CPU Availability" value={formData.cpu_constraint} onChange={(v) => handleSlider('cpu_constraint', v)} color="accent-cyan-500" />
              <SliderInput label="Memory" value={formData.memory_constraint} onChange={(v) => handleSlider('memory_constraint', v)} color="accent-cyan-500" />
              <SliderInput label="Energy" value={formData.energy_constraint} onChange={(v) => handleSlider('energy_constraint', v)} color="accent-emerald-500" />
              <SliderInput label="Bandwidth" value={formData.bandwidth_constraint} onChange={(v) => handleSlider('bandwidth_constraint', v)} color="accent-blue-500" />
              <SliderInput label="Latency Tolerance" value={formData.latency_constraint} onChange={(v) => handleSlider('latency_constraint', v)} color="accent-indigo-500" />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="w-full py-3 mt-4 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 rounded-md font-bold text-white shadow-[0_0_15px_rgba(168,85,247,0.4)] transition-all disabled:opacity-50"
            >
              {loading ? 'Computing Engine...' : 'Compute Security Profile'}
            </button>
          </form>
        </div>

        <div>
           {result ? (
             <div className="glass-card p-6 rounded-xl border border-cyan-500 shadow-[0_0_20px_rgba(14,165,233,0.15)] space-y-6 sticky top-6">
               <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
                 <Shield className="text-cyan-400" size={32} />
                 <div>
                   <h3 className="text-xl font-bold text-slate-100">Engine Result</h3>
                   <p className="text-sm text-cyan-400">Profile Computed Successfully</p>
                 </div>
               </div>

               <div className="space-y-4">
                  <ResultRow label="Selected Profile" value={result.selected_profile} highlight />
                  <ResultRow label="Security Rank" value={result.security_rank} />
                  <ResultRow label="Resource Capability" value={result.resource_capability} />
                  
                  <div className="pt-4 border-t border-slate-800">
                    <h4 className="text-sm font-semibold text-slate-400 mb-3">Cryptographic Output</h4>
                    <ResultRow label="Signature Valid" value={result.signature_verified ? 'Yes' : 'No'} />
                    <ResultRow label="Ciphertext Size" value={`${result.ciphertext_size} bytes`} />
                    <ResultRow label="Session Key Size" value={`${result.session_key_size} bytes`} />
                  </div>
               </div>
             </div>
           ) : (
             <div className="glass-card p-12 rounded-xl border border-slate-800 h-full flex flex-col items-center justify-center text-center opacity-50 sticky top-6">
                <Activity size={64} className="text-slate-600 mb-4" />
                <h3 className="text-xl text-slate-400 mb-2">Awaiting Parameters</h3>
                <p className="text-sm text-slate-500">Adjust the context and resource sliders and click compute to see the engine's dynamic decision making.</p>
             </div>
           )}
        </div>
      </div>
    </div>
  );
};

function SliderInput({ label, value, onChange, color }: { label: string, value: number, onChange: (v: string) => void, color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-300 font-mono">{(value * 100).toFixed(0)}%</span>
      </div>
      <input 
        type="range" 
        min="0" max="1" step="0.05"
        value={value} 
        onChange={(e) => onChange(e.target.value)}
        className={`w-full ${color}`}
      />
    </div>
  );
}

function ResultRow({ label, value, highlight = false }: { label: string, value: string, highlight?: boolean }) {
  return (
    <div className="flex justify-between items-center p-3 bg-slate-900/50 rounded-lg border border-slate-800/50">
      <span className="text-sm text-slate-400">{label}</span>
      <span className={`font-mono font-bold ${highlight ? 'text-cyan-400 text-lg' : 'text-slate-200 text-sm'}`}>{value}</span>
    </div>
  );
}
