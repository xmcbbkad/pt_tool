import pandas as pd
import os
import feature
import random

"""
name: buy above boll average
      sell below boll average
"""

class StatisticsOption():
    def __init__(self, name):
        self.name = name
        self.reset()
 
    def reset(self):
        self.win = 0
        self.lose = 0
        self.win_ratio = 0
        self.win_percent = 0
        self.lose_percent = 0
        self.net_percent = 0
    
    def add_item(self, item):
        if item.get("sell") > item.get("buy"):
            self.win += 1
            if item.get("direction", "") == "long":
                self.win_percent += (item.get("sell") - item.get("buy"))/item.get("buy")
            elif item.get("direction", "") == "short":
                self.win_percent += (item.get("sell") - item.get("buy"))/item.get("sell")
        else:
            self.lose += 1
            if item.get("direction", "") == "long":
                self.lose_percent += (item.get("buy") - item.get("sell"))/item.get("buy")
            elif item.get("direction", "") == "short":
                self.lose_percent += (item.get("buy") - item.get("sell"))/item.get("sell")
        
        self.win_ratio = self.win/(self.win+self.lose+0.1)
        self.net_percent = self.win_percent - self.lose_percent

    def print(self):
        print("date={}, win={}, lose={}, win_ratio={:.1%}, win_percent={:.1%}, lose_percent={:.1%}, net_percent={:.1%}".format(self.name, self.win, self.lose, self.win_ratio, self.win_percent, self.lose_percent, self.net_percent))


class OutputWithYearMonth():
    def __init__(self):
        self.month_statistics = []
        self.year_statistics = []   
 
    def add_item(self, date, item):
        year = date[:4]
        month = date[:7]
        
        if self.year_statistics and year == self.year_statistics[-1].name:
            self.year_statistics[-1].add_item(item)
        else:
            self.year_statistics.append(StatisticsOption(year))
            self.year_statistics[-1].add_item(item)
        
        if self.month_statistics and month == self.month_statistics[-1].name:
            self.month_statistics[-1].add_item(item)
        else:
            self.month_statistics.append(StatisticsOption(month))
            self.month_statistics[-1].add_item(item)

    def print(self):
        for item in self.month_statistics: 
            item.print()
        for item in self.year_statistics:
            item.print()    

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


def get_avg_ar(df):
    df_filtered = df.iloc[15:-15]
    average_tr = df_filtered["TR_percent"].mean()
    if pd.isna(average_tr):
        average_tr = 0 
    return average_tr

def run_all(input_dir):
    sorted_files = []
    for root, dirs, files in os.walk(input_dir):
        sorted_files.extend(os.path.join(root, file) for file in files)
    sorted_files = sorted(sorted_files)        
    
    
    ar_dict = {}
    for file in sorted_files:
        if file.endswith(".csv"):
            data = pd.read_csv(file)
            data = feature.FeatureBuilder().add_true_range(data) 
            print(file)
            date = file.split("/")[6]
            if date not in ar_dict:
                ar_dict[date] = {}
                ar_dict[date]["count"] = 0
                ar_dict[date]["amount"] = 0.0                

            ar_average = get_avg_ar(data)
            if ar_average:
                ar_dict[date]["count"] += 1 
                ar_dict[date]["amount"] += ar_average
    for key in ar_dict:
        ar_dict[key]["atr_percent"] = ar_dict[key]["amount"]/ar_dict[key]["count"]
        print(key)
        print("{:.2%}".format(ar_dict[key]["atr_percent"]))
        print(ar_dict[key])

if __name__ == "__main__":
    #run_all("/root/program_trading/data/tiger_1m_log_after/TSLA/2022/")
    #run_all("/root/program_trading/data/tiger_1m_log_after/TSLA/2022/2022-03/")
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
