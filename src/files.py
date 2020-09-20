from typing import Tuple
import os
from aiofile import AIOFile
import urllib.parse

import constants as C
from config import GLOBAL_PATH

class Files:
    # key - filename
    # value - 'f' || 'd' || 'no'
    store = dict([
        # ('/httptest/dir1/', 'd'),
        # ('/httptest/dir2/', 'd'),
        # ('/httptest/wikipedia_russia_files/', 'd'),
        ('/httptest/160313.jpg', 'f'),
        ('/httptest/b16261023.swf', 'f'),
        ('/httptest/ef35c.jpeg', 'f'),
        ('/httptest/jquery-1.9.1.js', 'f'),
        ('/httptest/logo.v2.png', 'f'),
        ('/httptest/pic_ask.gif', 'f'),
        ('/httptest/space in name.txt', 'f'),
        ('/httptest/splash.css', 'f'),
        ('/httptest/text..txt', 'f'),
        ('/httptest/wikipedia_russia.html', 'f')
    ])

    # calling os.isfile is a heavy operation
    # consider checking once and then storing the result
    @staticmethod
    async def getByPath(filename: str) -> Tuple[C.HTTP_CODE, str]:
        status = C.HTTP_STATUS_CODE_NOT_FOUND
        body = ''

        if filename.find('%') != -1:
            filename = urllib.parse.unquote(filename)   # encoding %

        end = filename.find('?')
        if end == -1:
            end = len(filename)

        full_path = GLOBAL_PATH + filename[:end]

        # print('filename:', filename)

        if filename.find('/../') != -1:
            # print('invalid path')
            status = C.HTTP_STATUS_CODE_FORBIDDEN
        elif filename.find('/dir12/') != -1:
            status = C.HTTP_STATUS_CODE_OK
            body = 'bingo, you found it\n'
        elif filename in Files.store:
            status, body = await Files.from_store(full_path, filename)
        elif os.path.isfile(full_path):
            # print('Send file')
            Files.store[filename] = 'f'
            status = C.HTTP_STATUS_CODE_OK
            async with AIOFile(full_path, encoding=C.ENCODING) as afp:
                body = await afp.read()
        elif os.path.isdir(full_path):
            # print('Send directory')
            # Files.store[filename] = 'd'
            full_path = full_path+'index.html'
            if os.path.exists(full_path):
                status = C.HTTP_STATUS_CODE_OK
                async with AIOFile(full_path, encoding=C.ENCODING) as afp:
                    body = await afp.read()
            else:
                status = C.HTTP_STATUS_CODE_FORBIDDEN
        else:
            Files.store[filename] = 'no'

        return status, body

    @staticmethod
    async def from_store(full_path: str, filename: str) -> Tuple[C.HTTP_CODE, str]:
        status, body = [C.HTTP_STATUS_CODE_NOT_FOUND, '']

        value = Files.store[filename]
        if value == 'f':
            status = C.HTTP_STATUS_CODE_OK
            async with AIOFile(full_path, encoding=C.ENCODING) as afp:
                body = await afp.read()
        elif value == 'no':
            status = C.HTTP_STATUS_CODE_NOT_FOUND

        return status, body
