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
        date = row[4].split()[0]
        if date not in all_result:
            all_result[date] = {
                "long_position" : 0,
                "long_position_price" : 0,
                "short_position" : 0,
                "short_position_price" : 0,
                "net" : 0
            }
            
        if row[0] == "BUY":
            all_result[date]["long_position"] += int(row[3])
            all_result[date]["long_position_price"] += float(row[1])*int(row[3])
        elif row[0] == "SELL":
            all_result[date]["short_position"] += int(row[3])
            all_result[date]["short_position_price"] += float(row[1])*int(row[3])
        
        all_result[date]["net"] = all_result[date]["short_position_price"] - all_result[date]["long_position_price"]

    
    net = 0
    for item in all_result:
        print(item)
        print(all_result[item])
        net += all_result[item]["net"]
    print(net)
