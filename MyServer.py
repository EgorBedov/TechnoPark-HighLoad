import asyncio

import constants as C
from Parser import Parser, Request, Response
from Files import Files
from utils import *


class MyServer:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        asyncio.run(self.run_server())

    async def run_server(self):
        server = await asyncio.start_server(self.serve_client, self.settings.host, self.settings.port)
        await server.serve_forever()

    async def serve_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        request = await Parser.parse_HTTP_request(reader)
        response = await self.handle_request(request)
        await self.write_response(writer, response, request)


    async def handle_request(self, request: Request) -> Response:
        if request.method == C.METHOD_GET or request.method == C.METHOD_HEAD:
            return Response(*Files.getByPath(request.path))
        else:
            return Response(C.HTTP_STATUS_CODE_METHOD_NOT_ALLOWED)


    async def write_response(self, writer: asyncio.StreamWriter, response: Response, request: Request):
        writer.write(response.to_string(request).encode('utf-8'))
        await writer.drain()
        writer.close()
