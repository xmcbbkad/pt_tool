class TradeStatisticsOption_1():
    def __init__(self,):
        self.buy_count = 0
        self.sell_count = 0

        self.long_count_ratio = 0.0
        self.short_count_ratio = 0.0
        self.long_net_profit_ratio = 0.0
        self.short_net_profit_ratio = 0.0

        self.buy_filled = 0
        self.sell_filled = 0
        self.buy_amount = 0.0
        self.sell_amount = 0.0
        self.fees = 0.0
        self.gross_profit = 0.0
        self.net_profit = 0.0

        self.long_filled = 0
        self.long_buy_amount = 0.0
        self.long_sell_amount = 0.0
        self.long_fees = 0.0
        self.long_gross_profit = 0.0
        self.long_net_profit = 0.0
        
        self.short_filled = 0
        self.short_buy_amount = 0.0
        self.short_sell_amount = 0.0
        self.short_fees = 0.0
        self.short_gross_profit = 0.0
        self.short_net_profit = 0.0
 
        self.count = 0 
        self.win_count = 0
        self.lose_count = 0
        self.win_amount = 0.0
        self.lose_amount = 0.0
        self.avg_win_amount = 0.0
        self.avg_lose_amount = 0.0
        self.win_ratio = 0.0
        self.profit_and_coss_ratio = 0.0

        self.long_count = 0
        self.long_win_count = 0
        self.long_lose_count = 0
        self.long_win_amount = 0.0
        self.long_lose_amount = 0.0
        self.long_avg_win_amount = 0.0
        self.long_avg_lose_amount = 0.0
        self.long_win_ratio = 0.0
        self.long_profit_and_coss_ratio = 0.0

        self.short_count = 0
        self.short_win_count = 0
        self.short_lose_count = 0
        self.short_win_amount = 0.0
        self.short_lose_amount = 0.0
        self.short_avg_win_amount = 0.0
        self.short_avg_lose_amount = 0.0
        self.short_win_ratio = 0.0
        self.short_profit_and_coss_ratio = 0.0


        self.finished_transactions = []
        self.unfinished_transactions = []
        
    def add_transaction(self, contract, action, filled, price):
        if action == "BUY":
            self.buy_filled += int(filled)
            self.buy_amount += int(filled) * float(price)
            self.buy_count += 1
            self.fees += 1.0
        elif action == "SELL":
            self.sell_filled += int(filled)
            self.sell_amount += int(filled) * float(price)
            self.sell_count += 1
            self.fees += 1.0
        

        this_transaction = {
            "contract": contract,
            "action": action,
            "filled": int(filled),
            "price": float(price),
            "fees": 1.0
        }
        #import pdb; pdb.set_trace()
        #fees = 0.0
        for i in range(len(self.unfinished_transactions)):
            fees = 0.0
            if self.unfinished_transactions[i].get("status", "") == "used":
                continue         
    
            if self.unfinished_transactions[i]["action"] == this_transaction["action"]:
                break


            if this_transaction["action"] == "BUY":
                direction = "short"
                sell_price = self.unfinished_transactions[i]["price"]
                buy_price = this_transaction["price"]
            elif this_transaction["action"] == "SELL":
                direction = "long"
                buy_price = self.unfinished_transactions[i]["price"]
                sell_price = this_transaction["price"]

            
            if self.unfinished_transactions[i]["filled"] <= this_transaction["filled"]:
                self.unfinished_transactions[i]["status"] = "used"
                filled = self.unfinished_transactions[i]["filled"]
            else: # self.unfinished_transactions[i]["filled"] > this_transaction["filled"]:
                filled = this_transaction["filled"]
                self.unfinished_transactions[i]["filled"] -= filled
            
            this_transaction["filled"] -= filled
            if self.unfinished_transactions[i]["fees"] >= 1.0:
                fees += 1.0
                self.unfinished_transactions[i]["fees"] -= 1.0
            
            if this_transaction["fees"] >= 1.0:
                fees += 1.0
                this_transaction["fees"] -= 1.0                

            self.finished_transactions.append(
                {
                    "contract": contract,
                    "direction": direction,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "filled": filled,
                    "fees": fees
                }
            )
            if this_transaction["filled"] <= 0:
                break
            

        if this_transaction["filled"]:
            self.unfinished_transactions.append(this_transaction)    
        #print(self.finished_transactions) 
 
    def cal_metrics(self):
        self.count = len(self.finished_transactions)
        for i in range(len(self.finished_transactions)):
            #print(self.finished_transactions[i])
            
            if self.finished_transactions[i]["direction"] == "long":
                self.long_count += 1
                self.long_filled += self.finished_transactions[i]["filled"]
                self.long_buy_amount += self.finished_transactions[i]["buy_price"] * self.finished_transactions[i]["filled"]
                self.long_sell_amount += self.finished_transactions[i]["sell_price"] * self.finished_transactions[i]["filled"]
                self.long_fees += self.finished_transactions[i]["fees"]
            elif self.finished_transactions[i]["direction"] == "short":
                self.short_count += 1
                self.short_filled += self.finished_transactions[i]["filled"]
                self.short_buy_amount += self.finished_transactions[i]["buy_price"] * self.finished_transactions[i]["filled"]
                self.short_sell_amount += self.finished_transactions[i]["sell_price"] * self.finished_transactions[i]["filled"]
                self.short_fees += self.finished_transactions[i]["fees"]

            if (self.finished_transactions[i]["sell_price"] - self.finished_transactions[i]["buy_price"]) * self.finished_transactions[i]["filled"] - self.finished_transactions[i]["fees"] >= 0:
                self.win_count += 1
                win_amount = (self.finished_transactions[i]["sell_price"] - self.finished_transactions[i]["buy_price"]) * self.finished_transactions[i]["filled"] - self.finished_transactions[i]["fees"]
                self.win_amount += win_amount
                
                if self.finished_transactions[i]["direction"] == "long":
                    self.long_win_count += 1
                    self.long_win_amount += win_amount
                elif self.finished_transactions[i]["direction"] == "short":
                    self.short_win_count += 1
                    self.short_win_amount += win_amount                
                
                #print("win_amount={}".format(win_amount))
            else:
                self.lose_count += 1
                lose_amount = (self.finished_transactions[i]["buy_price"] - self.finished_transactions[i]["sell_price"]) * self.finished_transactions[i]["filled"] + self.finished_transactions[i]["fees"]
                self.lose_amount += lose_amount

                if self.finished_transactions[i]["direction"] == "long":
                    self.long_lose_count += 1
                    self.long_lose_amount += lose_amount                
                elif self.finished_transactions[i]["direction"] == "short":
                    self.short_lose_count += 1
                    self.short_lose_amount += lose_amount                
 
                #print("lose_amount={}".format(lose_amount))
        
        self.win_ratio = self.win_count/(self.win_count+self.lose_count + 1e-5)
        self.avg_win_amount = self.win_amount/(self.win_count + 1e-5)
        self.avg_lose_amount = self.lose_amount/(self.lose_count + 1e-5)
        self.profit_and_coss_ratio = self.avg_win_amount/(self.avg_lose_amount + 1e-5)

        self.long_win_ratio = self.long_win_count/(self.long_win_count+self.long_lose_count + 1e-5)
        self.long_avg_win_amount = self.long_win_amount/(self.long_win_count + 1e-5)
        self.long_avg_lose_amount = self.long_lose_amount/(self.long_lose_count + 1e-5)
        self.long_profit_and_coss_ratio = self.long_avg_win_amount/(self.long_avg_lose_amount + 1e-5)

        self.short_win_ratio = self.short_win_count/(self.short_win_count+self.short_lose_count + 1e-5)
        self.short_avg_win_amount = self.short_win_amount/(self.short_win_count + 1e-5)
        self.short_avg_lose_amount = self.short_lose_amount/(self.short_lose_count + 1e-5)
        self.short_profit_and_coss_ratio = self.short_avg_win_amount/(self.short_avg_lose_amount + 1e-5)

 
        self.gross_profit = self.sell_amount - self.buy_amount
        self.net_profit = self.gross_profit - self.fees
        self.fees_net_profit_ratio = self.fees / (self.net_profit + self.fees)      
 
        self.long_gross_profit = self.long_sell_amount - self.long_buy_amount
        self.long_net_profit = self.long_gross_profit - self.long_fees

        self.short_gross_profit = self.short_sell_amount - self.short_buy_amount
        self.short_net_profit = self.short_gross_profit - self.short_fees
 
        self.long_count_ratio = self.long_count/(self.count + 1e-5)
        self.short_count_ratio = self.short_count/(self.count + 1e-5)

        self.long_net_profit_ratio = self.long_net_profit/(self.net_profit + 1e-5)
        self.short_net_profit_ratio = self.short_net_profit/(self.net_profit + 1e-5)

    #def add_item(self, item):
    #    self.buy_count += item.buy_count
    #    self.sell_count += item.sell_count
    #    self.buy_filled += item.buy_filled
    #    self.sell_filled += item.sell_filled
    #    self.buy_amount += item.buy_amount
    #    self.sell_amount += item.sell_amount
    #    self.gross_profit += item.gross_profit
    #    self.net_profit += item.net_profit
    #    self.fees += item.fees

    #    self.win_count += item.win_count
    #    self.lose_count += item.lose_count
    #    self.win_amount += item.win_amount
    #    self.lose_amount += item.lose_amount
    #    
    #    self.win_ratio = self.win_count/(self.win_count+self.lose_count + 1e-5)
    #    self.avg_win_amount = self.win_amount/(self.win_count + 1e-5)
    #    self.avg_lose_amount = self.lose_amount/(self.lose_count + 1e-5)
    #    self.profit_and_coss_ratio = self.avg_win_amount/(self.avg_lose_amount + 1e-5)
 
    def print(self):
        print("  all:")
        print("    buy_count={}, sell_count={}, buy_filled={}, sell_filled={}, buy_amount={:.2f}, sell_amount={:.2f}, gross_profit={:.2f}, fees={}, fees_net_profit_ratio={:.2%}, net_profit={:.2f}".format(self.buy_count, self.sell_count, self.buy_filled, self.sell_filled, self.buy_amount, self.sell_amount, self.gross_profit, self.fees, self.fees_net_profit_ratio, self.net_profit))
        print("    count={}, win_count={}, lose_count={}, win_amount={:.2f}, lose_amount={:.2f}, avg_win_amount={:.2f}, avg_lose_amount={:.2f}, win_ratio={:.2%}, profit_and_coss_ratio={:.2f}".format(self.count, self.win_count, self.lose_count, self.win_amount, self.lose_amount, self.avg_win_amount, self.avg_lose_amount, self.win_ratio, self.profit_and_coss_ratio))
        print("    count={}, long_count={}, short_count={}, long_count_ratio={:.2%}, short_count_ratio={:.2%}, long_net_profit_ratio={:.2%}, short_net_profit_ratio={:.2%}".format(self.count, self.long_count, self.short_count, self.long_count_ratio, self.short_count_ratio, self.long_net_profit_ratio, self.short_net_profit_ratio))

        print("  long:") 
        print("    filled={}, buy_amount={:.2f}, sell_amount={:.2f}, gross_profit={:.2f}, fees={}, net_profit={:.2f}".format(self.long_filled, self.long_buy_amount, self.long_sell_amount, self.long_gross_profit, self.long_fees, self.long_net_profit))
        print("    count={}, win_count={}, lose_count={}, win_amount={:.2f}, lose_amount={:.2f}, avg_win_amount={:.2f}, avg_lose_amount={:.2f}, win_ratio={:.2%}, profit_and_coss_ratio={:.2f}".format(self.long_count, self.long_win_count, self.long_lose_count, self.long_win_amount, self.long_lose_amount, self.long_avg_win_amount, self.long_avg_lose_amount, self.long_win_ratio, self.long_profit_and_coss_ratio))

        print("  short:") 
        print("    filled={}, buy_amount={:.2f}, sell_amount={:.2f}, gross_profit={:.2f}, fees={}, net_profit={:.2f}".format(self.short_filled, self.short_buy_amount, self.short_sell_amount, self.short_gross_profit, self.short_fees, self.short_net_profit))
        print("    count={}, win_count={}, lose_count={}, win_amount={:.2f}, lose_amount={:.2f}, avg_win_amount={:.2f}, avg_lose_amount={:.2f}, win_ratio={:.2%}, profit_and_coss_ratio={:.2f}".format(self.short_count, self.short_win_count, self.short_lose_count, self.short_win_amount, self.short_lose_amount, self.short_avg_win_amount, self.short_avg_lose_amount, self.short_win_ratio, self.short_profit_and_coss_ratio))


