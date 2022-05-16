from kafka import KafkaConsumer
from json import loads


consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    consumer_timeout_ms=10000
    )

consumer.subscribe(['test-topic'])
for msg in consumer:
    print(msg)
