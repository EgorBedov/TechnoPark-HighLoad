METHOD_GET = 'GET'
METHOD_HEAD = 'HEAD'

MAX_LINE = 64*1024
MAX_HEADERS = 100

class HTTP_CODE:
    def __init__(self, code: int, status: str):
        self.code = code
        self.status = status

HTTP_STATUS_CODE_OK = HTTP_CODE(200, 'OK')
HTTP_STATUS_CODE_FORBIDDEN = HTTP_CODE(403, 'Forbidden')
HTTP_STATUS_CODE_NOT_FOUND = HTTP_CODE(404, 'Not Found')
HTTP_STATUS_CODE_METHOD_NOT_ALLOWED = HTTP_CODE(405, 'Method Not Allowed')
HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR = HTTP_CODE(500, 'Internal Server Error')

HTTP_EOF = '\r\n'

ENCODING = 'iso-8859-1'
