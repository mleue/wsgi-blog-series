from flask import Flask, request
from wsgi.server import WSGIServer


app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    print("Called root endpoint.")
    return "hello from /"


@app.route("/create", methods=["POST"])
def create():
    print(f"Called create endpoint with data {request.data}.")
    return "hello from /create"


if __name__ == "__main__":
    server = WSGIServer("127.0.0.1", 5000, app)
    server.serve_forever()
