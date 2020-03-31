from typing import Tuple
import socket
import threading
from http_parse import HttpRequestParser
from http_response import make_response


class Session:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        self.response_sent = False
        self.parser = HttpRequestParser(self)

    def run(self):
        while True:
            if self.response_sent:
                break
            data = self.client_socket.recv(1024)
            print(f"Received {data}")
            self.parser.feed_data(data)
        self.client_socket.close()
        print(f"Socket with {self.address} closed.")

    def send_response(self):
        body = b"<html><body>Hello World</body></html>"
        response = make_response(status_code=200, headers=[], body=body)
        self.client_socket.send(response)
        print("Response sent.")
        self.response_sent = True

    # parser callbacks
    def on_url(self, url: bytes):
        print(f"Received url: {url}")
        self.http_method = self.parser.http_method.decode("utf-8")
        self.url = url.decode("utf-8")
        self.headers = []

    def on_header(self, name: bytes, value: bytes):
        print(f"Received header: ({name}, {value})")
        self.headers.append((name, value))

    def on_body(self, body: bytes):
        print(f"Received body: {body}")

    def on_message_complete(self):
        print("Received request completely.")
        self.send_response()


def serve_forever(host: str, port: int):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        client_socket, address = server_socket.accept()
        print(f"Socket established with {address}.")
        session = Session(client_socket, address)
        t = threading.Thread(target=session.run)
        t.start()


if __name__ == "__main__":
    serve_forever("127.0.0.1", 5000)
