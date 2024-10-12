import json
import sys

from kombu import Connection, Consumer, Exchange, Queue

sys.path = ['', '..'] + sys.path[1:]

rabbitmq_url = "amqp://guest:guest@rabbitmq-service:5672/"

exchange = Exchange('device_exchange', type='direct', durable=True)
queue = Queue(name='device_locations', exchange=exchange, routing_key='device_locations', durable=True)


def process_message(body, message):
    from app.crud import save_location_data
    print(f"Consumer received message: {body}")
    try:
        save_location_data(json.loads(body))
        message.ack()
    except Exception as e:
        print(f"Error processing message on consumer: {e}")
        message.reject()


def start_consumer():
    print("Consumer is starting.")
    import time
    time.sleep(50)
    with Connection(rabbitmq_url) as conn:
        with Consumer(conn, queues=queue, callbacks=[process_message], accept=['json']):
            print("Consumer started. Waiting for messages...")
            while True:
                conn.drain_events()


if __name__ == '__main__':
    start_consumer()
