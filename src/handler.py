import http.client
import json
from decouple import config

def makeAPIRequest(method, url):
    apiConn = http.client.HTTPConnection(config('API_URL_HOST'), int(config('API_URL_PORT')), timeout=10)
    apiConn.request(method, url)
    res = apiConn.getresponse()
    if res.status == 401:
        print("Unauthorized User")
        #displayMessage("Unauthorized User")
        return {}
    elif res.status != 200:
        print("Unexpected error, please check server logs")
        #displayMessage("Unexpected error")
        return {}
    data = res.read()
    apiConn.close()
    return json.loads(data)