class TradeStatisticsOption_2():
    def __init__(self, name):
        self.name = name
        self.reset()
 
    def reset(self):
        self.win = 0
        self.lose = 0
        self.win_ratio = 0
        self.win_percent = 0
        self.lose_percent = 0
        self.net_percent = 0
    
    def add_item(self, item):
        if item.get("sell") > item.get("buy"):
            self.win += 1
            if item.get("direction", "") == "long":
                self.win_percent += (item.get("sell") - item.get("buy"))/item.get("buy")
            elif item.get("direction", "") == "short":
                self.win_percent += (item.get("sell") - item.get("buy"))/item.get("sell")
        else:
            self.lose += 1
            if item.get("direction", "") == "long":
                self.lose_percent += (item.get("buy") - item.get("sell"))/item.get("buy")
            elif item.get("direction", "") == "short":
                self.lose_percent += (item.get("buy") - item.get("sell"))/item.get("sell")
        
        self.win_ratio = self.win/(self.win+self.lose+0.1)
        self.net_percent = self.win_percent - self.lose_percent

    def print(self):
        print("date={}, win={}, lose={}, win_ratio={:.1%}, win_percent={:.1%}, lose_percent={:.1%}, net_percent={:.1%}".format(self.name, self.win, self.lose, self.win_ratio, self.win_percent, self.lose_percent, self.net_percent))


class TradeStaticsWithYearMonth():
    def __init__(self):
        self.month_statistics = []
        self.year_statistics = []   
 
    def add_item(self, date, item):
        year = date[:4]
        month = date[:7]
        
        if self.year_statistics and year == self.year_statistics[-1].name:
            self.year_statistics[-1].add_item(item)
        else:
            self.year_statistics.append(TradeStatisticsOption_2(year))
            self.year_statistics[-1].add_item(item)
        
        if self.month_statistics and month == self.month_statistics[-1].name:
            self.month_statistics[-1].add_item(item)
        else:
            self.month_statistics.append(TradeStatisticsOption_2(month))
            self.month_statistics[-1].add_item(item)

    def print(self):
        for item in self.month_statistics: 
            item.print()
        for item in self.year_statistics:
            item.print()    


