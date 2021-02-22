import http.client
import json

from settings import GNS_SERVER_HOST, GNS_SERVER_PORT


def send_request(method, url, param=None, return_data=False):
    """
    Sends an HTTP request to the GNS3 server
    :param method: HTTP method to use
    :param url: URL for the request
    :param param: Optional parameter to send to the GNS3 server
    :param return_data: Flag indicating whether the request returns data (in JSON format)
    :return: Status of the request or parsed JSON data if return_data == True
    """
    conn = http.client.HTTPConnection(GNS_SERVER_HOST, GNS_SERVER_PORT)
    if param is not None:
        conn.request(method, url, param)
    else:
        conn.request(method, url)

    r = conn.getresponse()
    if return_data:
        data = r.read()
        jdata = json.loads(data)
        conn.close()
        return jdata
    else:
        conn.close()
        return r.status
