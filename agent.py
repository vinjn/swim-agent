from mitmproxy import http, ctx
from mitmproxy.script import concurrent
import datetime
import time
import sys
import socket
from os import system

passthrough_mode = False
HOST_NAME = 'ae.bestdo.com'

# GET_VALID_PRICE = 'ajaxGetValidPriceTime'

API_RESERVE = 'ae.bestdo.com/mer/item/detail/ajaxGetSth'
API_SUBMIT = 'ae.bestdo.com/orders/swimbod/createOrder'

today = datetime.date.today()
swim_day = today + datetime.timedelta(7)
swim_day = "%s-%02d-%d" % (swim_day.year, swim_day.month, swim_day.day)
print(swim_day)

# swim_day = "2018-04-22"
ip_address = "N/A"
for i in socket.getaddrinfo(socket.gethostname(), None):
    ip_address = i[4][0]
    print(ip_address)

system("title " + ip_address + ':' + str(ctx.options.listen_port))

def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host != HOST_NAME:
        return

    if passthrough_mode and flow.request.urlencoded_form and flow.request.method == 'POST':
        print(flow.request.urlencoded_form)
        return

    print(flow.request)

    if flow.request.urlencoded_form and flow.request.method == 'POST':
        if (API_RESERVE in flow.request.pretty_url) or (API_SUBMIT in flow.request.pretty_url):
            flow.request.urlencoded_form["book_day"] = swim_day
            flow.request.urlencoded_form["start_hour"] = "7"
            print(flow.request.urlencoded_form)

            if API_RESERVE in flow.request.pretty_url:
                print('\n\n=====API_RESERVE=====\n\n')

            if API_SUBMIT in flow.request.pretty_url:
                while True:
                    now = datetime.datetime.now()
                    if now.hour == 10:
                        print('\n\n=====API_SUBMIT=====\n\n')
                        break
                    print(now)
                    time.sleep(0.1)

def response(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host != HOST_NAME:
        return
    print(flow.response)
