import json
import socket

import pika


def generate_location_data(request_data):
    data = json.loads(request_data)
    return {"device_id": data.get('device_id'),
            "latitude": data.get('latitude'),
            "longitude": data.get('longitude')}


def start_tcp_server(host='0.0.0.0', port=12345):
    print("TCP Socket is starting")
    import time
    time.sleep(50)
    connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@rabbitmq-service:5672'))
    channel = connection.channel()
    channel.queue_declare(queue='device_locations', durable=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"TCP Socket started at {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            print(f"TCP Socket connected by {addr}")
            data = conn.recv(1024).decode('utf-8')
            if data:
                location_data = generate_location_data(data)
                channel.basic_publish(
                    exchange='',
                    routing_key='device_locations',
                    body=json.dumps(location_data)
                )
                print(f"TCP Socket sent data: {location_data} to the queue")
                response = json.dumps({"status": "success", "message": "Location data received"})
                conn.sendall(response.encode('utf-8'))


if __name__ == "__main__":
    start_tcp_server()
