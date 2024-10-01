from http_server import HTTPServer

server = HTTPServer(port=5000)
server.startServer()

@server.get('/')
def home(req, res):
    print('here is req')