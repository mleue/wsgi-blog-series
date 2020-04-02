from typing import Callable
from dataclasses import dataclass
from .request import Request
from .response import PlainTextResponse, BaseResponse


class WSGIApplication:
    def __init__(self):
        self.path_operations = dict()

    def _register_path_operation(
        self, path: str, http_method: str, func: Callable
    ):
        po = PathOperation(path, http_method)
        self.path_operations[po] = func

    def _create_register_decorator(self, path: str, http_method: str):
        def decorator(func: Callable):
            self._register_path_operation(path, http_method, func)
            return func

        return decorator

    def get(self, path: str):
        return self._create_register_decorator(path, "GET")

    def post(self, path: str):
        return self._create_register_decorator(path, "POST")

    def __call__(self, environ, start_response):
        po = PathOperation(environ["PATH_INFO"], environ["REQUEST_METHOD"])
        func = self.path_operations.get(po)
        if func is None:
            response = PlainTextResponse(status="404 NOT FOUND")
        else:
            request = Request.from_environ(environ)
            ret = func(request=request)
            if isinstance(ret, BaseResponse):
                response = ret
            else:
                response = PlainTextResponse(body=ret)
        start_response(response.status, response.headers)
        return [response.body]


@dataclass(frozen=True, eq=True)
class PathOperation:
    path: str
    http_method: str
