from mitmproxy import http
from mitmproxy.script import concurrent
import datetime
import time
import sys

HOST_NAME = 'ae.bestdo.com'

# GET_VALID_PRICE = 'ajaxGetValidPriceTime'

API_RESERVE = 'https://ae.bestdo.com/mer/item/detail/ajaxGetSth'
API_SUBMIT = 'http://ae.bestdo.com/orders/swimbod/createOrder'

target_date = "2018-04-17"

def start():
    if len(sys.argv) == 2:
        global target_date
        target_date = sys.argv[1]

def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host != HOST_NAME:
        return

    print(flow.request)

    if flow.request.urlencoded_form:
        if flow.request.pretty_url in (API_RESERVE, API_SUBMIT):
            flow.request.urlencoded_form["book_day"] = target_date
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
