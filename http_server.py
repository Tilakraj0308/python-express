from request import Request
from response import Response
from tcp import TCPServer
import signal
import sys


class HTTPServer(TCPServer):

    def __init__(self, host='127.0.0.1', port=8939):
        super().__init__(host, port)
        self.routes = {}

    def handle_interrupt(self, signum, frame):
        print("There is an Interrupt")
        self.stop()
        sys.exit(0)

    def process_request(self, data):
        try:
            request = Request(data)
            req = request.getRequestObject()
            res = Response()
            route = request.getRoute()
            method = request.getRequestType()
            if not route in self.routes or not method in self.routes[route]:
                raise Exception(f'{method} for route {route} not found')
            return self.routes[route][method](req, res)
        except Exception as e:
            return res.status(404).send(e)

    def router(self, path, methods):
        if not path in self.routes:
            self.routes[path] = {}
        def inner(func):
            for method in methods:
                self.routes[path][method] = func
        return inner

    def get(self, path):
        print("path=", path)
        return self.router(path.upper(), methods=['GET'])
        
    def post(self, path):
        return self.router(path.upper(), methods=['POST'])
    
    def put(self, path):
        return self.router(path.upper(), methods=['PUT'])
    
    def delete(self, path):
        return self.router(path.upper(), methods=['DELETE'])


    def startServer(self):
        signal.signal(signalnum=signal.SIGINT, handler=self.handle_interrupt)
        try:
            self.start()
        except KeyboardInterrupt as e:
            print("Ctrl + c pressed")
            pass
        finally:
            if self.running:
                print("finally block")
                self.stop()