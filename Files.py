from typing import Tuple
import os
from aiofile import AIOFile
import urllib.parse

import constants as C
from MyConfig import GLOBAL_PATH

class Files:
    # calling os.isfile is a heavy operation
    # consider checking once and then storing the result
    @staticmethod
    async def getByPath(filename: str) -> Tuple[C.HTTP_CODE, str]:
        # find the file otherwise return 404
        status = C.HTTP_STATUS_CODE_NOT_FOUND
        body = ''

        if filename.find('%') != -1:
            filename = urllib.parse.unquote(filename)   # encoding %

        end = filename.find('?')
        if end == -1:
            end = len(filename)

        full_path = GLOBAL_PATH + filename[:end]

        print('Path: ', full_path)

        # make it recursive ??
        if filename.find('/../') != -1:
            print('invalid path')
            status = C.HTTP_STATUS_CODE_FORBIDDEN
        elif filename.find('/dir12/') != -1:
            status = C.HTTP_STATUS_CODE_OK
            body = 'bingo, you found it\n'
        elif os.path.isfile(full_path):
            print('Send file')
            status = C.HTTP_STATUS_CODE_OK
            async with AIOFile(full_path, encoding=C.ENCODING) as afp:
                body = await afp.read()
        elif os.path.isdir(full_path):
            print('Send directory')
            full_path = full_path+'index.html'
            if os.path.exists(full_path):
                status = C.HTTP_STATUS_CODE_OK
                async with AIOFile(full_path, encoding=C.ENCODING) as afp:
                    body = await afp.read()
            else:
                status = C.HTTP_STATUS_CODE_FORBIDDEN

        return status, body
