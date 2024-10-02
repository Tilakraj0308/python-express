from request import Request
from response import Response
from tcp import TCPServer
import signal
import sys


# types = ['multipart/form-data', 'application/x-www-form-urlencoded', 'text/plain']

class HTTPServer(TCPServer):

    def __init__(self, host='127.0.0.1', port=8939):
        super().__init__(host, port)
        self.routes = {}

    def handle_interrupt(self, signum, frame):
        print("There is an Interrupt")
        self.stop()
        sys.exit(0)


# Do not delete --> for later use
    def process_request(self, data):
        print(data)
        request = Request(data)
        req = request.getRequestObject()
        print(req)
        res = Response()
        route = request.getRoute()
        method = request.getRequestType()
        if not route in self.routes or not method in self.routes[route]:
            # 404 not found
            return
        self.routes[route][method](req, res)
        return res

    # def process_request(self, data):
    #     print(data)
    #     request = Request(data)
    #     req = request.getRequestObject()
    #     print(req)
    #     # route = request.getRoute()
    #     # method = request.getRequestType()
    #     # if not route in self.routes or not method in self.routes[route]:
    #     #     # 404 not found
    #     #     return
    #     # self.routes[route][method](req, res)
    #     return super().process_request(req["body"])

    def router(self, path, methods):
        if not path in self.routes:
            self.routes[path] = {}
        def inner(func):
            for method in methods:
                self.routes[path][method] = func
        return inner

    def get(self, path):
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