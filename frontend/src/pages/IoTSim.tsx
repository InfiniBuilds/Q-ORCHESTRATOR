import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, Activity, ShieldAlert, Wifi, Battery } from 'lucide-react';
import { IoTAPI } from '@/api';

const DEVICES = [
  { id: 'SMART_METER', name: 'Smart Power Meter', type: 'SMART_METER', color: 'text-amber-400', bg: 'bg-amber-400/20' },
  { id: 'CAMERA', name: 'Security Camera', type: 'CAMERA', color: 'text-purple-400', bg: 'bg-purple-400/20' },
  { id: 'MEDICAL_SENSOR', name: 'Pacemaker Monitor', type: 'MEDICAL_SENSOR', color: 'text-red-400', bg: 'bg-red-400/20' },
  { id: 'INDUSTRIAL_SENSOR', name: 'SCADA Pressure Sensor', type: 'INDUSTRIAL_SENSOR', color: 'text-cyan-400', bg: 'bg-cyan-400/20' },
];

export const IoTSim: React.FC = () => {
  const [activeDevice, setActiveDevice] = useState(DEVICES[0]);
  const [battery, setBattery] = useState(85);
  const [trusted, setTrusted] = useState(true);
  const [anomaly, setAnomaly] = useState(false);
  const [streamData, setStreamData] = useState<any[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (isStreaming) {
      interval = setInterval(async () => {
        try {
          const res = await IoTAPI.simulate({
            device_type: activeDevice.type,
            battery_level: battery / 100,
            trusted_device: trusted,
            anomaly_detected: anomaly,
          });
          
          setStreamData(prev => [
            { timestamp: new Date().toLocaleTimeString(), data: res },
            ...prev.slice(0, 4) // keep last 5
          ]);
        } catch (error) {
          console.error("Stream error", error);
        }
      }, 2500);
    }
    return () => clearInterval(interval);
  }, [isStreaming, activeDevice, battery, trusted, anomaly]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Cpu className="text-cyan-400" />
            IoT Telemetry Simulation
          </h2>
          <p className="text-slate-400">Resource-constrained orchestration with real-time stream processing.</p>
        </div>
        <button 
          onClick={() => setIsStreaming(!isStreaming)}
          className={`px-6 py-2 rounded-full font-bold flex items-center gap-2 transition-all ${
            isStreaming 
              ? 'bg-red-500/20 text-red-400 border border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.3)]' 
              : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.3)]'
          }`}
        >
          {isStreaming ? (
            <><div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" /> Stop Stream</>
          ) : (
            <><Wifi size={18} /> Start Stream</>
          )}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1 space-y-4">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Select Device</h3>
          {DEVICES.map(device => (
            <motion.div
              key={device.id}
              whileHover={{ scale: 1.02 }}
              onClick={() => setActiveDevice(device)}
              className={`p-4 rounded-xl border cursor-pointer transition-all ${
                activeDevice.id === device.id 
                  ? 'bg-slate-800 border-cyan-500 shadow-[0_0_15px_rgba(14,165,233,0.2)]' 
                  : 'bg-slate-900/50 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${device.bg} ${device.color}`}>
                  <Activity size={20} />
                </div>
                <div className="flex-1">
                  <p className="font-medium text-slate-200">{device.name}</p>
                  <p className="text-xs text-slate-400">{device.type}</p>
                </div>
              </div>
            </motion.div>
          ))}

          <div className="glass-card p-4 rounded-xl border border-slate-800 mt-6 space-y-4">
             <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Device Context</h3>
             
             <div>
               <div className="flex justify-between text-xs mb-1">
                 <span className="text-slate-400 flex items-center gap-1"><Battery size={14} /> Battery</span>
                 <span className={battery > 20 ? 'text-emerald-400' : 'text-red-400'}>{battery}%</span>
               </div>
               <input 
                 type="range" min="5" max="100" 
                 value={battery} onChange={(e) => setBattery(parseInt(e.target.value))}
                 className="w-full accent-cyan-500"
               />
             </div>

             <div className="flex items-center justify-between">
                <span className="text-sm text-slate-300">Trusted Network</span>
                <button 
                  className={`w-10 h-5 rounded-full transition-colors relative ${trusted ? 'bg-cyan-500' : 'bg-slate-700'}`}
                  onClick={() => setTrusted(!trusted)}
                >
                  <div className={`w-3 h-3 bg-white rounded-full absolute top-1 transition-all ${trusted ? 'left-6' : 'left-1'}`} />
                </button>
             </div>

             <div className="flex items-center justify-between">
                <span className="text-sm text-slate-300 flex items-center gap-1"><ShieldAlert size={14} className="text-red-400" /> Anomaly</span>
                <button 
                  className={`w-10 h-5 rounded-full transition-colors relative ${anomaly ? 'bg-red-500' : 'bg-slate-700'}`}
                  onClick={() => setAnomaly(!anomaly)}
                >
                  <div className={`w-3 h-3 bg-white rounded-full absolute top-1 transition-all ${anomaly ? 'left-6' : 'left-1'}`} />
                </button>
             </div>
          </div>
        </div>

        <div className="lg:col-span-3">
          <div className="glass-card p-6 rounded-xl border border-slate-800 h-full flex flex-col">
            <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
              <Activity className="text-cyan-400" size={20} />
              Live Telemetry Stream
            </h3>
            
            <div className="flex-1 bg-slate-950 rounded-lg border border-slate-800 p-4 font-mono text-sm overflow-hidden relative">
               {!isStreaming && streamData.length === 0 && (
                 <div className="absolute inset-0 flex items-center justify-center text-slate-500">
                   Waiting for stream to start...
                 </div>
               )}
               <div className="space-y-3">
                 <AnimatePresence>
                   {streamData.map((packet, idx) => (
                     <motion.div 
                       key={idx + packet.timestamp}
                       initial={{ opacity: 0, x: -20 }}
                       animate={{ opacity: 1, x: 0 }}
                       exit={{ opacity: 0, scale: 0.9 }}
                       className="bg-slate-900 border border-slate-800 p-3 rounded flex gap-4 items-center"
                     >
                       <div className="text-cyan-500 text-xs w-20">{packet.timestamp}</div>
                       <div className="flex-1 flex gap-4 text-xs">
                          <span className="text-purple-400">[{packet.data.selected_profile}]</span>
                          <span className={packet.data.signature_verified ? 'text-emerald-400' : 'text-red-400'}>SIG:{packet.data.signature_verified ? 'OK' : 'FAIL'}</span>
                          <span className="text-slate-400">CIPHER_SIZE:{packet.data.ciphertext_size}B</span>
                          <span className="text-amber-400">DATA:{packet.data.recovered_plaintext}</span>
                       </div>
                     </motion.div>
                   ))}
                 </AnimatePresence>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
