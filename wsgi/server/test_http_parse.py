import pytest
from .http_parse import HttpRequestParser


class TestParserProtocol:
    # parser callbacks
    def on_url(self, url: bytes):
        print(f"Received url: {url}")
        self.url = url
        self.headers = []

    def on_header(self, name: bytes, value: bytes):
        print(f"Received header: ({name}, {value})")
        self.headers.append((name, value))

    def on_body(self, body: bytes):
        self.body = body
        print(f"Received body: {body}")

    def on_message_complete(self):
        pass


def test_parser_get():
    protocol = TestParserProtocol()
    parser = HttpRequestParser(protocol)
    data = b"GET /abc HTTP/1.1\r\nHost: localhost:5000\r\nUser-Agent: curl/7.69.1\r\nAccept: */*\r\n\r\n"
    parser.feed_data(data)
    assert protocol.url == b"/abc"
    assert protocol.headers == [
        (b"Host", b"localhost:5000"),
        (b"User-Agent", b"curl/7.69.1"),
        (b"Accept", b"*/*"),
    ]
    assert not hasattr(protocol, "body")


def test_parser_get_chunked():
    protocol = TestParserProtocol()
    parser = HttpRequestParser(protocol)
    chunks = [
        b"GET /index.html ",
        b"HTTP/1.1\r\nHost",
        b": localhost:5000",
        b"\r\nUser-Agent: ",
        b"curl/7.69.1\r\nA",
        b"ccept: */*\r\n\r",
        b"\n",
    ]
    for data in chunks:
        parser.feed_data(data)
    assert protocol.url == b"/index.html"
    assert protocol.headers == [
        (b"Host", b"localhost:5000"),
        (b"User-Agent", b"curl/7.69.1"),
        (b"Accept", b"*/*"),
    ]
    assert not hasattr(protocol, "body")


def test_parser_post_with_body():
    protocol = TestParserProtocol()
    parser = HttpRequestParser(protocol)
    data = b"POST / HTTP/1.1\r\nHost: localhost:5000\r\nUser-Agent: curl/7.69.1\r\nAccept: */*\r\nContent-Length: 7\r\nContent-Type: application/json\r\n\r\nabc=def"
    parser.feed_data(data)
    assert protocol.url == b"/"
    assert protocol.headers == [
        (b"Host", b"localhost:5000"),
        (b"User-Agent", b"curl/7.69.1"),
        (b"Accept", b"*/*"),
        (b"Content-Length", b"7"),
        (b"Content-Type", b"application/json"),
    ]
    assert protocol.body == b"abc=def"
