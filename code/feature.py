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
