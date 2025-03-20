import pandas as pd
import os
import feature
import random
from utils.cal_metrics import TradeStaticsWithYearMonth

"""
buy when rsi_6, rsi_12, rsi_24 all at day high
sell when rsi_6, rsi_12, rsi_24 all at day low
"""

def buy_rsi_6_12_24_all_high(df, output_strategy="percent_0.5"):
    output = []
    max_rsi_6 = 50
    max_rsi_12 = 50
    max_rsi_24 = 50    

    buy_price = -1.0
    sell_price = -1.0

    for i in range(len(df)):
        if i < 15:
            continue
        if i < 30:        
            max_rsi_6 = max(max_rsi_6, df.iloc[i]["RSI_6"])        
            max_rsi_12 = max(max_rsi_12, df.iloc[i]["RSI_12"])        
            max_rsi_24 = max(max_rsi_24, df.iloc[i]["RSI_24"])        
            continue


        if len(df)-i > 15 and buy_price < 0 and df.iloc[i]["RSI_6"] > max_rsi_6 and df.iloc[i]["RSI_12"] > max_rsi_12 and df.iloc[i]["RSI_24"] > max_rsi_24:
            buy_price = df.iloc[i]["close"]
            continue 
        
        if output_strategy=="percent_0.5":
            if buy_price > 0 and sell_price < 0:
                if df.iloc[i]["low"] <= buy_price*0.995:
                    sell_price = buy_price*0.995
                elif df.iloc[i]["high"] >= buy_price*1.005:
                    sell_price = buy_price*1.005
                #elif i == len(df) - 1:
                #    sell_price = df.iloc[i]["low"]
        elif output_strategy=="boll_mean":
            if buy_price > 0 and sell_price < 0:
                if df.iloc[i]["low"] <= df.iloc[i]["boll_mean"]:
                    sell_price = df.iloc[i]["boll_mean"]
               
        if buy_price > 0 and sell_price > 0:
            output.append({"direction":"long", "buy":buy_price, "sell":sell_price})
            buy_price = -1.0
            sell_price = -1.0
        
        max_rsi_6 = max(max_rsi_6, df.iloc[i]["RSI_6"])        
        max_rsi_12 = max(max_rsi_12, df.iloc[i]["RSI_12"])        
        max_rsi_24 = max(max_rsi_24, df.iloc[i]["RSI_24"])        
    return output


def sell_rsi_6_12_24_all_low(df, output_strategy="percent_0.5"):
    output = []
    min_rsi_6 = 50
    min_rsi_12 = 50
    min_rsi_24 = 50   

    buy_price = -1.0
    sell_price = -1.0

    for i in range(len(df)):
        if i <15 :
            continue
        if i < 30:       
            min_rsi_6 = min(min_rsi_6, df.iloc[i]["RSI_6"])        
            min_rsi_12 = min(min_rsi_12, df.iloc[i]["RSI_12"])        
            min_rsi_24 = min(min_rsi_24, df.iloc[i]["RSI_24"])        
            continue
 
        if len(df)-i > 15 and sell_price < 0 and df.iloc[i]["RSI_6"] < min_rsi_6 and df.iloc[i]["RSI_12"] < min_rsi_12 and df.iloc[i]["RSI_24"] < min_rsi_24:
            sell_price = df.iloc[i]["close"]
            continue 
        
        if output_strategy=="percent_0.5": 
            if sell_price > 0 and buy_price < 0:
                if df.iloc[i]["high"] >= sell_price*1.005:
                    buy_price = sell_price*1.005
                elif df.iloc[i]["low"] <= sell_price*0.995:
                    buy_price = sell_price*0.995
                #elif i == len(df) - 1:
                #    buy_price = df.iloc[i]["high"]
        elif output_strategy=="boll_mean":
            if buy_price > 0 and sell_price < 0:
                if df.iloc[i]["high"] >= df.iloc[i]["boll_mean"]:
                    buy_price = df.iloc[i]["boll_mean"]
             
        if sell_price > 0 and buy_price > 0:
            output.append({"direction":"short", "sell":sell_price, "buy":buy_price})
            
            buy_price = -1.0
            sell_price = -1.0
 
        min_rsi_6 = min(min_rsi_6, df.iloc[i]["RSI_6"])        
        min_rsi_12 = min(min_rsi_12, df.iloc[i]["RSI_12"])        
        min_rsi_24 = min(min_rsi_24, df.iloc[i]["RSI_24"])        
    
    return output

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
            data = feature.FeatureBuilder().add_rsi(data, window=6) 
            data = feature.FeatureBuilder().add_rsi(data, window=12) 
            data = feature.FeatureBuilder().add_rsi(data, window=24) 
            output = buy_rsi_6_12_24_all_high(data, output_strategy="boll_mean")  
            #output = sell_rsi_6_12_24_all_low(data, output_strategy="boll_mean")  
            print(file)
            date = file.split("/")[-1][:10]
            print(output)
            for item in output:
                output_with_year_month.add_item(date, item)
            
    output_with_year_month.print()

if __name__ == "__main__":
    #run_all("/root/program_trading/data/tiger_1m_log_after/TSLA/2024-07")
    #run_all("/root/program_trading/data/taobao/AAPL/2022/2022-01")
    run_all("/root/program_trading/data/tiger_1m_log_after/TSLA/2023/")
    #run_all("/root/program_trading/data/taobao/AAPL/2022/")
    #run_all("/root/program_trading/data/tiger_1m_log_after/AAPL/2022/")
    exit(0)
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
