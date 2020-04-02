from wsgi.server import WSGIServer
from wsgi.application import WSGIApplication, Request
from wsgi.application.response import JSONResponse

app = WSGIApplication()


@app.get("/")
def root(request: Request):
    return f"hello from / with query {request.query}"


@app.post("/create")
def create(request: Request):
    return f"hello from /create with request body {request.body}"


@app.post("/some_json")
def create(request: Request):
    return JSONResponse(body={"hello": "world"})


if __name__ == "__main__":
    server = WSGIServer("127.0.0.1", 5000, app)
    server.serve_forever()
