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
        if request is None:
            await writer.close()
            print('Served empty request')
            return


        response = await self.handle_request(request)

        await self.write_response(writer, response, request)


    async def handle_request(self, request: Request) -> Response:
        if request.method == C.METHOD_GET or request.method == C.METHOD_HEAD:
            status, body = await Files.getByPath(request.path)
            return Response(status, body)
        else:
            return Response(C.HTTP_STATUS_CODE_METHOD_NOT_ALLOWED)


    async def write_response(self, writer: asyncio.StreamWriter, response: Response, request: Request):
        writer.write(response.to_string(request).encode(C.ENCODING))
        await writer.drain()
        writer.close()
