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
from tigeropen.trade.trade_client import TradeClient
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
openapi_client = TradeClient(client_config, logger=logger)

def ts2str(ts):
    ts = ts/1000
    str = datetime.datetime.fromtimestamp(ts, pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S')
    return str

def get_latest_order():
    tz = pytz.timezone('America/New_York')
    run_date = datetime.datetime.now(tz).strftime('%Y-%m-%d')
    end_ts = int(time.time())*1000
    start_ts = end_ts -86400*3*1000
    orders = openapi_client.get_orders(limit=300, start_time=start_ts, end_time=end_ts)

    df = pd.DataFrame(columns=["contract", "trade_timestamp", "trade_time", "action", "filled", "avg_fill_price"])
    for item in orders[::-1]:
        add_item ={}
        add_item["contract"] = item.contract
        add_item["trade_timestamp"] = item.trade_time
        add_item["trade_time"] = ts2str(item.trade_time) 
        add_item["action"] = item.action
        add_item["filled"] = item.filled
        add_item["avg_fill_price"]  = item.avg_fill_price 
    
        df = pd.concat([df, pd.DataFrame([add_item])], ignore_index=True)
        df['trade_time'] = pd.to_datetime(df['trade_time'])
        

    return df

def save_order(output_dir = "/root/program_trading/data/tiger_trade_log/"):
    this_df = get_latest_order()
    #print(this_df)
    #print(this_df.info())
    this_df['trade_month'] = this_df['trade_time'].dt.strftime('%Y-%m')
    
    groupd = this_df.groupby("trade_month")
    for month, group_data in groupd:
        output_file = "{}{}.csv".format(output_dir, month)
        
        if os.path.exists(output_file):
            existing_data = pd.read_csv(output_file)
            print("111 len(existing)={}".format(len(existing_data)))
            combined_data = pd.concat([existing_data, group_data], ignore_index=True)
            print("222 len(combinmed)={}".format(len(combined_data)))
        else:
            combined_data = group_data
        
        combined_data.drop('trade_month', axis=1, inplace=True)
        combined_data.drop_duplicates(subset=["trade_timestamp"], keep='first', inplace=True)
        print("333 len(duplicated combinmed)={}".format(len(combined_data)))
        combined_data.to_csv(output_file, index=False)


if __name__ == "__main__":
    #get_latest_order()
    save_order()
