import json
from confluent_kafka import Consumer, KafkaError, KafkaException

print("🔌 Booting Edge Receiver...")

# 1. Configure the Receiver to connect to the Kafka Router (Port 9092)
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'solar_monitoring_dashboard',
    'auto.offset.reset': 'latest' # Tells the receiver to only catch NEW packets
}

consumer = Consumer(conf)

# 2. Tune the antenna to the specific frequency (Topic)
topic = 'solar_telemetry'
consumer.subscribe([topic])

print(f"📡 Receiver Online. Listening to '{topic}' stream...\n")

try:
    while True:
        # 3. Pull data off the Kafka RAM buffer
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
            
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())

        # 4. Decode binary to JSON
        payload = json.loads(msg.value().decode('utf-8'))
        
        sensor = payload.get('sensor_id')
        voltage = payload.get('voltage')
        amperage = payload.get('amperage')
        
        # 5. Basic Edge Alert Logic
        if voltage > 240.0:
            print(f"⚠️ OVERVOLTAGE ALERT: {sensor} is spiking at {voltage}V!")
        else:
            print(f"✅ Packet Caught: {sensor} | {voltage}V | {amperage}A")

except KeyboardInterrupt:
    print("\n🛑 Receiver powered down by operator.")
finally:
    consumer.close()