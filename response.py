import json
import os
 
class Response:

    def __init__(self):
        self.body = {}
        self.status_map = {
            '200': 'OK',
            '204': 'No Content',
            '400': 'Bad Request',
            '401': 'Unauthorized',
            '403': 'Forbidden',
            '404': 'Not Found',
            '409': 'Conflict',
            '500': 'Internal Server Error',
            '502': 'Bad Gateway'
        }
        self.status_code = '200'
        self.httpVersion = 1.1
        self.setResponseLine()
        self.renderPath = 'templates'

    def setResponseLine(self):
        status_message = self.status_map[self.status_code]
        self.responseLine = f'HTTP/{self.httpVersion} {self.status_code} {status_message}\r\n'

    def status(self, status_code):
        self.status_code = str(status_code)
        self.setResponseLine()
        return self
    
    def json(self, json_res):
        response_body = json.dumps(json_res)
        response_headers = {
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Content-Length": str(len(response_body))
        }
        response_headers_str = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())
        full_response = self.responseLine + response_headers_str + "\r\n\r\n" + response_body
        self.responseBody = full_response
        return full_response
    
    def send(self, message):
        message = str(message)
        response_headers = {
            "Content-Type": "text/plain",
            "Connection": "keep-alive",
            "Content-Length": str(len(message))
        }
        response_headers_str = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())
        full_response = self.responseLine + response_headers_str + "\r\n\r\n" + message
        self.responseBody = full_response
        return full_response

    
    def render(self, page, context):
        try:
            template_path = os.path.join(self.renderPath, page)
            with open(template_path, 'r') as file:
                template_content = file.read()
        except FileNotFoundError:
            return 'not found'
        try:
            rendered_content = template_content.format(**context)
        except KeyError as e:
            return 'some error'
        response_body = rendered_content
        response_headers = {
            "Content-Type": "text/html",
            "Connection": "keep-alive",
            "Content-Length": str(len(rendered_content))
        }
        response_headers_str = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())
        full_response = self.responseLine + response_headers_str + "\r\n\r\n" + response_body
        self.responseBody = full_response
        return full_response