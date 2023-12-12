# -*- coding: utf-8 -*-
import os,sys
import json
import datetime
import time
import pytz
import logging
import pandas as pd
from tigeropen.common.consts import Language, BarPeriod
from tigeropen.quote.domain.filter import OptionFilter
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a', )
logger = logging.getLogger('TigerOpenApi')


def get_client_config(config_file = "/root/program_trading/code/pt_tool/code/get_data/tiger/tiger_api_config.json"):
    """
    https://www.itiger.com/openapi/info 开发者信息获取
    :return:
    """
    
    tiger_api_config = json.load(open(config_file,'r'))

    is_sandbox = False
    client_config = TigerOpenClientConfig(sandbox_debug=is_sandbox)
    client_config.private_key = read_private_key(tiger_api_config.get("private_key", ""))
    client_config.tiger_id = tiger_api_config.get("tiger_id", "")
    client_config.account = tiger_api_config.get("account", "")  # 环球账户
    client_config.standard_account = None  # 标准账户
    client_config.paper_account = None  # 模拟账户
    client_config.language = Language.en_US
    return client_config


client_config = get_client_config()
openapi_client = QuoteClient(client_config, logger=logger)

def ts2str(ts):
    ts = ts/1000
    str = datetime.datetime.fromtimestamp(ts, pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S')
    return str

def get_1m_data(code):
    tz = pytz.timezone('America/New_York')
    run_date = datetime.datetime.now(tz).strftime('%Y-%m-%d')
    run_month = datetime.datetime.now(tz).strftime('%Y-%m')
    ts = (int(time.time())-86400*3)*1000 
    bars = openapi_client.get_bars(symbols=[code], begin_time=ts, period=BarPeriod.ONE_MINUTE, limit=5000)
    
    time_str = bars['time'].apply(ts2str)
    bars.insert(1, 'time_str', time_str)
   
    
    directory = "/root/program_trading/data/tiger_1m_log/{}/{}".format(code, run_month)
    if not os.path.exists(directory):
        os.makedirs(directory) 
 
    bars.to_csv("{}/{}.csv".format(directory, run_date), index=0)

if __name__ == '__main__':
    get_1m_data(".IXIC")
    time.sleep(10)
    get_1m_data("TSLA")
    time.sleep(10)
    get_1m_data("AAPL")
    time.sleep(10)
    get_1m_data("AMD")
    time.sleep(10)
    get_1m_data("NVDA")
    time.sleep(10)
    get_1m_data("MSFT")
    time.sleep(10)
    get_1m_data("GOOG")
    time.sleep(10)
    get_1m_data("AMZN")
