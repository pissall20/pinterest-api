import pyspark
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import *

packages = ['org.apache.spark:spark-sql-kafka-0-10_2.12:{}'.format(pyspark.__version__)]
packages = ",".join(packages) if isinstance(packages, list) else packages
spark = (
    SparkSession.builder.master("local[*]")
        .config("spark.io.compression.codec", "snappy")
        .config("spark.ui.enabled", "false")
        .config("spark.jars.packages", packages)
        .getOrCreate()
)

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("failOnDataLoss", "false") \
    .option("subscribe", "pinterest") \
    .option("includeHeaders", "true") \
    .option("startingOffsets", "latest") \
    .option("spark.streaming.kafka.maxRatePerPartition", "50") \
    .load()

kafka_df.printSchema()

string_df = kafka_df.selectExpr("CAST(value AS STRING)")

schema = StructType().add("category", "string").add("index", "integer").add("unique_id", "string") \
    .add("title", "string").add("description", "string").add("follower_count", "string").add("tag_list", "string") \
    .add("is_image_or_video", "string").add("image_src", "string").add("downloaded", "integer") \
    .add("save_location", "string")

schema_df = string_df.select(F.from_json(F.col("value"), schema).alias("data")).select("data.*")

# Clean save_location column to only contain the path
df1 = schema_df.withColumn("save_location", F.expr("substring(save_location, 16, length(save_location))"))

# Clean follower count and convert to integer (k=1000, M=100000)
df2 = df1.withColumn("follower_count", F.regexp_replace(F.col("follower_count"), "k", "000"))\
    .withColumn("follower_count", F.regexp_replace(F.col("follower_count"), "M", "000000"))\
    .withColumn("follower_count", F.col("follower_count").cast("integer"))

# Convert tag_list which is as string to an actual list of tags
df3 = df2.withColumn("tag_list_clean", F.split(F.col("tag_list"), ","))

# Count the number of tags as a feature
df4 = df3.withColumn("number_of_tags", F.size(F.col("tag_list_clean")))

df4.printSchema()

df4.writeStream.format("console").outputMode("append").start().awaitTermination()
