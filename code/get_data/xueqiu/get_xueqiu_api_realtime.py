# -*- coding: utf-8 -*-
import requests
import pytz
import datetime

def get_xueqiu_realtime_data(code):
    tz = pytz.timezone('America/New_York')
    file_name = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    header = {}
    header["Host"] = "stock.xueqiu.com"
    header["Connection"] = "keep-alive"
    header["Cache-Control"] = "max-age=0"
    header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    header["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
 
    with open("../data/xueqiu_realtime_log/{}/{}_{}".format(code, file_name, code), 'a+') as f:
        r = requests.get("https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol={}".format(code), headers=header)
        f.write(r.text) 
        f.write('\n')

get_xueqiu_realtime_data(".IXIC")
get_xueqiu_realtime_data("TSLA")
get_xueqiu_realtime_data("AAPL")
get_xueqiu_realtime_data("AMD")
get_xueqiu_realtime_data("NVDA")
get_xueqiu_realtime_data("FB")
get_xueqiu_realtime_data("MSFT")
get_xueqiu_realtime_data("GOOG")
get_xueqiu_realtime_data("AMZN")
