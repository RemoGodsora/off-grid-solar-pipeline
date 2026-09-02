import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

# 🛠️ THE FIX: Point to the root folder ONLY. Spark will add \bin internally.
os.environ['HADOOP_HOME'] = 'C:\\hadoop'

# Hard-lock the Kafka driver to the stable release
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.6.0 pyspark-shell'

print("🔌 Booting Distributed Stream Processor (Synchronized to v3.5.1)...")

temp_path = os.path.abspath("./spark_temp")

# 1. Initialize the Master Node (With Temp Override)
spark = SparkSession.builder \
    .appName("Solar_Streaming_Controller") \
    .master("local[*]") \
    .config("spark.driver.extraJavaOptions", "-Duser.timezone=UTC") \
    .config("spark.executor.extraJavaOptions", "-Duser.timezone=UTC") \
    .config("spark.sql.session.timeZone", "UTC") \
    .config("spark.local.dir", temp_path) \
    .getOrCreate()

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
alert_stream = parsed_stream.filter(col("voltage") > 50.0)

# 6. Define the Database Routing Protocol
def write_to_postgres(batch_df, batch_id):
    # (batch_id is automatically injected by PySpark, exactly like a hardware interrupt)
    
    # 1. Print the micro-batch to your terminal (The LCD Monitor)
    print(f"\n--- Catching Overvoltage Anomaly in Batch {batch_id} ---")
    batch_df.show()
    
    # 2. Write the exact same data to PostgreSQL (The Battery Bank)
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5433/telemetry") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "thermal_anomalies") \
        .option("user", "admin") \
        .option("password", "admin") \
        .mode("append") \
        .save()

print("⚙️ Routing stream to PostgreSQL. Waiting for thermal anomalies...")

# 7. Execute the continuous micro-batch loop
# 🛠️ THE FIX: Hard-code a physical checkpoint path to bypass Windows file locking
checkpoint_path = os.path.abspath("./spark_checkpoints")

query = alert_stream.writeStream \
    .foreachBatch(write_to_postgres) \
    .option("checkpointLocation", f"file:///{checkpoint_path}") \
    .start()

query.awaitTermination()