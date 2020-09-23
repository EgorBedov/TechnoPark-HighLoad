from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime


def get_content_type(full_path: str):
    res = "application/unknown"
    pos = full_path.rfind('.')
    end = full_path.find('?', pos)
    if end == -1:
         end = len(full_path)

    if pos == -1 or pos == len(full_path) - 1:
        return res

    file_type = full_path[pos + 1:end]

    if file_type == "html" or file_type == "css":
        res = "text/" + file_type
    elif file_type == "gif" or file_type == "jpeg" or file_type == "png":
        res = "image/" + file_type
    elif file_type == "jpg":
        res = "image/jpeg"
    elif file_type == "js":
        res = "application/javascript"
    elif file_type == "swf":
        res = "application/x-shockwave-flash"

    return res


def get_date():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)
