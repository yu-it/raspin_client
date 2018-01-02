import sseclient
import requests

import threading
res = sseclient.SSEClient(requests.get("http://192.168.2.123:3000/raspin-ut/sse/receive", stream=True))

for event in res.events():
    print("get event:" + event.data)
