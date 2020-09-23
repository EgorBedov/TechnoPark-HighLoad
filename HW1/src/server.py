import multiprocessing as mp
import atexit
import uvloop

from logger import Logger as log
from config import *
from parser import *


class MainServer:
    def __init__(self):
        self.childrens_pull = []
        self.sock = None
        atexit.register(self.kill_children)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        log.l.info(f'Server is running on {HOST}:{PORT}')
        sock.listen(MAX_CONNECTIONS)
        sock.setblocking(False)

        uvloop.install()

        for i in range(CORES):
            self.prefork(sock)

        try:
            for worker in self.childrens_pull:
                worker.join()
        except KeyboardInterrupt:
            for worker in self.childrens_pull:
                worker.terminate()
            sock.close()
            log.l.info('Server was manually stopped')

    def prefork(self, parent_sock: socket.socket):
        p = mp.Process(target=worker, args=(parent_sock, ))
        p.start()
        self.childrens_pull.append(p)

    def kill_children(self):
        for c in self.childrens_pull:
            c.terminate()
            c.join()


def worker(parent_sock: socket.socket):
    asyncio.run(__worker(parent_sock))


async def __worker(parent_sock: socket.socket):
    while True:
        child_sock, _ = await asyncio.get_event_loop().sock_accept(parent_sock)
        await handle(child_sock)
        child_sock.close()


async def handle(sock: socket.socket):
    raw = await asyncio.get_event_loop().sock_recv(sock, 1024)
    request = parse(raw)
    if request is None:
        log.l.info('Served empty request')
        return

    response = Response(C.HTTP_STATUS_CODE_METHOD_NOT_ALLOWED)
    if request.method == C.METHOD_GET or request.method == C.METHOD_HEAD:
        response.update(request)

    await response.send(sock)
