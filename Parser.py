import asyncio

from MyConfig import SERVER_NAME
from utils import *

import constants as C


class Parser:
    @staticmethod
    async def parse_HTTP_request(reader: asyncio.StreamReader):
        method, path, ver = await Parser.parse_request_line(reader)
        headers = await Parser.parse_headers(reader)
        body = await Parser.parse_body(reader)
        return Request(method, path, ver, headers, body)

    @staticmethod
    async def parse_request_line(reader: asyncio.StreamReader):
        raw = await reader.readline()

        req_line = raw.decode('iso-8859-1')
        req_line = req_line.rstrip('\r\n')
        words = req_line.split()
        # if len(words) != 3:
        #     raise Exception('Malformed request line')

        print(words)

        return words    #['GET', 'path', 'http/1.1']

    @staticmethod
    async def parse_headers(reader: asyncio.StreamReader) -> dict:
        headers = []
        while True:
            raw = await reader.readline()
            line = raw.decode('utf-8')
            # if len(line) > C.MAX_LINE:
            #     raise Exception('Header line is too long')

            print(line)

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

    @staticmethod
    async def parse_body(reader: asyncio.StreamReader):
        body = ''

        while True:
            chunk = await reader.read(8)
            if chunk == b'\r\n':
                break
            body += chunk.decode('utf-8')

        print(body)
        return body


class Request:
    def __init__(self, method, path, version, headers, body):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body


class Response:
    def __init__(self, status, body=''):
        self.status = status
        self.body = body

    def to_string(self, type: str, with_body: bool) -> str:
        tmp = \
            f'HTTP/1.1 {self.status}\n' \
            f'Date: {get_date()}\n' \
            f'Server: {SERVER_NAME}\n' \
            'Connection: Close\n'

        if self.body is not None and len(self.body):
            tmp = tmp + \
                f'Content-Length: {len(self.body)}\n' \
                f'Content-Type: {type}\n' + C.HTTP_EOF

        if with_body:
            tmp = tmp + self.body

        tmp = tmp + C.HTTP_EOF

        return tmp
