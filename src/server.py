import socket
import multiprocessing as mp
import select
import atexit
import asyncio

import constants as C
from logger import Logger as log
import MyConfig as config
from Parser import *
from Files import Files
import time


class MainServer:
    q = mp.Queue()

    def __init__(self):
        self.childrens_pull = []
        self.sock = None
        atexit.register(self.kill_children)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((config.HOST, config.PORT))
        sock.listen(10)

        for i in range(mp.cpu_count()):
            self.prefork(sock, MainServer.q)

        to_read = [sock]
        while True:
            ready_to_read, _, _ = select.select(to_read, [], [])
            if sock in ready_to_read:
                self.q.put('GO')
                # time.sleep(3)
                log.l.info('Socket is ready to accept')

    def prefork(self, parent_sock: socket.socket, queue: mp.Queue):
        p = mp.Process(target=worker, args=(parent_sock, queue))
        p.start()
        self.childrens_pull.append(p)

    def kill_children(self):
        for c in self.childrens_pull:
            c.terminate()
            c.join()


def worker(parent_sock: socket.socket, q: mp.Queue):
    asyncio.run(__worker(parent_sock, q))


async def __worker(parent_sock: socket.socket, q: mp.Queue):
    while True:
        msg = q.get()
        log.l.info(msg)
        if msg != 'GO':
            return
        connection, _ = parent_sock.accept()

        await handle(connection)

        connection.close()


async def handle(conn: socket.socket):
    raw = await asyncio.get_event_loop().sock_recv(conn, 1024)
    request = parse(raw)
    if request is None:
        log.l.info('Served empty request')
        return
    print('Parsed request', request)

    response = Response(C.HTTP_STATUS_CODE_METHOD_NOT_ALLOWED)
    if request.method == C.METHOD_GET or request.method == C.METHOD_HEAD:
        status, body = await Files.getByPath(request.path)
        response = Response(status, body)

    conn.sendall(response.to_string(request).encode(C.ENCODING))
