from tcp import TCPServer
import signal
import sys


types = ['multipart/form-data', 'application/x-www-form-urlencoded', 'text/plain']


class HTTPServer(TCPServer):

    def __init__(self, host='127.0.0.1', port=8939):
        super().__init__(host, port)
        self.routes = {}

    def handle_interrupt(self, signum, frame):
        print("There is an Interrupt")
        self.stop()
        sys.exit(0)

    def getRequestType(self, data):
        return data.split(' ')[0]
    
    def getRoute(self, data):
        return data.split(' ')[1]
     
    def getContentType(self, data_list):
        for d in data_list:
            if d.startswith('Content-Type'):
                return d.split(':')[1].split(';')[0]
        raise Exception('Content-Type missing')

    def process_request(self, data):
        print("DATA------------------------------------")
        for d in data.split('\r\n'):
            print(d.split('\n'))
        print('CONTENT-TYPE-------------------------')
        print(self.getContentType(data))
        print("Request type------------------------------------")
        print(self.getRequestType(data))
        return super().process_request(data)

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