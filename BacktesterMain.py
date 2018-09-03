""" python 3.6, anaconda 5.2
    Backtester Main Engine source code v0.1.
    20180901, gunheecs.lee@samsung.com
"""
import BacktestStrategies
import StockExchangeSimulator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def ReceiveStartingCondition(start_cond_dict):
    start_cond_dict['initial_capital_usd']=float(input("Initial Capital (USD): "))
    start_cond_dict['sell_threshold_percent']=float(input(
        "Sell Signal Threshold (Percent, compared to recent highest price): "))
    start_cond_dict['buy_momentum_days']=int(input(
        "Buy Signal Momentum Period(check this day before) as int: "))
    return start_cond_dict

def RunBacktest(start_cond_dict, strat, df, stock_exchange):
    inventory_dict={'cash_usd':start_cond_dict['initial_capital_usd'], 'stock_amount':0}
    strat(start_cond_dict, df, stock_exchange, inventory_dict)    
    return

if __name__=='__main__':
    start_cond_dict={'initial_capital_usd':1000, 'sell_threshold_percent':75.0, 
            'buy_momentum_days':270}
    data_csv=pd.read_csv('QQQ.csv')
    #print(data_csv)  # This is a pandas dataframe object.
    stock_exchange=StockExchangeSimulator.StockExchange(data_csv)

    start_cond_dict=ReceiveStartingCondition(start_cond_dict)
    RunBacktest(start_cond_dict, BacktestStrategies.BacktestStrategy1, data_csv, stock_exchange)
    RunBacktest(start_cond_dict, BacktestStrategies.BacktestStrategy2, data_csv, stock_exchange)

    exit(0)