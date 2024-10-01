import socket
from threading import Thread


def request_handler(connection):
    data = connection.recv(1024)
    decoded_data = data.decode().strip()
    # print(decoded_data)
    # print("decoded decoded-------------------")
    # print("This is the response")
    # print(decoded_data.split("\r\n"))
    request_data = decoded_data.split("\r\n")[-1]
    response = f"Data received: {request_data}, Data reversed: {request_data[::-1]}"
    response_body = f"<html><head><title>Hello from Python HTTP Server</title></head><body><h1>response</h1></body></html>"
    response_headers = {
            "Content-Type": "text/html",
            "Connection": "close"
        }
    response_line = f"HTTP/1.1 200 OK\r\n"
    response_headers_str = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())

    response = response_line + response_headers_str + "\r\n" + response_body
    # connection.send(response_body.encode('utf-8'))
    message = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Hello, world!</h1></body></html>"
    connection.send(message.encode('utf-8'))
    connection.close()


def startServer(port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'

    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Started server on port {port}")
    while True:
        client_socket, address = server_socket.accept()
        client_handler = Thread(target=request_handler, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    startServer(9939)
