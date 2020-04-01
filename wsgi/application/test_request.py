from io import BytesIO
from .request import Request

def test_from_environ():
    environ = {
        "QUERY_STRING": "abc=1&def=2",
        "wsgi.input": BytesIO(b"abc"),
        "HTTP_Content-Type": "application/json",
        "HTTP_Content-Length": "20",
    }
    request = Request.from_environ(environ)
    assert request.query["abc"] == "1"
    assert request.query["def"] == "2"
    assert request.body == b"abc"
    assert request.headers["Content-Type"] == "application/json"
    assert len(request.headers) == 2
