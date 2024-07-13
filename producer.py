from kafka import KafkaConsumer

class KafkaConsumerApp:
    def __init__(self, topic, group_id, servers):
        self.consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

    def listen_messages(self):
        print(f"Listening to messages on topic: {self.consumer.topics()}")
        for message in self.consumer:
            print(f"Received message: {message.value.decode('utf-8')}")

if __name__ == "__main__":
    # Remplacez 'your_topic', 'your_group_id', et 'localhost:9092' par vos valeurs spécifiques
    topic = 'your_topic'
    group_id = 'your_group_id'
    servers = ['localhost:9092']

    kafka_app = KafkaConsumerApp(topic, group_id, servers)
    kafka_app.listen_messages()
