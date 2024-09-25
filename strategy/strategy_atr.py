import pandas as pd
import os
import feature
import random

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
