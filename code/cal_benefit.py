import csv

# 指定CSV文件的路径
file_path = '/root/program_trading/data/tiger_trade_log/2024-09.csv'

# 使用with语句打开文件，确保文件最后会被正确关闭
with open(file_path, mode='r', encoding='utf-8') as file:
    # 创建一个csv reader对象
    reader = csv.reader(file)

    all_result = {}

    
    # 遍历CSV文件中的每一行
    for row in reader:
        print(row)
        date = row[0].split()[0]
        if date not in all_result:
            all_result[date] = {
                "buy_count" : 0,
                "sell_count": 0,
                "buy_filled" : 0,
                "sell_filled" : 0,
                "buy_amount" : 0,
                "sell_amount" : 0,
                "net" : 0
            }
            
        if row[2] == "BUY":
            all_result[date]["buy_filled"] += int(row[3])
            all_result[date]["buy_amount"] += int(row[3])*float(row[4])
            all_result[date]["buy_count"] += 1
        elif row[2] == "SELL":
            all_result[date]["sell_filled"] += int(row[3])
            all_result[date]["sell_amount"] += int(row[3])*float(row[4])
            all_result[date]["sell_count"] += 1
        
        all_result[date]["net"] = all_result[date]["sell_amount"] - all_result[date]["buy_amount"]

    
    net = 0
    for item in all_result:
        print(item)
        print(all_result[item])
        net += all_result[item]["net"]
    print("cumulative net:{}".format(net))
