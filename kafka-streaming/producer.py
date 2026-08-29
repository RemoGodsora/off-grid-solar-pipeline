import json
import time
import random
from confluent_kafka import Producer

print("Booting Enterprise Network Antenna (Confluent)...")

# Establish the TCP connection to your local Kafka Router
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

topic = 'solar_telemetry'
print("Connection established. Initiating high-frequency telemetry transmission...")

def receipt_confirmation(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err}")

try:
    while True:
        # Generate a synthetic payload
        payload = {
            'sensor_id': f'array_{random.randint(1, 50):02d}',
            'voltage': round(random.uniform(45.0, 52.0), 2),
            'current_amps': round(random.uniform(8.0, 12.0), 2),
            'temperature': round(random.uniform(20.0, 85.0), 2),
            'timestamp': int(time.time())
        }

        # Fire the packet into the Kafka network
        json_payload = json.dumps(payload).encode('utf-8')
        producer.produce(topic, value=json_payload, callback=receipt_confirmation)
        
        # Clear the queue and trigger the callback
        producer.poll(0)
        
        print(f"Packet transmitted: {payload['sensor_id']} -> {payload['voltage']}V")

        # Wait 500 milliseconds (High Velocity)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nTransmission halted by operator. Flushing network buffers...")
    producer.flush()