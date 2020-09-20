from email.parser import BytesParser

import constants as C
from config import SERVER_NAME
from utils import *


def parse(raw: bytes):
    try:
        request_line, headers_alone = raw.split(b'\r\n', 1)
    except:
        return None
    headers = BytesParser().parsebytes(headers_alone)

    method, path, ver = request_line.decode(C.ENCODING).split()

    return Request(method, path, ver, headers)


class Request:
    def __init__(self, method, path, version, headers):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers

    def __str__(self):
        return f'Method: {self.method}\nPath: {self.path}\nVer: {self.version}\n\n'


class Response:
    def __init__(self, status: C.HTTP_CODE, body=''):
        self.status = status
        self.body = body

    def to_string(self, request: Request) -> str:
        type = get_content_type(request.path)
        with_body = self.body is not None and request.method == C.METHOD_GET

        tmp = request.version+' '+str(self.status.code)+' '+self.status.status+C.HTTP_EOF + \
            'Date: '+get_date()+C.HTTP_EOF + \
            'Server: '+SERVER_NAME+C.HTTP_EOF + \
            'Connection: Close'+C.HTTP_EOF

        if request.method == C.METHOD_HEAD or self.body is not None and len(self.body):
            tmp = tmp + \
                'Content-Length: ' + str(len(self.body)) + C.HTTP_EOF + \
                'Content-Type: ' + type + C.HTTP_EOF

        tmp = tmp + C.HTTP_EOF

        print(f'String body (with_body:{with_body})\n{tmp}')

        if with_body:
            tmp = tmp + self.body

        return tmp
