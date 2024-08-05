import pandas as pd
import os
import feature


"""
name: buy the dip/sell the top
"""

def buy_the_dip(df):
    for i in range(len(df)):
        if df.iloc[i]["continue_10_down"]:
            print(df.iloc[i])        

def run_all(input_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".csv"):
                data = pd.read_csv(file_path)
                data = feature.FeatureBuilder().add_continue_down(data) 
    
                buy_the_dip(data)                

if __name__ == "__main__":
    run_all("/root/program_trading/data/tiger_1m_log_after/TSLA")
    #code = "TSLA"
    #date = "2024-03-21"
    #data = pd.read_csv('/root/program_trading/data/tiger_1m_log_after/{}/{}/{}.csv'.format(code, date[:7], date))
    #buy_the_dip(data)
