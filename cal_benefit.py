from utils.cal_metrics import TradeStatisticsOption_1
import csv

# 指定CSV文件的路径

def cal_benefit(file_path):
    # 使用with语句打开文件，确保文件最后会被正确关闭
    with open(file_path, mode='r', encoding='utf-8') as file:
        # 创建一个csv reader对象
        reader = csv.reader(file)
    
        result_with_date = {}
        all_result = TradeStatisticsOption_1() 
        
        # 遍历CSV文件中的每一行
        for row in reader:
            print(row)
            if row[0] == "trade_date":
                continue
            if int(row[3]) == 0:
                continue

            date = row[0].split()[0]
            if date not in result_with_date:
                result_with_date[date] = TradeStatisticsOption_1()
            
            result_with_date[date].add_transaction(contract=row[1], action=row[2], filled=row[3], price=row[4])
            all_result.add_transaction(contract=row[1], action=row[2], filled=row[3], price=row[4])
 
    
        
        #all_statistic = TradeStatisticsOption_1()
        for item in result_with_date:
            print(item)
            result_with_date[item].cal_metrics()
            result_with_date[item].print()
            #all_statistic.add_item(result_with_date[item])

        print("all:")
        #all_statistic.print()    
        all_result.cal_metrics()
        all_result.print()    

if __name__ == "__main__":
    #file_path = '/root/program_trading/data/tiger_trade_log/2024-09.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024-09-10.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_0902_0906.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_0909_0913.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024-09_16-20.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024-09_23-27.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_0930_1004.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024-10.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1007_1011.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1014_1018.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1021_1025.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024-10_fix.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1028_1101.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024-11.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1104_1108.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1111_1115.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1118_1122.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1125_1129.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1209_1213.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1216_1220.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1223_1227.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024-12.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2024_1230_0103.csv'
    file_path = '/root/program_trading/data/tiger_trade_log/2025-01.csv'
    #file_path = '/root/program_trading/data/tiger_trade_log/2025_0106_0110.csv'
    file_path = '/root/program_trading/data/tiger_trade_log/2025_0113_0117.csv'
    cal_benefit(file_path)
