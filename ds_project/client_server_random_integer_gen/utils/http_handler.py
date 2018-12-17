import re
import sys
import datetime
from time import mktime
from email.utils import formatdate


class HttpHandler(object):

    def __init__(self):
        self.http_post_string = "POST /server_manager.py HTTP/1.0\nUser-Agent: python_client\n" \
                                "Content-Type: application/x-www-form-urlencoded\nContent-Length: {}\ndate: {}\n\n{}"
        self.http_response_string = "HTTP/1.1 200 OK\nDate: {}\nServer: Python_server\nContentLength: {}\nContent-Type:" \
                                    " text\n\n{}"

    def http_request_encode(self, key, value):
        key_val = "{}: {}".format(str(key),str(value))
        http_current_date = self._get_current_date_in_http_format()
        return self.http_post_string.format(str(sys.getsizeof(key_val)), str(http_current_date), key_val)

    def http_request_decode(self, message):
        re_object = re.search("\n\n([\w\d_]+):\s+([\w_\d]+)", str(message))
        print(re_object)
        print(re_object.group(0), re_object.group(1), re_object.group(2))
        if re_object:
            return re_object.group(1), re_object.group(2)
        else:
            raise Exception("Message not in http format")

    def http_response_encode(self, message):
        http_current_date = self._get_current_date_in_http_format()
        content_length = sys.getsizeof(str(message))
        return self.http_response_string.format(str(http_current_date), str(content_length), str(message))

    def http_response_decode(self, message):
        re_object = re.search("\n\n([\w\s\d\(\'\.\,\)]+)", str(message))
        if re_object:
            return re_object.group(1)
        else:
            raise Exception("Message not in http format")



    def _get_current_date_in_http_format(self):
        now = datetime.datetime.now()
        stamp = mktime(now.timetuple())
        return formatdate(timeval=stamp, localtime=False, usegmt=True)



# print(HttpHandler().http_request_encode("str_time", 10))
# print("\n\n\n")
# print(HttpHandler().http_response_encode("server slept fot 10 seconds"))
#
# print(HttpHandler().http_request_decode("POST /server_manager.py HTTP/1.0\nUser-Agent: python_client\nContent-Type: application/x-www-form-urlencoded\nContent-Length: 60\ndate:Wed, 26 Sep 2018 20:48:45 GMT\n\nstr_time: 10"))
# print(HttpHandler().http_response_decode("HTTP/1.1 200 OK\nDate: Wed, 26 Sep 2018 20:48:45 GMT\nServer: Python_server\nContentLength: 76\nContent-Type:text\n\nserver slept fot 10 seconds"))

# "POST /server_manager.py HTTP/1.0\nUser-Agent: python_client\nContent-Type: application/x-www-form-urlencoded\nContent-Length: 60\ndate:Wed, 26 Sep 2018 20:48:45 GMT\n\nstr_time:10"

# "HTTP/1.1 200 OK\nDate: Wed, 26 Sep 2018 20:48:45 GMT\nServer: Python_server\nContentLength: 76\nContent-Type:text\n\nserver slept fot 10 seconds"