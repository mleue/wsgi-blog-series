import json
from typing import List, Tuple, Optional, Any


class BaseResponse:
    def __init__(
        self,
        status: str = "200 OK",
        headers: Optional[List[Tuple[str, str]]] = None,
        body: Optional[Any] = None,
    ):
        self.status = status
        self.headers = headers if headers is not None else []
        self.body = self.body_conversion(body) if body is not None else b""
        self.add_content_type_and_content_length()

    def add_content_type_and_content_length(self):
        header_names = {name for name, value in self.headers}
        if not "Content-Type" in header_names:
            self.headers.append(("Content-Type", self.content_type))
        if self.body and not "Content-Length" in header_names:
            self.headers.append(("Content-Length", str(len(self.body))))


class PlainTextResponse(BaseResponse):
    content_type = "plain/text"

    @classmethod
    def body_conversion(cls, body):
        return body.encode("utf-8")


class HTMLResponse(BaseResponse):
    content_type = "plain/html"

    @classmethod
    def body_conversion(cls, body):
        return body.encode("utf-8")


class JSONResponse(BaseResponse):
    content_type = "application/json"

    @classmethod
    def body_conversion(cls, body):
        return json.dumps(body).encode("utf-8")
