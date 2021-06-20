"""Основной скрипт для запуска ETL сервиса."""
import gc
import json
import sys
from time import sleep

from clickhouse import init_clickhouse_database, save_to_clickhouse
from config import settings
from confluent_kafka import Consumer, KafkaError, KafkaException
from models import Event

# kafka client init
conf = {
    "bootstrap.servers": settings.kafka_hosts_as_string,
    "group.id": settings.kafka_consumer_group,
    "auto.offset.reset": "smallest",
}

consumer = Consumer(conf)
running = True
SLEEP_TIME = 5


def consume_loop(consumer, topics):
    """Цикл, который потребляет сообщения из Kafka."""
    try:
        consumer.subscribe(topics)

        while running:
            messages = consumer.consume(num_messages=100, timeout=1.0)
            if messages is None:
                continue

            events: list[Event] = []
            for message in messages:
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write(
                            "%% %s [%d] reached end at offset %d\n"
                            % (message.topic(), message.partition(), message.offset()),
                        )
                    elif message.error():
                        raise KafkaException(message.error())

                events.append(Event(**json.loads(message.value())))

            if events:
                save_to_clickhouse(events)

            gc.collect()

            sleep(SLEEP_TIME)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    """Завершение работы ETL."""
    global running
    running = False


if __name__ == "__main__":
    init_clickhouse_database()
    consume_loop(consumer, settings.kafka_topics)
