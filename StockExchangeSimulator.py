""" This module simulate buy / sell behavior of Stock Exchange (ex: NASDAQ).
    Later, the price information should be located here.
    Assumption: Buy/Sell at open price.
"""
class StockExchange:
    def __init__(self, df):
        self.df_ = df

    def FullBuyStocks(self, invt, day_number):
        today_stock_price=self.df_.iloc[day_number,1]   # 'Open' column.
        new_invt=invt
        if invt['cash_usd'] >= today_stock_price:
            bought_stock_amount,remaining_cash_usd=divmod(invt['cash_usd'], today_stock_price)
            new_invt['cash_usd']=remaining_cash_usd
            new_invt['stock_amount']=invt['stock_amount']+bought_stock_amount
        return new_invt

    def FullSellStocks(self, invt, day_number):
        today_stock_price=self.df_.iloc[day_number,1]   # 'Open' column.
        new_invt=invt
        if invt['stock_amount'] > 0:
            stock_worth_usd=invt['stock_amount']*today_stock_price
            new_invt['cash_usd']=invt['cash_usd']+stock_worth_usd
            new_invt['stock_amount']=0
        return new_invt

    def EstimateNetWealth(self, invt, day_number):
        today_stock_price=self.df_.iloc[day_number,1]   # 'Open' column.
        return invt['cash_usd']+(invt['stock_amount']*today_stock_price)

    def GetDayOpenPrice(self, day_number):
        return self.df_.iloc[day_number,1]  # 'Open'

    def GetDayClosePrice(self, day_number):
        return self.df_.iloc[day_number,4]  # 'Close'

    def GetDayHighestPrice(self, day_number):
        return self.df_.iloc[day_number,2]  # 'High'