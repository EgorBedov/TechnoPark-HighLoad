from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime


def get_content_type(full_path: str):
    res = "application/unknown"
    pos = full_path.rfind('.')

    if pos == -1 or pos == len(full_path) - 1:
        return res

    fileType = full_path[pos + 1:]

    if fileType == "html" or fileType == "css":
        res = "text/" + fileType
    elif fileType == "gif" or fileType == "jpeg" or fileType == "png":
        res = "image/" + fileType
    elif fileType == "jpg":
        res = "image/jpeg"
    elif fileType == "js":
        res = "application/javascript"
    elif fileType == "swf":
        res = "application/x-shockwave-flash"

    return res


def get_date():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)
