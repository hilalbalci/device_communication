import socket


def test_tcp_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('host.docker.internal', 12345))
    client.sendall(b'{"device_id": 1}')
    response = client.recv(1024)
    assert response == b''
