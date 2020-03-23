import socket


def serve_forever(host, port):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        client_socket, address = server_socket.accept()
        print(f"Socket established with {address}.")
        data = client_socket.recv(1024)
        print(f"Received {data}")
        client_socket.send(data)
        client_socket.close()


if __name__ == "__main__":
    serve_forever("127.0.0.1", 5000)
