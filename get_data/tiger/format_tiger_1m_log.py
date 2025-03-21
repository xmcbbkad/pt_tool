# -*- coding: utf-8 -*-
import os,sys
import json
import pytz,time,datetime
import pandas as pd

def get_dir_result(code, input_dir, output_dir):
    file_list = [file for file in os.listdir(input_dir) if file.endswith('.csv')]
    
    first_file_path = os.path.join(input_dir, file_list[0])
    header = pd.read_csv(first_file_path, nrows=0).columns
    combined_df = pd.DataFrame(columns=header)
    
    for f in file_list:
        file_path = os.path.join(input_dir, f)
        df = pd.read_csv(file_path)
        if not combined_df.empty and not df.empty:    
            combined_df = pd.concat([combined_df, df], ignore_index=True)        
        elif not df.empty:
            combined_df = df.copy()


    unique_combined_df = combined_df.drop_duplicates()
   
 
    unique_combined_df['date'] = pd.to_datetime(unique_combined_df['time_str'], format='%Y-%m-%d %H:%M:%S')
    print(unique_combined_df.info())

    unique_combined_df['DateOnly'] = unique_combined_df['date'].dt.date

    
    grouped = unique_combined_df.groupby("DateOnly")
    #grouped = unique_combined_df.groupby("time_str")
    for period, group_data in grouped:
        month = group_data['date'].dt.strftime('%Y-%m').iloc[0]
        #group_data['DateOnly'] = pd.to_datetime(group_data['time_str'])
        #month = group_data['DateOnly'].dt.strftime('%Y-%m').iloc[0]
        group_data.drop('DateOnly', axis=1, inplace=True)
        group_data.drop('time', axis=1, inplace=True)
        group_data.drop('time_str', axis=1, inplace=True)
        group_data.drop('symbol', axis=1, inplace=True)

        cols = ['date'] + [col for col in group_data if col != 'date']
        group_data = group_data[cols]

        #new_output_dir = "{}{}".format(output_dir, month)
        new_output_dir = os.path.join(output_dir, month[:4], month)
        if not os.path.exists(new_output_dir):
            os.makedirs(new_output_dir)

        filename = "{}/{}.csv".format(new_output_dir, period)
        group_data.to_csv(filename, index=False)


def run_all(code_list=[], month_list=[], input_dir="/root/program_trading/data/tiger_1m_log"):
    if not code_list:
        code_list = [f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))] 
        print(code_list)
    if not month_list:
        code_dir = os.path.join(input_dir, "TSLA")
        month_list = [f for f in os.listdir(code_dir) if os.path.isdir(os.path.join(code_dir, f))] 
        print(month_list)
    
    for code in code_list:
        for month in month_list:
            print("{}--{}".format(code, month))
            input_dir = "/root/program_trading/data/tiger_1m_log/{}/{}/".format(code, month)
            output_dir = "/root/program_trading/data/tiger_1m_log_after/{}/".format(code)
            get_dir_result(code, input_dir, output_dir) 
 


if __name__ == "__main__":
    #code = sys.argv[1]
    #month = sys.argv[2]
    #input_dir = "/root/program_trading/data/tiger_1m_log/{}/{}/".format(code, month)
    #output_dir = "/root/program_trading/data/tiger_1m_log_after/{}/".format(code)
    #
    #get_dir_result(code, input_dir, output_dir)
    #run_all(code_list=["AAPL"])
    month_list=["2025-03"]
    run_all(month_list=month_list)
     
