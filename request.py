import json

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Request:
    def __init__(self, data):
        self.data = data

    def getContentType(self):
        for d in self.data.split('\r\n'):
            if d.startswith('Content-Type'):
                return d.split(':')[1].split(';')[0].strip()
        return 'text/plain'
    
    def getRequestType(self):
        return self.data.split(' ')[0].upper()
    
    def getRoute(self):
        return self.data.split(' ')[1].split('?')[0].upper()

    def getRequestLine(self):
        request_line = self.data.split('\r\n')[0]
        request_elements = request_line.split(' ')
        httpMethod = request_elements[0]
        httpVersion = request_elements[2].split('/')[1]
        requestTarget = request_elements[1].split('?')
        requestLine = {'http-method': httpMethod, 'request-target': requestTarget[0], 'http-version': httpVersion, 'query': {}}
        if len(requestTarget) > 1:
            query_params = {}
            params = requestTarget[1].split('&')
            for query in params:
                key, value = query.split('=')
                query_params[key] = value
            requestLine['query'] = dotdict(query_params)
        return requestLine

    def getRequestHeader(self):
        data = '\r\n'.join(self.data.split('\r\n')[1:])
        request_header = {}
        # For url-encoded data
        if self.getContentType() == 'multipart/form-data':
            boundary = data.split('boundary=')[1].split('\r\n')[0]
            data = '\r\n'.join([data.split(f'boundary={boundary}')[0].split(';')[0], data.split(f'boundary={boundary}')[1].split('\r\n')[1]])

        for d in data.split('\r\n'):
            if not d:
                break
            key, value = d.split(': ')
            request_header[key.lower()] = value.strip()
        return request_header
    
    def getRequestBody(self):
        request_body = {}
        if self.data.split('\r\n\r\n')[1] == '':
            return request_body
        contentType = self.getContentType()
        # For form-data
        if contentType == 'multipart/form-data':
            boundary = self.data.split('boundary=')[1].split('\r\n')[0]
            params = '\r\n'.join('\r\n'.join('\r\n'.join(self.data.split(boundary+'\r\n')[2:]).split('--'+boundary+'--')).split('\r\n\r\n'))
            for param in params.split('--'):
                keyValue = param.split(';')[1].split('\r\n')
                key = keyValue[0].split('=')[1]
                value = keyValue[1]
                request_body[key[1:-1]] = value
            return request_body
            
        # For raw-text or raw-json data
        elif contentType in ['text/plain', 'application/json']:
            data = self.data.split('\r\n\r\n')[1]
            request_body = json.loads(str(data))
            return request_body
        
        # For url-encoded data
        elif contentType == 'application/x-www-form-urlencoded':
            data = self.data.split('\r\n\r\n')[1]
            for pair in data.split('&'):
                key, value = pair.split('=')
                request_body[key] = value
            return request_body
        
        # Any other format not supported
        else:
            raise Exception("Input data format not supported")


    def getRequestObject(self):
        request = {}
        request['requestLine'] = dotdict(self.getRequestLine())
        request['header'] = dotdict(self.getRequestHeader())
        request['body'] = dotdict(self.getRequestBody())
        return dotdict(request)