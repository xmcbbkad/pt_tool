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
        print(f)
        with open(dir_name+f) as f1:
            for line in f1:
                try:
                    json_obj = json.loads(line)
                except:
                    print(dir_name+f)
                    continue
                try:
                    dt = json_obj['data'][0]
                except:
                    print(json_obj)
                    continue
                if dt['timestamp'] in timestamp_dict:
                        continue
                data = "{}\t{}\t{}\t{}\t{}\t{}".format(int(dt['timestamp']/1000), 'null', 'null', 'null', dt['current'], dt['volume']) # time,open,high,low,close,volume
                if dt['volume']:
                    output_list.append(data)     
                timestamp_dict[dt['timestamp']] = 1                    

    output_list = sorted(list(set(output_list)))
    
    with open(output_dir+code+"_tmp", 'w') as f:
        for item in output_list:
            try:
                ts = int(item.split('\t')[0])
                tz = pytz.timezone('America/New_York')
                dt = pytz.datetime.datetime.fromtimestamp(ts, tz)
                dt = dt.strftime('%Y-%m-%d')
                f.write(dt+'\t'+item+'\n')
            except:
                print(item)
 
    last_dt = 0
    last_ts = 0
    f_out = None
    for item in output_list:
        ts = int(item.split('\t')[0])
        tz = pytz.timezone('America/New_York')
        dt = pytz.datetime.datetime.fromtimestamp(ts, tz)
        dt = dt.strftime('%Y-%m-%d')
        if dt != last_dt:
            if last_dt: 
                f_out.close()
            f_out = open(output_dir+dt+'_'+code, 'w')
            f_out.write(item+'\n')
        else:
            if last_ts !=0 and ts-last_ts <10:
                #print("<10s,ts:{}___range:{}".format(ts, ts-last_ts))
                continue
            #if last_ts != 0 and ts-last_ts >100:
            #    print(">100s,ts:{}___range:{}".format(ts, ts-last_ts))
            f_out.write(item+'\n')
        last_dt = dt
        last_ts = ts
    f_out.close()

if __name__ == "__main__":
    code = sys.argv[1]
    dir_name = "/root/program_trading/xueqiu_realtime_log/{}/".format(code)
    filter = None
    if(len(sys.argv) == 3):
        filter = sys.argv[2]
    output_dir = "/root/program_trading/xueqiu_realtime_log_after/{}/".format(code)
    
    get_dir_result(dir_name, code, filter, output_dir)
