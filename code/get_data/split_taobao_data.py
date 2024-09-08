import pandas as pd
import os

# 读取CSV文件
#symbol = "AAPL"
#symbol = "AMD"
#symbol = "AMZN"
#symbol = "GOOG"
#symbol = "MSFT"
#symbol = "NVDA"
symbol = "TSLA"
base_dir = "/root/program_trading/data/taobao/"
df = pd.read_csv('{}/{}.csv'.format(base_dir, symbol))
df = df.iloc[::-1]


# 将日期列转换为datetime格式
df['date'] = pd.to_datetime(df['date'])

# 按日期进行分组
groups = df.groupby(df['date'].dt.date)

# 遍历每个组
for date, group in groups:
    # 创建文件夹（按年月命名）
    directory = os.path.join(base_dir, symbol, date.strftime('%Y'), date.strftime('%Y-%m'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # 创建文件路径
    filename = os.path.join(directory, f"{date}.csv")
    
    # 将分组数据保存为CSV文件
    group.to_csv(filename, index=False)

    print(f"Saved {filename}")

