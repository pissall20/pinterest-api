import pyspark
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from cassandra.cluster import Cluster


spark = (
    SparkSession.builder.master("local[*]")
        .config("spark.io.compression.codec", "snappy")
        .config("spark.ui.enabled", "false")
        .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0")
        .getOrCreate()
)

# Replace json_files with s3 URI to read from S3
df = spark.read.json("json_files/*.json")

# Clean save_location column to only contain the path
df = df.withColumn("save_location", F.expr("substring(save_location, 16, length(save_location))"))

# Clean follower count and convert to integer (k=1000, M=100000)
df = df.withColumn("follower_count", F.regexp_replace(F.col("follower_count"), "k", "000")) \
    .withColumn("follower_count", F.regexp_replace(F.col("follower_count"), "M", "000000")) \
    .withColumn("follower_count", F.col("follower_count").cast("integer"))

# Convert tag_list which is as string to an actual list of tags
df = df.withColumn("tag_list_count", F.size(F.split(F.col("tag_list"), ",")))

# Cassandra does not agree with column name as index
df = df.withColumnRenamed("index", "index_var")

df.show()

# Cassandra part

cluster = Cluster()
session = cluster.connect()

key_space_name = "pinterest"
config_dict = {"class": "SimpleStrategy", "replication_factor": 1}
create_keyspace_query = f"CREATE KEYSPACE IF NOT EXISTS {key_space_name} WITH REPLICATION = {str(config_dict)};"

session.execute(create_keyspace_query)
print("Keyspace successfully created")

session.set_keyspace(key_space_name)

# create table query
table_name = "events"
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name}(unique_id text PRIMARY KEY,category text,title text," \
                     f"description text,index_var int,follower_count int,tag_list text,is_image_or_video text," \
                     f"image_src text,downloaded int,save_location text,tag_list_count int);"
session.execute(create_table_query)
print("Table successfully created")

# Write data to cassandra
df.write.format("org.apache.spark.sql.cassandra").mode('append').options(table=table_name,
                                                                         keyspace=key_space_name).save()


# Showing that the rows have been inserted
rows = session.execute(f"select * from {table_name}")

for row in rows:
    print(row)
