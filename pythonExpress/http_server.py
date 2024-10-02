from pythonExpress.request import Request
from pythonExpress.response import Response
from pythonExpress.tcp import TCPServer
import signal
import sys
import os


class HTTPServer(TCPServer):

    def __init__(self, host='127.0.0.1', port=8939):
        super().__init__(host, port)
        self.routes = {}
        self.last_modified_time = self.get_last_modified_time()

    def get_last_modified_time(self):
        return max(os.path.getmtime(f) for f in os.listdir('.') if f.endswith('.py'))

    def handle_interrupt(self, signum, frame):
        if self.debug_mode and signum == signal.SIGALRM:
            current_modified_time = self.get_last_modified_time()
            if current_modified_time > self.last_modified_time:
                print("Code changes detected. Restarting server...")
                print()
                self.stop()
                os.execv(sys.executable, ['python'] + sys.argv)
            signal.alarm(1)
        else:
            print()
            print("Keyboard Interrupt")
            print("Stopping the server....")
            self.stop()
            print("Server stopped")
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
        return self.router(path.upper(), methods=['GET'])
        
    def post(self, path):
        return self.router(path.upper(), methods=['POST'])
    
    def put(self, path):
        return self.router(path.upper(), methods=['PUT'])
    
    def delete(self, path):
        return self.router(path.upper(), methods=['DELETE'])


    def startServer(self, debug=False):
        self.debug_mode = debug
        signal.signal(signalnum=signal.SIGINT, handler=self.handle_interrupt)
        if self.debug_mode:
            print("Server running in debug mode. Auto-restart is enabled.")
            signal.signal(signal.SIGALRM, self.handle_interrupt)
            signal.alarm(1)
        try:
            self.start()
        except KeyboardInterrupt as e:
            print("Ctrl + c pressed")
            pass
        finally:
            if self.running:
                self.stop()