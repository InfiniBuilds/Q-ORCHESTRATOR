import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Mock Data Generators for missing endpoints
export const mockEventLogs = [
  { id: 1, timestamp: new Date().toISOString(), event: 'SYSTEM_BOOT', details: 'Orchestrator initialized.' },
];

export const addMockLog = (event: string, details: string) => {
  mockEventLogs.unshift({
    id: mockEventLogs.length + 1,
    timestamp: new Date().toISOString(),
    event,
    details,
  });
};

// API Services
export const OrchestratorAPI = {
  orchestrate: async (data: any) => {
    try {
      const response = await api.post('/orchestrate', data);
      addMockLog('ORCHESTRATION_REQUEST', `Domain: ${data.domain}, Status: SUCCESS`);
      return response.data;
    } catch (error) {
      addMockLog('ORCHESTRATION_ERROR', 'Failed to orchestrate request.');
      throw error;
    }
  },
};

export const BankingAPI = {
  simulate: async (data: any) => {
    try {
      const response = await api.post('/banking/simulate', data);
      addMockLog('BANKING_SIMULATION', `Transaction: ${data.transaction_type}, Valid: ${response.data.signature_verified}`);
      return response.data;
    } catch (error) {
      addMockLog('BANKING_ERROR', 'Failed banking simulation.');
      throw error;
    }
  },
};

export const IoTAPI = {
  simulate: async (data: any) => {
    try {
      const response = await api.post('/iot/simulate', data);
      addMockLog('IOT_SIMULATION', `Device: ${data.device_type}, Security: ${response.data.security_rank}`);
      return response.data;
    } catch (error) {
      addMockLog('IOT_ERROR', 'Failed IoT simulation.');
      throw error;
    }
  },
};

export const AnalyticsAPI = {
  getSummary: async () => {
    const response = await api.get('/analytics/summary');
    return response.data;
  },
};
