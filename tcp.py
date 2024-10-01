import socket
from threading import Thread
import select

class TCPServer:

    def __init__(self, host='127.0.0.1', port=8939):
        self.host = host
        self.port = port
        self.running = False
        self.threads = []
        self.server_socket = None

    def process_request(self, data):
        response = f"Data received: {data}, Data reversed: {data[::-1]}"
        response_body = f"<html><body><h1>{response}</h1></body></html>"
        response_headers = {
            "Content-Type": "text/html",
            "Connection": "keep-alive",
            "Content-Length": str(len(response_body))
        }
        
        response_line = "HTTP/1.1 200 OK\r\n"
        response_headers_str = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())
        full_response = response_line + response_headers_str + "\r\n\r\n" + response_body
        return full_response

    def request_handler(self, client_socket):
        while self.running:
            try:
                ready = select.select([client_socket], [], [], 1.0)
                print("ready-----------------")
                print(ready)
                if ready[0]:
                    data = client_socket.recv(2048)
                    if not data:
                        break
                    data = data.decode('utf-8')
                    full_response = self.process_request(data)
                    client_socket.sendall(full_response.encode('utf-8'))
            except Exception as e:
                print(f"Exception while processing request: {e}")
                break        
        client_socket.close()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"server is now running at {self.host}:{self.port}")
        self.running = True
        while self.running:
            try:
                client_socket, client_add = self.server_socket.accept()
                thread = Thread(target=self.request_handler, args=(client_socket,))
                thread.start()
                self.threads.append(thread)
            except:
                if self.running:
                    print("Error while accepting socket")

    def stop(self):
        print("Keyboard Interupt")

        self.running = False

        if self.server_socket:
            self.server_socket.close()

        print("socket closed")
        
        for thread in self.threads:
            thread.join()
        print("Server stopped")