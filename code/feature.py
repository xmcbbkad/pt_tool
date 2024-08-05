import pandas as pd


class FeatureBuilder():
    def __init__(self, ):
        pass
    
    def add_boll(self, df):
        window = 20
        df['boll_mean'] = df['close'].rolling(window=window).mean()
        df['boll_std'] = df['close'].rolling(window=window).std()
        df['boll_upper'] = df['boll_mean'] + 2 * df['boll_std']
        df['boll_lower'] = df['boll_mean'] - 2 * df['boll_std']
        
        return df

    def add_continue_down(self, df):
        df["continue_10_down"] = False
        for i in range(len(df)):
            span = 10
            if i-span <= 0:
                continue
            
            continue_fall = True
            for j in range(i-1, i-span, -1):
                if df.iloc[j]["close"] > df.iloc[j+1]["close"]:
                    continue
                else:
                    continue_fall = False
                    break
            if continue_fall:
                df.loc[i, "continue_10_down"] = True 
        
        return df


    def add_fluctuation(self, df):
        df["fluctuation"] = "" 
        last_index = 0
        for i in range(len(df)):
        #for i in range(5):
            #print("-----")
            #print(df.iloc[i]["close"])
            for j in range(i-1, last_index-1, -1):
                if df.iloc[i]["high"] - df.iloc[j]["low"] > 1.0:
                    print("buy")
                    print(df.iloc[j]["time_str"])
                    print(df.iloc[j]["low"])
                    print("sell")
                    print(df.iloc[i]["time_str"])
                    print(df.iloc[i]["high"])
                    print("----")
                    #df.iloc[j]["fluctuation"] = "buy"
                    #df.iloc[i]["fluctuation"] = "sell"
                    df.loc[j, "fluctuation"] = "left_buy"
                    df.loc[i, "fluctuation"] = "right_sell"
                    last_index = i+1
                    break
                elif df.iloc[j]["high"] - df.iloc[i]["low"] > 1.0:
                    print("sell")
                    print(df.iloc[j]["time_str"])
                    print(df.iloc[j]["high"])
                    print("buy")
                    print(df.iloc[i]["time_str"])
                    print(df.iloc[i]["low"])
                    print("----")
                    #df.iloc[j]["fluctuation"] = "sell"
                    #df.iloc[i]["fluctuation"] = "buy"
                    df.loc[j, "fluctuation"] = "left_sell"
                    df.loc[i, "fluctuation"] = "right_buy"
                    last_index = i+1
                    break
        return df

if __name__ == "__main__":
    code = "TSLA"
    date = "2024-03-21"
    data = pd.read_csv('/root/program_trading/data/tiger_1m_log_after/{}/{}/{}.csv'.format(code, date[:7], date))
    data = FeatureBuilder().add_fluctuation(data)
    print(data)
