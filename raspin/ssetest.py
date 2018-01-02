import sseclient
import requests

import threading
res = sseclient.SSEClient(requests.get("http://localhost:3000/raspin-ut/sse/receive", stream=True))

for event in res.events():
    print("get event:" + event.data)
