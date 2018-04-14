from mitmproxy import http
from mitmproxy.script import concurrent
import datetime
import time
import sys
import socket

HOST_NAME = 'ae.bestdo.com'

# GET_VALID_PRICE = 'ajaxGetValidPriceTime'

API_RESERVE = 'ae.bestdo.com/mer/item/detail/ajaxGetSth'
API_SUBMIT = 'ae.bestdo.com/orders/swimbod/createOrder'

today = datetime.date.today()
swim_day = today + datetime.timedelta(7)
swim_day = "%s-%02d-%d" % (swim_day.year, swim_day.month, swim_day.day)
print(swim_day)

# swim_day = "2018-04-22"

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()

def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host != HOST_NAME:
        return

    print(flow.request)

    if flow.request.urlencoded_form and flow.request.method == 'POST':
        if (API_RESERVE in flow.request.pretty_url) or (API_SUBMIT in flow.request.pretty_url):
            flow.request.urlencoded_form["book_day"] = swim_day
            flow.request.urlencoded_form["start_hour"] = "7"
            print(flow.request.urlencoded_form)

            if API_SUBMIT == flow.request.pretty_url:
                while True:
                    now = datetime.datetime.now()
                    if now.hour == 10:
                        break
                    print(now)
                    time.sleep(0.1)

def response(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host != HOST_NAME:
        return
    print(flow.response)
