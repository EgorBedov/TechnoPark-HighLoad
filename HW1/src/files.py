from typing import Tuple
import os
import urllib.parse

import constants as C
import config as config

class Files:
    GLOBAL_PATH = config.GLOBAL_PATH
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
    def getByPath(filename: str) -> Tuple[C.HTTP_CODE, str]:
        status = C.HTTP_STATUS_CODE_NOT_FOUND

        if filename.find('%') != -1:
            filename = urllib.parse.unquote(filename)   # encoding %

        end = filename.find('?')
        if end == -1:
            end = len(filename)

        full_path = Files.GLOBAL_PATH + filename[:end]

        if filename.find('/..') != -1:
            status = C.HTTP_STATUS_CODE_FORBIDDEN
        elif filename in Files.store:
            status = Files.from_store(filename)
        elif os.path.isfile(full_path):
            Files.store[filename] = 'f'
            status = C.HTTP_STATUS_CODE_OK
        elif os.path.isdir(full_path):
            full_path = full_path+C.DIRECTORY_INDEX_FILENAME
            if os.path.exists(full_path):
                status = C.HTTP_STATUS_CODE_OK
            else:
                status = C.HTTP_STATUS_CODE_FORBIDDEN
        else:
            Files.store[filename] = 'no'

        return status, full_path

    @staticmethod
    def from_store(filename: str) -> C.HTTP_CODE:
        status = C.HTTP_STATUS_CODE_NOT_FOUND

        value = Files.store[filename]
        if value == 'f':
            status = C.HTTP_STATUS_CODE_OK
        elif value == 'no':
            status = C.HTTP_STATUS_CODE_NOT_FOUND

        return status

    @staticmethod
    def read_config(mode: str):
        if mode == 'deploy':
            Files.GLOBAL_PATH = '/http-test-suite'
