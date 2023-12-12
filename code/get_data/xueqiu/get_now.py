# -*- coding: utf-8 -*-
import requests
import json

list_code = ["SH000001", "HKHSI", "01810", "00700", "03690", "06078", "01801", "03900", "01797", "SZ002594", "SZ300750", "SH600438", "SH600795"]
list_name = ["SH", "HK", "mi", "qq", "mt", "hygeia", "xinda", "green", "xdf", "byd", "catl", "TW", "GD"]

header = {}
header["Host"] = "stock.xueqiu.com"
header["Connection"] = "keep-alive"
header["Cache-Control"] = "max-age=0"
header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
header["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"


def cal_percent(last, now):
    if not last or not now:
        return 0
    percent = 0
    if now > last:
        percent = (now-last)/last
    else:
        percent = now/last-1
    return format(percent*100, ".2f")
 
print("{}\t{}\t{}(%)\t{}\t{}".format("code", "last", "current", "low", "high"))
for i in range(len(list_code)):
    url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol={}".format(list_code[i])
    r = requests.get(url, headers=header)
    #print(r.text)
    json_dict = json.loads(r.text)["data"][0]
    print("{}\t{}\t{}({}%)\t{}({}%)\t{}({}%)".format(list_name[i], json_dict["last_close"], json_dict["current"], json_dict["percent"], json_dict["low"], cal_percent(json_dict["last_close"], json_dict["low"]), json_dict["high"], cal_percent(json_dict["last_close"], json_dict["high"])))
    if i == 1:
        print("----------------------------")
