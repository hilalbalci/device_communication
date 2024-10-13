import json
import sys
import time

from kombu import Connection, Consumer, Exchange, Queue

sys.path = ['', '..'] + sys.path[1:]

rabbitmq_url = "amqp://guest:guest@rabbitmq-service:5672/"

exchange = Exchange('device_exchange', type='direct', durable=True)
queue = Queue(name='device_locations', exchange=exchange, routing_key='device_locations', durable=True)


def process_message(body, message):
    from app.crud import save_location_data
    from app.main import logger
    logger.info(f"Consumer received a message: {body}")
    try:
        save_location_data(json.loads(body))
        message.ack()
    except Exception as e:
        logger.error(f"Error processing message on consumer: {e}")
        message.reject()


def start_consumer():
    from app.main import logger
    logger.info("Consumer is starting")
    time.sleep(50)
    with Connection(rabbitmq_url) as conn:
        with Consumer(conn, queues=queue, callbacks=[process_message], accept=['json']):
            logger.info("Consumer started. Waiting for messages...")
            while True:
                conn.drain_events()


if __name__ == '__main__':
    start_consumer()
