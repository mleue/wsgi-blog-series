from typing import Tuple, List
import socket
import threading
from io import BytesIO
from http_parse import HttpRequestParser
from wsgi import WSGIRequest, WSGIResponse
from app import app


class Session:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        self.parser = HttpRequestParser(self)
        self.request = WSGIRequest()
        self.response = WSGIResponse()

    def run(self):
        while True:
            if self.response.is_sent:
                break
            data = self.client_socket.recv(1024)
            print(f"Received {data}")
            self.parser.feed_data(data)
        self.client_socket.close()
        print(f"Socket with {self.address} closed.")

    # parser callbacks
    def on_url(self, url: bytes):
        print(f"Received url: {url}")
        self.request.http_method = self.parser.http_method.decode("utf-8")
        self.request.path = url.decode("utf-8")

    def on_header(self, name: bytes, value: bytes):
        print(f"Received header: ({name}, {value})")
        self.request.headers.append(
            (name.decode("utf-8"), value.decode("utf-8"))
        )

    def on_body(self, body: bytes):
        print(f"Received body: {body}")
        self.request.body.write(body)
        self.request.body.seek(0)

    def on_message_complete(self):
        print("Received request completely.")
        environ = self.request.to_environ()
        body_chunks = app(environ, self.response.start_response)
        print("App callable has returned.")
        self.response.body = b"".join(body_chunks)
        self.client_socket.send(self.response.to_http())


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
