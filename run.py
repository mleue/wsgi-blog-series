from wsgi.server import WSGIServer
from wsgi.application import WSGIApplication

app = WSGIApplication()


@app.get("/")
def root():
    print("Called root endpoint.")
    return "hello from /"


@app.post("/create")
def create():
    print(f"Called /create endpoint.")
    return "hello from /create"


if __name__ == "__main__":
    server = WSGIServer("127.0.0.1", 5000, app)
    server.serve_forever()
