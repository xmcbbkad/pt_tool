# -*- coding: utf-8 -*-
import requests
import datetime
import pytz
import time

def get_xueqiu_1m_data(code):
    tz = pytz.timezone('America/New_York')
    file_name = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    r = requests.get("https://xueqiu.com", headers={"user-agent":"Mozilla"})

    header = {}
    header["Host"] = "stock.xueqiu.com"
    header["Connection"] = "keep-alive"
    header["Cache-Control"] = "max-age=0"
    header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    header["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    header["cookie"] = "xq_a_token={};".format(r.cookies["xq_a_token"])
    
    time_stamp = int(round(time.time() * 1000)) + 10000


    with open("../data/xueqiu_1m_log/{}/{}_{}".format(code, file_name, code), 'a+') as f:
        url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin={}&period=1m&type=before&count=-2".format(code, time_stamp)
        r = requests.get(url, headers=header)
        f.write(r.text) 
        f.write('\n')


get_xueqiu_1m_data(".IXIC")
get_xueqiu_1m_data("TSLA")
get_xueqiu_1m_data("AAPL")
get_xueqiu_1m_data("AMD")
get_xueqiu_1m_data("NVDA")
get_xueqiu_1m_data("FB")
get_xueqiu_1m_data("MSFT")
get_xueqiu_1m_data("GOOG")
get_xueqiu_1m_data("AMZN")

