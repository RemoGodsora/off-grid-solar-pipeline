import json
import random
import time
from datetime import datetime, timezone

def generate_telemetry(num_records=100):
    """Simulates real-world electrical telemetry from an off-grid solar array."""
    payloads = []
    
    for _ in range(num_records):
        # Base physical parameters
        device_id = f"array_{random.randint(1, 50):02d}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Simulate realistic electrical physics
        is_faulting = random.random() < 0.05  # 5% chance of an anomaly
        
        if is_faulting:
            voltage = round(random.uniform(35.0, 42.0), 2)     # Voltage drop
            current = round(random.uniform(15.0, 25.0), 2)     # High load spike
            temperature = round(random.uniform(85.0, 105.0), 2) # Overheating
            battery_soc = round(random.uniform(20.0, 40.0), 2) # Low battery
        else:
            voltage = round(random.uniform(47.5, 48.5), 2)     # Stable 48V system
            current = round(random.uniform(5.0, 12.0), 2)      # Normal load
            temperature = round(random.uniform(35.0, 55.0), 2) # Safe operating temp
            battery_soc = round(random.uniform(80.0, 100.0), 2)# Healthy battery
            
        payloads.append({
            "device_id": device_id,
            "timestamp": timestamp,
            "voltage": voltage,
            "current": current,
            "inverter_temp_c": temperature,
            "battery_soc_pct": battery_soc,
            "is_faulting": is_faulting
        })
        
    return payloads

if __name__ == "__main__":
    print("Initializing Edge Sensor Array...")
    data = generate_telemetry(500) # Generate 500 telemetry pings
    
    # Dump to a local buffer file (simulating edge storage)
    output_file = "raw_telemetry_buffer.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"SUCCESS: {len(data)} packets safely written to {output_file}.")