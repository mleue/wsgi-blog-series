from .splitbuffer import SplitBuffer

def test_splitbuffer():
    buffer = SplitBuffer()
    buffer.feed_data(b"abc,")
    buffer.feed_data(b"defg")
    buffer.feed_data(b",hi,")
    assert buffer.pop(separator=b",") == b"abc"
    assert buffer.pop(separator=b",") == b"defg"
    buffer.feed_data(b",jkl")
    assert buffer.pop(separator=b",") == b"hi"
    assert buffer.pop(separator=b",") == b""
    assert buffer.pop(separator=b",") is None
    assert buffer.flush() == b"jkl"
