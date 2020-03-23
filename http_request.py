from typing import Callable


class HttpRequestParserProtocol:
    def __init__(self, send_response: Callable):
        self.send_response = send_response

    # parser callbacks
    def on_url(self, url):
        print(f"Received url: {url}")
        self.headers = []

    def on_header(self, name: bytes, value: bytes):
        print(f"Received header: ({name}, {value})")
        self.headers.append((name, value))

    def on_body(self, body: bytes):
        print(f"Received body: {body}")

    def on_message_complete(self):
        print("Received request completely.")
        self.send_response()
