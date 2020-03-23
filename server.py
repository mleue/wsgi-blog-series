from typing import Tuple
import socket
import threading


def handle_socket(client_socket, address: Tuple[str, int]):
    while True:
        data = client_socket.recv(1024)
        print(f"Received {data}")
        if data == b"":
            break
        client_socket.send(data)
    client_socket.close()
    print(f"Socket with {address} closed.")


def serve_forever(host: str, port: int):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        client_socket, address = server_socket.accept()
        print(f"Socket established with {address}.")
        t = threading.Thread(
            target=handle_socket, args=(client_socket, address)
        )
        t.start()


if __name__ == "__main__":
    serve_forever("127.0.0.1", 5000)
