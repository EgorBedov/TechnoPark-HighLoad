import asyncio

from MyConfig import SERVER_NAME
from utils import *

import constants as C


class Parser:
    @staticmethod
    async def parse_HTTP_request(reader: asyncio.StreamReader):
        method, path, ver = await Parser.parse_request_line(reader)
        if method is None or method == '':
            print('No method')
            return None
        print('Parsed request line: ', method, path, ver)

        headers = await Parser.parse_headers(reader)
        print('Parsed headers: ', headers)

        # body = await Parser.parse_body(reader)
        # print('Parsed body: ', body)

        return Request(method, path, ver, headers)

    @staticmethod
    async def parse_request_line(reader: asyncio.StreamReader):
        raw = await reader.readline()

        print('Raw: ', raw)

        req_line = raw.decode(C.ENCODING)
        req_line = req_line.rstrip('\r\n')
        words = req_line.split()
        # if len(words) != 3:
        #     raise Exception('Malformed request line')

        print('Words: ', words)

        return words    #['GET', 'path', 'http/1.1']

    @staticmethod
    async def parse_headers(reader: asyncio.StreamReader) -> dict:
        headers = []
        while True:
            raw = await reader.readline()
            line = raw.decode(C.ENCODING)
            # if len(line) > C.MAX_LINE:
            #     raise Exception('Header line is too long')


            if raw in (b'\r\n', b'\n', b''):
                # завершаем чтение заголовков
                break

            headers.append(line)
            # if len(headers) > C.MAX_HEADERS:
            #     raise Exception('Too many headers')

        # convert array to dict
        hdict = {}
        for h in headers:
            # h = h.decode('iso-8859-1') # here what
            k, v = h.split(':', 1)
            hdict[k] = v

        return hdict

    # @staticmethod
    # async def parse_body(reader: asyncio.StreamReader):
    #     body = ''
    #
    #     print('Start parsing body')
    #     while not reader.at_eof():
    #         chunk = await reader.read(8)
    #         print(chunk)
    #         if chunk == b'\r\n' or chunk == b'\n' or chunk == b'':
    #             break
    #         print('New chunk: ', chunk.decode(C.ENCODING))
    #         body += chunk.decode(C.ENCODING)
    #
    #     return body


class Request:
    def __init__(self, method, path, version, headers):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers


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
