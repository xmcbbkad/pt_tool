import pandas as pd
import os
import feature
import random
from utils.cal_metrics import TradeStaticsWithYearMonth

"""
name: buy above boll average
      sell below boll average
"""

def random_buy_above_average(df):
    output = []
    buy_price = -1.0
    sell_price = -1.0
    buy_time = ""
    sell_time = ""
    for i in range(len(df)):
        if i <= 15:
            continue
        #if buy_price < 0 and random.random()<=0.1  and df.iloc[i]["close"] > df.iloc[i]["boll_mean"]:
        if len(df)-i > 15 and buy_price < 0 and df.iloc[i]["close"] > df.iloc[i]["boll_mean"]:
        #if buy_price < 0 and df.iloc[i]["low"] < df.iloc[0]["open"] and df.iloc[i]["close"] > df.iloc[i]["boll_mean"] and df.iloc[i]["close"]*1.005 < df.iloc[i]["boll_upper"]:
            buy_price = df.iloc[i]["close"]
            continue

        if buy_price > 0 and sell_price < 0:
            if df.iloc[i]["low"] <= buy_price*0.995:
                sell_price = buy_price*0.995
            elif df.iloc[i]["high"] >= buy_price*1.005:
                sell_price = buy_price*1.005
            #elif i == len(df) - 1:
            #    sell_price = df.iloc[i]["low"]
             
        if buy_price > 0 and sell_price > 0:
            output.append({"direction":"long", "buy":buy_price, "sell":sell_price})
            buy_price = -1.0
            sell_price = -1.0
    return output
    #return output[:1]

def random_sell_below_average(df):
    output = []
    sell_price = -1.0
    buy_price = -1.0
    buy_time = ""
    sell_time = ""
    for i in range(len(df)):
        #if sell_price < 0 and random.random()<0.1 and df.iloc[i]["close"] < df.iloc[i]["boll_mean"]:
        #if sell_price < 0 and df.iloc[i]["high"] > df.iloc[0]["open"] and df.iloc[i]["close"] < df.iloc[i]["boll_mean"] and df.iloc[i]["close"]*0.995 > df.iloc[i]["boll_lower"]:
        #    sell_price = df.iloc[i]["close"]
        #    continue
        if i <=15:
            continue
        if len(df)-i > 15 and sell_price < 0 and df.iloc[i]["close"] < df.iloc[i]["boll_mean"]:
            sell_price = df.iloc[i]["close"]
            continue

        if sell_price > 0 and buy_price < 0:
            if df.iloc[i]["high"] >= sell_price*1.005:
                buy_price = sell_price*1.005
            elif df.iloc[i]["low"] <= sell_price*0.995:
                buy_price = sell_price*0.995
            #elif i == len(df) - 1:
            #    buy_price = df.iloc[i]["high"]
             
        if sell_price > 0 and buy_price > 0:
            output.append({"direction":"short", "sell":sell_price, "buy":buy_price})
            
            buy_price = -1.0
            sell_price = -1.0
    
    return output

def random_buy_below_average(df):
    output = []
    buy_price = -1.0
    sell_price = -1.0
    buy_time = ""
    sell_time = ""
    for i in range(len(df)):
        if i <=15:
            continue
        if len(df)-i > 15 and buy_price < 0 and df.iloc[i]["close"] < df.iloc[i]["boll_mean"]:
        #if buy_price < 0 and df.iloc[i]["low"] < df.iloc[0]["open"] and df.iloc[i]["close"] > df.iloc[i]["boll_mean"] and df.iloc[i]["close"]*1.005 < df.iloc[i]["boll_upper"]:
            buy_price = df.iloc[i]["close"]
            continue

        if buy_price > 0 and sell_price < 0:
            if df.iloc[i]["low"] <= buy_price*0.995:
                sell_price = buy_price*0.995
            elif df.iloc[i]["high"] >= buy_price*1.005:
                sell_price = buy_price*1.005
            #elif i == len(df) - 1:
            #    sell_price = df.iloc[i]["low"]
             
        if buy_price > 0 and sell_price > 0:
            output.append({"direction":"long", "buy":buy_price, "sell":sell_price})
            buy_price = -1.0
            sell_price = -1.0
    
    return output

