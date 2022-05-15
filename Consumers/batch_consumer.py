from kafka import KafkaConsumer
from json import loads, dumps
import boto3
import os
from json.decoder import JSONDecodeError
from time import sleep
from helpers.settings import *


consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    consumer_timeout_ms=10000,
    value_deserializer=lambda message: loads(message.decode('utf-8'))
)

s3 = boto3.resource(
    service_name='s3',
    region_name=region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

bucket = s3.Bucket('pintrst')
folder_name = "pinpost"
print(bucket)

# TODO send data to S3 using boto3
consumer.subscribe(['pinterest'])
for msg in consumer:
    data = msg.value
    save_file_name = data.get("unique_id") + ".json"
    s3object = bucket.put_object(Key=save_file_name, Body=dumps(data))
