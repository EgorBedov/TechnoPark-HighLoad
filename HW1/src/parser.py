from email.parser import BytesParser
import socket
import asyncio
import os
import sendfile

import constants as C
from config import SERVER_NAME
from utils import *
from files import Files
from logger import Logger as log


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
    def __init__(self, status: C.HTTP_CODE):
        self.status = status
        self.path = None

    def update(self, req: Request):
        self.method = req.method
        self.status, self.path = Files.getByPath(req.path)

    def head_to_string(self) -> str:
        if self.path is not None:
            type = get_content_type(self.path)

        tmp = 'HTTP/1.1 '+str(self.status.code)+' '+self.status.status+C.HTTP_EOF + \
            'Date: '+get_date()+C.HTTP_EOF + \
            'Server: '+SERVER_NAME+C.HTTP_EOF + \
            'Connection: Close'+C.HTTP_EOF

        if self.status == C.HTTP_STATUS_CODE_OK and self.path is not None:
            tmp += \
                'Content-Length: ' + str(os.path.getsize(self.path)) + C.HTTP_EOF + \
                'Content-Type: ' + type + C.HTTP_EOF

        tmp += C.HTTP_EOF

        return tmp

    async def send(self, sock: socket.socket):
        await asyncio.get_event_loop().sock_sendall(sock, self.head_to_string().encode(C.ENCODING))

        # send body
        if self.status == C.HTTP_STATUS_CODE_OK and self.path and self.method == C.METHOD_GET:
            with open(self.path, 'rb') as file:
                # Using lib sendfile
                offset = 0
                blocksize = os.path.getsize(self.path)
                while True:
                    sent = sendfile.sendfile(sock.fileno(), file.fileno(), offset, blocksize)
                    offset += sent
                    if sent == 0:
                        break
                
                ## Using os.sendfile
                # try:
                #     await asyncio.get_event_loop().run_in_executor(
                #         None,
                #         os.sendfile,
                #         sock.fileno(), file.fileno(),
                #         0, os.path.getsize(self.path) )
                # except (BrokenPipeError, ConnectionResetError) as e:
                #     log.l.warning(e)
                #     return

                ## Using partial read
                # part = file.read(C.MAX_LINE)
                # while len(part) > 0:
                #     try:
                #         await asyncio.get_event_loop().sock_sendall(sock, part)
                #     except (BrokenPipeError, ConnectionResetError, OSError) as e:
                #         return
                #     part = file.read(C.MAX_LINE)
