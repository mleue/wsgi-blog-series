from typing import Tuple
import socket
import threading
from httptools import HttpRequestParser
from http_request import HttpRequestParserProtocol
from http_response import make_response


def handle_socket(client_socket, address: Tuple[str, int]):
    response_sent = False

    def send_response():
        body = b"<html><body>Hello World</body></html>"
        response = make_response(status_code=200, headers=[], body=body)
        client_socket.send(response)
        print("Response sent.")
        nonlocal response_sent
        response_sent = True

    protocol = HttpRequestParserProtocol(send_response)
    parser = HttpRequestParser(protocol)

    while True:
        if response_sent:
            break
        data = client_socket.recv(1024)
        print(f"Received {data}")
        parser.feed_data(data)
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
