import csv

# 指定CSV文件的路径

class StatisticItem():
    def __init__(self,):
        self.buy_count = 0
        self.sell_count = 0
        self.buy_filled = 0
        self.sell_filled = 0
        self.buy_amount = 0
        self.sell_amount = 0
        self.gross_profit = 0
        self.net_profit = 0
        self.fees = 0
   
    def add(self, item):
        self.buy_count += item.buy_count
        self.sell_count += item.sell_count
        self.buy_filled += item.buy_filled
        self.sell_filled += item.sell_filled
        self.buy_amount += item.buy_amount
        self.sell_amount += item.sell_amount
        self.gross_profit += item.gross_profit
        self.net_profit += item.net_profit
        self.fees += item.fees
 
    def print(self):
        print("buy_count={} sell_count={} buy_filled={} sell_filled={} buy_amount={} sell_amount={} gross_profit={:.2f} fees={} net_profit={:.2f}".format(self.buy_count, self.sell_count, self.buy_filled, self.sell_filled, self.buy_amount, self.sell_amount, self.gross_profit, self.fees, self.net_profit))   

def cal_benefit(file_path):
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
                all_result[date] = StatisticItem()
                
            if row[2] == "BUY":
                all_result[date].buy_filled += int(row[3])
                all_result[date].buy_amount += int(row[3])*float(row[4])
                all_result[date].buy_count += 1
                all_result[date].fees += 1.0
            elif row[2] == "SELL":
                all_result[date].sell_filled += int(row[3])
                all_result[date].sell_amount += int(row[3])*float(row[4])
                all_result[date].sell_count += 1
                all_result[date].fees += 1.0
            
            all_result[date].gross_profit = all_result[date].sell_amount - all_result[date].buy_amount
            all_result[date].net_profit = all_result[date].gross_profit - all_result[date].fees
    
        
        all_statistic = StatisticItem()
        for item in all_result:
            print(item)
            all_result[item].print()
            all_statistic.add(all_result[item])

        print("all:")
        all_statistic.print()    

if __name__ == "__main__":
    file_path = '/root/program_trading/data/tiger_trade_log/2024-09.csv'
    cal_benefit(file_path)
