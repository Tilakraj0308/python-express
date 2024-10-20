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
        pass

    def request_handler(self, client_socket):
        while self.running:
            try:
                ready = select.select([client_socket], [], [], 1.0)
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
        # Creating socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Freeing port instantly after program is stopped
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Binding the port and host to socket
        self.server_socket.bind((self.host, self.port))

        self.server_socket.listen()
        self.server_socket.settimeout(0.1)
        print(f"server is now running at http://{self.host}:{self.port}")
        self.running = True
        while self.running:
            try:
                client_socket, client_add = self.server_socket.accept()
                thread = Thread(target=self.request_handler, args=(client_socket,))
                thread.start()
                self.threads.append(thread)
            except socket.timeout:
                continue
            except:
                if self.running:
                    print("Error while accepting socket")

    def stop(self):

        self.running = False

        if self.server_socket:
            self.server_socket.close()
        
        for thread in self.threads:
            thread.join()