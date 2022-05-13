# Run following commands in separate terminals

# Start zookeeper for kafka connections
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
# Start kafka server
kafka-server-start /usr/local/etc/kafka/server.properties
# Create kafka topic named test-topic
kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
# Create kafka producer - You can write messages into this (ONLY FOR TESTING)
kafka-console-producer --broker-list localhost:9092 --topic test-topic
# Create kafka consumer - You can view messages in this terminal (ONLY FOR TESTING)
kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning