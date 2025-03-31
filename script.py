from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

# Kafka configuration
KAFKA_BROKER = '[broker_address]'
CONSUMER_TOPIC = 'events_topic'
PRODUCER_TOPIC = 'processed_events_topic'

# Initialize Kafka producer and consumer
producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
consumer = KafkaConsumer(
    CONSUMER_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    group_id='worker-service-recovery',
    auto_offset_reset='earliest',  # Start from the earliest message, could replace with latest offset before errors
)

# Function to process event
def process_event(event_data):
    # Implement the logic to process the event
    return f"Processed: {event_data}"

# Function to consume events from Kafka, simulate event replay
def replay_events():
    try:
        for msg in consumer:
            event_data = msg.value.decode('utf-8')
            result = process_event(event_data)
            producer.send(PRODUCER_TOPIC, value=result.encode('utf-8'))
            producer.flush()
    except KafkaError as e:
        print(f"Kafka error occurred: {e}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    replay_events()
