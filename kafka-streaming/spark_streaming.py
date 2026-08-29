import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

# 🛠️ THE FIX: Point to the root folder ONLY. Spark will add \bin internally.
os.environ['HADOOP_HOME'] = 'C:\\hadoop'

# Hard-lock the Kafka driver to the stable release
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 pyspark-shell'

print("🔌 Booting Distributed Stream Processor (Synchronized to v3.5.1)...")

# 1. Initialize the Master Node
spark = SparkSession.builder \
    .appName("Solar_Streaming_Controller") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Define the exact schematic of our incoming JSON payload
schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("voltage", DoubleType(), True),
    StructField("current_amps", DoubleType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("timestamp", LongType(), True)
])

print("📡 Tapping into Kafka Router (Port 9092)...")

# 3. Read the live binary stream from Kafka
raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "solar_telemetry") \
    .option("startingOffsets", "latest") \
    .load()

# 4. Decode the raw binary network payload into a structured table
parsed_stream = raw_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# 5. Distributed Transformation (Only catch Overheating spikes)
alert_stream = parsed_stream.filter(col("temperature") > 80.0)

print("⚙️ Routing stream to console output. Waiting for thermal anomalies...")

# 6. Execute the continuous micro-batch loop
query = alert_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Keep the circuit open indefinitely
query.awaitTermination()