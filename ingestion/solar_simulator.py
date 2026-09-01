import json
import random
from datetime import datetime, timedelta

def generate_historical_telemetry(num_records=500):
    """Simulates 7 days of electrical telemetry with injected hardware faults."""
    payloads = []
    
    # Loop backwards to simulate historical hardware operation
    for i in range(num_records):
        # Stagger the timestamps across the last 7 days
        simulated_time = datetime.now() - timedelta(minutes=(i * 20))
        
        # Inject a hardware fault (0.0V) approx 10% of the time to test BMS alerts
        if random.random() < 0.10:
            pv_voltage = 0.0
            pv_current = 0.0
        else:
            pv_voltage = round(random.uniform(30.0, 45.0), 2)
            pv_current = round(random.uniform(5.0, 15.0), 2)
            
        # Build the payload to match your raw BigQuery intake pins exactly
        payloads.append({
            "device_id": f"array_{random.randint(1, 5):02d}", # Creates array_01 through array_05
            "timestamp": simulated_time.strftime("%Y-%m-%d %H:%M:%S"),
            "voltage": pv_voltage,
            "current": pv_current
        })
        
    return payloads

if __name__ == "__main__":
    print("Initializing Edge Sensor Array (Historical & Fault Injection Mode)...")
    data = generate_historical_telemetry(500)
    
    # Dump to the local buffer file that Mage reads from
    output_file = "raw_telemetry_buffer.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"SUCCESS: {len(data)} packets safely written to {output_file}.")