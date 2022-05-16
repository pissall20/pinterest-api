import os
import sys
from kafka import KafkaConsumer
from json import loads, dumps
import boto3

# To fix path issues for import
sys.path.insert(0, os.getcwd())
from settings import *

# Create a Kafka Consumer
consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    consumer_timeout_ms=10000,
    value_deserializer=lambda message: loads(message.decode('utf-8'))
)

# Create s3 object to interact with s3 bucket
s3 = boto3.resource(
    service_name='s3',
    region_name=region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# Define the bucket
bucket = s3.Bucket(bucket_name)
print(bucket)

# Subscribe to the kafka topic
consumer.subscribe([kafka_topic])

# Loop over messages in the kafka topic and put files to S3 bucket
for msg in consumer:
    data = msg.value
    save_file_name = data.get("unique_id") + ".json"
    save_path = os.path.join(folder_name, save_file_name)
    print(f"Saving file to {save_path}")
    s3object = bucket.put_object(Key=save_path, Body=dumps(data))
