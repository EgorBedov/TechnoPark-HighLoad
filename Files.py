from typing import Tuple
import os
from aiofile import AIOFile

from MyConfig import GLOBAL_PATH

class Files:
    # calling os.isfile is a heavy operation
    # consider checking once and then storing the result
    @staticmethod
    def getByPath(filename: str) -> Tuple[int, str]:
        # find the file otherwise return 404
        status = 404
        body = ''

        full_path = GLOBAL_PATH + filename

        if os.path.isfile(full_path):
            status = 200
        else:
            status = 404

        return status, body
