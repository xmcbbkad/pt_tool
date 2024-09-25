# -*- coding: utf-8 -*-
import os
import sys
import json
import pytz
import datetime

def in_filter(f, filter):
    if not filter:
        return True
    
    filter = filter.split('_')
    for kw in filter:
        if kw in f:
            return True
    return False

def get_dir_result(dir_name, code, filter, output_dir):
    file_list = os.listdir(dir_name)
    timestamp_dict = {}
    output_list = []
    for f in file_list:
        if not in_filter(f, filter):
            continue
        with open(dir_name+f) as f1:
            print(f1)
            for line in f1:
                try:
                    json_obj = json.loads(line)
                    for item in json_obj.get('data',{}).get("item",[]):
                        if item[0] in timestamp_dict:
                            continue
                        time_string = datetime.datetime.fromtimestamp(int(item[0]/1000), pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S GMT%z')
                        data = "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(int(item[0]), time_string, item[2], item[3], item[4], item[5], item[1]) # time,open,high,low,close,volume
                        output_list.append(data)     
                        timestamp_dict[item[0]] = 1                    
                except Exception as e:
                   print("line error")
    output_list = sorted(list(set(output_list)))
    
    #with open(output_dir+code+"_tmp", 'w') as f:
    #    for item in output_list:
    #        ts = int(item.split('\t')[1])
    #        tz = pytz.timezone('America/New_York')
    #        dt = pytz.datetime.datetime.fromtimestamp(ts, tz)
    #        dt = dt.strftime('%Y-%m-%d')
    #        f.write(item+'\n')
    
    last_dt = 0
    f_out = None
    for item in output_list:
        ts = int(item.split('\t')[0])/1000
        tz = pytz.timezone('America/New_York')
        dt = pytz.datetime.datetime.fromtimestamp(ts, tz)
        dt = dt.strftime('%Y-%m-%d')
        if dt != last_dt:
            if last_dt: 
                f_out.close()
            f_out = open(output_dir+dt, 'w')
            f_out.write(item+'\n')
        else:
            f_out.write(item+'\n')
        last_dt = dt
    f_out.close()

if __name__ == "__main__":
    code = sys.argv[1]
    dir_name = "/root/program_trading/data/xueqiu_1m_log/{}/".format(code)
    filter = None
    if(len(sys.argv) == 3):
        filter = sys.argv[2]
    output_dir = "/root/program_trading/data/xueqiu_1m_log_after/{}/".format(code)
    get_dir_result(dir_name, code, filter, output_dir)
