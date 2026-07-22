
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';

import { Overview } from './pages/Overview';
import { BankingSim } from './pages/BankingSim';
import { IoTSim } from './pages/IoTSim';
import { EncryptionFlow } from './pages/EncryptionFlow';
import { SecurityEngine } from './pages/SecurityEngine';
import { Benchmarks } from './pages/Benchmarks';
import { Algorithms } from './pages/Algorithms';
import { EventLogs } from './pages/EventLogs';
import { Architecture } from './pages/Architecture';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Overview />} />
          <Route path="banking" element={<BankingSim />} />
          <Route path="iot" element={<IoTSim />} />
          <Route path="encryption" element={<EncryptionFlow />} />
          <Route path="security-engine" element={<SecurityEngine />} />
          <Route path="benchmarks" element={<Benchmarks />} />
          <Route path="algorithms" element={<Algorithms />} />
          <Route path="logs" element={<EventLogs />} />
          <Route path="architecture" element={<Architecture />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
