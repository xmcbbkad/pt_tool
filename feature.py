import pandas as pd


class FeatureBuilder():
    def __init__(self, ):
        pass
   
    def add_boll(self, df, window=20):
        df['boll_mean'] = df['close'].rolling(window=window, min_periods=1).mean().round(2)
        boll_std = df['close'].rolling(window=window, min_periods=1).std().round(2)
        df['boll_upper'] = df['boll_mean'] + 2 * boll_std
        df['boll_lower'] = df['boll_mean'] - 2 * boll_std
        
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

    def add_continue_down_invert(self, df):
        df["continue_10_down_invert"] = False
        for i in range(len(df)):
            if df.iloc[i]["continue_10_down"] == False:
                continue
            if i+1<len(df) and df.iloc[i+1]["close"]>df.iloc[i+1]["open"] and df.iloc[i+1]["close"] > df.iloc[i]["high"]:
                df.loc[i+1, "continue_10_down_invert"] = True
            elif i+2<len(df) and df.iloc[i+1]["close"]>df.iloc[i+1]["open"] and df.iloc[i+2]["close"]>df.iloc[i+2]["open"] and df.iloc[i+2]["close"] > df.iloc[i]["high"]:
                df.loc[i+2, "continue_10_down_invert"] = True
            elif i+3 <len(df) and df.iloc[i+1]["close"]>df.iloc[i+1]["open"] and df.iloc[i+2]["close"]>df.iloc[i+2]["open"] and df.iloc[i+3]["close"]>df.iloc[i+3]["open"] and df.iloc[i+3]["close"] > df.iloc[i]["high"]:
                df.loc[i+3, "continue_10_down_invert"] = True
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
                    print(df.iloc[j]["date"])
                    print(df.iloc[j]["low"])
                    print("sell")
                    print(df.iloc[i]["date"])
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
                    print(df.iloc[j]["date"])
                    print(df.iloc[j]["high"])
                    print("buy")
                    print(df.iloc[i]["date"])
                    print(df.iloc[i]["low"])
                    print("----")
                    #df.iloc[j]["fluctuation"] = "sell"
                    #df.iloc[i]["fluctuation"] = "buy"
                    df.loc[j, "fluctuation"] = "left_sell"
                    df.loc[i, "fluctuation"] = "right_buy"
                    last_index = i+1
                    break
        return df

    def add_true_range(self, df):
        df["TR"] = 0.0
        df["TR_percent"] = 0.0
        for i in range(1, len(df)):
            TR1 = df.iloc[i]["high"] - df.iloc[i]["low"]
            TR2 = abs(df.iloc[i]["high"] - df.iloc[i-1]["close"])
            TR3 = abs(df.iloc[i]["low"] - df.iloc[i-1]["close"])
            df.loc[i, "TR"] = max([TR1, TR2, TR3])
            
            TR1_percent = (df.iloc[i]["high"] - df.iloc[i]["low"])/df.iloc[i]["low"]
            TR2_percent = abs(df.iloc[i]["high"] - df.iloc[i-1]["close"])/min(df.iloc[i]["high"], df.iloc[i-1]["close"])
            TR3_percent = abs(df.iloc[i]["low"] - df.iloc[i-1]["close"])/min(df.iloc[i]["low"], df.iloc[i-1]["close"])
            df.loc[i, "TR_percent"] = max([TR1_percent, TR2_percent, TR3_percent])

        df["TR"] = df["TR"].round(2)
        df["TR_percent"] = df["TR_percent"]*100
        df["TR_percent"] = df["TR_percent"].round(2)
        return df

    def add_rsi(self, df, window=6):
        delta = df['close'].diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()
        avg_loss = avg_loss.replace(0, 1e-10)

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        df['RSI_{}'.format(window)] = rsi.round(2)
        return df 

if __name__ == "__main__":
    code = "TSLA"
    date = "2024-08-21"
    data = pd.read_csv('/root/program_trading/data/tiger_1m_log_after/{}/{}/{}/{}.csv'.format(code, date[:4], date[:7], date))
    data = FeatureBuilder().add_boll(data)
    data = FeatureBuilder().add_fluctuation(data)
    data = FeatureBuilder().add_true_range(data)
    data = FeatureBuilder().add_rsi(data, window=6)
    data = FeatureBuilder().add_rsi(data, window=12)
    data = FeatureBuilder().add_rsi(data, window=24)
    print(data[:50])
