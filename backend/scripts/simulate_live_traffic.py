import requests
import time
import random
import json

# 1. UPDATED: Pointing to the exact route defined in your APIRouter
# (Note: If your main.py includes this router with a prefix like "/api", change this to "/api/orchestrate")
API_URL = "http://127.0.0.1:8000/orchestrate"

def generate_iot_payload():
    """Simulates a constrained IoT edge sensor mapping to OrchestrationRequest."""
    return {
        "domain": "IOT", # Ensure this matches your Domain Enum
        "criticality": 0.2,
        "sensitivity": 0.2,
        "anomaly_score": 0.0,
        "trust_deficit": 0.1,
        "exposure": 0.8,
        "cpu_constraint": random.uniform(0.8, 0.99),     # Simulating overloaded CPU (80-99%)
        "memory_constraint": 0.7,
        "energy_constraint": random.uniform(0.8, 0.99),  # Simulating a dying battery
        "bandwidth_constraint": 0.6,
        "latency_constraint": 0.8,
        "plaintext": "SENSOR_PING: TEMP 22C, HUMIDITY 45%"
    }

def generate_banking_payload():
    """Simulates a high-value interbank transfer mapping to OrchestrationRequest."""
    return {
        "domain": "BANKING",
        "criticality": 0.9,
        "sensitivity": 1.0,
        "anomaly_score": 0.0,
        "trust_deficit": 0.2,
        "exposure": 0.2,
        "cpu_constraint": random.uniform(0.1, 0.3), # Server has plenty of CPU
        "memory_constraint": 0.2,
        "energy_constraint": 0.0,                   # Server is plugged into the wall
        "bandwidth_constraint": 0.1,
        "latency_constraint": 0.1,
        "plaintext": "TRANSFER: 1500000 INR, ACCT_DEST: 9876543210"
    }

print("--- STARTING Q-ORCHESTRATOR LIVE TRAFFIC SIMULATOR ---")

for i in range(1, 6):
    print(f"\n--- Request #{i} ---")
    
    is_banking = random.choice([True, False])
    payload = generate_banking_payload() if is_banking else generate_iot_payload()
    
    print(f"Sending Context: {payload['domain']} | Criticality: {payload['criticality']} | Energy Constraint: {payload['energy_constraint']}")
    
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            # Mapping directly to the OrchestrationResponse schema you provided
            print(f"[✓] Orchestrator Decision: {result.get('selected_profile')}")
            print(f"    Security Rank: {result.get('security_rank')}")
            print(f"    Resource Capability: {result.get('resource_capability')}")
            print(f"    Ciphertext Size: {result.get('ciphertext_size')} bytes")
            print(f"[✓] Processing Time: {round((end_time - start_time) * 1000, 2)} ms")
        else:
            print(f"[X] API Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("[X] Connection Failed. Is your Uvicorn server running?")
        break
        
    time.sleep(1.5)