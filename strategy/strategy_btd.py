import pandas as pd
import os
import feature


"""
name: buy the dip/sell the top
"""

def buy_the_dip(df):
    output_continue_down = []
    output_invert = []
    for i in range(len(df)):
        if df.iloc[i]["continue_10_down"]:
            output_continue_down.append(df.iloc[i]["time_str"])
        if df.iloc[i]["continue_10_down_invert"]:
            output_invert.append(df.iloc[i]["time_str"])
    return output_continue_down, output_invert

def run_all(input_dir):
    sorted_files = []
    for root, dirs, files in os.walk(input_dir):
        sorted_files.extend(os.path.join(root, file) for file in files)
    sorted_files = sorted(sorted_files)        
    for file in sorted_files:
        if file.endswith(".csv"):
            data = pd.read_csv(file)
            data = feature.FeatureBuilder().add_continue_down(data) 
            data = feature.FeatureBuilder().add_continue_down_invert(data) 
    
            output_continue_down, output_invert = buy_the_dip(data)
            if output_continue_down:
                print(file)
                print("continue_down:{}".format(output_continue_down))
                print("invert:{}".format(output_invert))

if __name__ == "__main__":
    run_all("/root/program_trading/data/tiger_1m_log_after/TSLA")
    #code = "TSLA"
    #date = "2024-03-21"
    #data = pd.read_csv('/root/program_trading/data/tiger_1m_log_after/{}/{}/{}.csv'.format(code, date[:7], date))
    #buy_the_dip(data)