def random_sell_above_average(df):
    output = []
    sell_price = -1.0
    buy_price = -1.0
    buy_time = ""
    sell_time = ""
    for i in range(len(df)):
        #if sell_price < 0 and random.random()<0.1 and df.iloc[i]["close"] < df.iloc[i]["boll_mean"]:
        #if sell_price < 0 and df.iloc[i]["high"] > df.iloc[0]["open"] and df.iloc[i]["close"] < df.iloc[i]["boll_mean"] and df.iloc[i]["close"]*0.995 > df.iloc[i]["boll_lower"]:
        #    sell_price = df.iloc[i]["close"]
        #    continue
        if i <=15:
            continue
        #if sell_price < 0  and random.random()<=0.1 and df.iloc[i]["close"] > df.iloc[i]["boll_mean"]:
        if len(df)-i > 15 and sell_price < 0 and df.iloc[i]["close"] > df.iloc[i]["boll_mean"]:
            sell_price = df.iloc[i]["close"]
            continue

        if sell_price > 0 and buy_price < 0:
            if df.iloc[i]["high"] >= sell_price*1.005:
                buy_price = sell_price*1.005
            elif df.iloc[i]["low"] <= sell_price*0.995:
                buy_price = sell_price*0.995
            #elif i == len(df) - 1:
            #    buy_price = df.iloc[i]["high"]
             
        if sell_price > 0 and buy_price > 0:
            output.append({"direction":"short", "sell":sell_price, "buy":buy_price})
            
            buy_price = -1.0
            sell_price = -1.0
   
    return output
    #return output[:1]

def run_all(input_dir):
    sorted_files = []
    for root, dirs, files in os.walk(input_dir):
        sorted_files.extend(os.path.join(root, file) for file in files)
    sorted_files = sorted(sorted_files)        
    

    output_with_year_month = TradeStaticsWithYearMonth()
    
    for file in sorted_files:
        if file.endswith(".csv"):
            data = pd.read_csv(file)
            data = feature.FeatureBuilder().add_boll(data) 
            #output = random_buy_above_average(data)  
            #output = random_sell_below_average(data)  
            #output = random_buy_below_average(data)  
            output = random_sell_above_average(data)  
            print(file)
            date = file.split("/")[-1][:10]
            print(output)
            for item in output:
                output_with_year_month.add_item(date, item)
            
    output_with_year_month.print()

if __name__ == "__main__":
    #run_all("/root/program_trading/data/tiger_1m_log_after/TSLA/2024-07")
    #run_all("/root/program_trading/data/taobao/AAPL/2022/2022-01")
    #run_all("/root/program_trading/data/taobao/AAPL/2022/")
    #run_all("/root/program_trading/data/tiger_1m_log_after/AAPL/2022/")
    #exit(0)
    #run_all("/root/program_trading/data/tiger_1m_log_after/TSLA")
    
    base_data_dir_1 = "/root/program_trading/data/taobao/"
    base_data_dir_2 = "/root/program_trading/data/tiger_1m_log_after"

    print("start AAPL")
    run_all(os.path.join(base_data_dir_1, "AAPL"))
    print("-----------------")
    run_all(os.path.join(base_data_dir_2, "AAPL"))
    print("-----------------")
    print("start AMD")
    run_all(os.path.join(base_data_dir_1, "AMD"))
    print("-----------------")
    run_all(os.path.join(base_data_dir_2, "AMD"))
    print("-----------------")
    print("start AMZN")
    run_all(os.path.join(base_data_dir_1, "AMZN"))
    print("-----------------")
    run_all(os.path.join(base_data_dir_2, "AMZN"))
    print("-----------------")
    print("start GOOG")
    run_all(os.path.join(base_data_dir_1, "GOOG"))
    print("-----------------")
    run_all(os.path.join(base_data_dir_2, "GOOG"))
    print("-----------------")
    print("start MSFT")
    run_all(os.path.join(base_data_dir_1, "MSFT"))
    print("-----------------")
    run_all(os.path.join(base_data_dir_2, "MSFT"))
    print("-----------------")
    print("start NVDA")
    run_all(os.path.join(base_data_dir_1, "NVDA"))
    print("-----------------")
    run_all(os.path.join(base_data_dir_2, "NVDA"))
    print("-----------------")
    print("start TSLA")
    run_all(os.path.join(base_data_dir_1, "TSLA"))
    print("-----------------")
    run_all(os.path.join(base_data_dir_2, "TSLA"))
    

    #code = "TSLA"
    #date = "2024-03-21"
    #data = pd.read_csv('/root/program_trading/data/tiger_1m_log_after/{}/{}/{}.csv'.format(code, date[:7], date))
    #buy_the_dip(data)
