import requests
import hmac
import hashlib
from urllib.parse import urlencode
import time

from test_config import options, endpoint


def get_default_params():
    return {'recvWindow': '60000', 'timestamp': int(time.time() * 1000)}


def request(method, path, params=None):
    resp = requests.request(method, endpoint + path, params=params)
    return resp


def signed_request(method, path, params=None):
    # preparing params
    query_dict = get_default_params()
    if params:
        query_dict.update(params)
    query = urlencode(sorted(query_dict.items()))

    # adding signature
    secret = bytes(options["secret"].encode("utf-8"))
    signature = hmac.new(secret, query.encode("utf-8"), hashlib.sha256).hexdigest()
    query += "&signature=" + signature

    # sending request
    resp = requests.request(method,
                            endpoint + path + "?" + query,
                            headers={"X-MBX-APIKEY": options["apiKey"]})
    return resp
