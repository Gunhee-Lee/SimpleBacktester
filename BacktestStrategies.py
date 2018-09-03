import StockExchangeSimulator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def BacktestStrategy1(start_cond_dict, df, stock_exchange, invt_dict):
    """ Baseline strategy, which buys from the start day,
    and do nothing until the end day. (Ultra long investment) 
    """
    total_days=df.shape[0]
    today_invt_dict=invt_dict
    invt_daily_list=[]      # invt after today's transaction
    net_wealth_list=[]

    for i in range(total_days):
        if i==0:
            today_invt_dict=stock_exchange.FullBuyStocks(today_invt_dict, i)
        elif i==total_days-1:   # last day
            today_invt_dict=stock_exchange.FullSellStocks(today_invt_dict, i)
        invt_daily_list.append(today_invt_dict)
        net_wealth_list.append(stock_exchange.EstimateNetWealth(today_invt_dict, i))
    
    PrintResult("Baseline Strategy", net_wealth_list)
    plt.plot(net_wealth_list)
    plt.title("Baseline (1st day buy->hold->last day sell) Strategy")
    plt.ylabel('Net Worth in USD')  # Cash + Stock worth
    plt.show()
    return

def BacktestStrategy2(start_cond_dict, df, stock_exchange, invt_dict):
    """ TQQQ desired strategy (main target of this backtest)
    """
    total_days=df.shape[0]
    today_invt_dict=invt_dict
    invt_daily_list=[]      # invt after today's transaction
    net_wealth_list=[]
    recent_max=0            # recent max = 전고점 가격
    for i in range(total_days):
        if i==0:    # 첫날은 일단 풀매수
            recent_max=stock_exchange.GetDayHighestPrice(i)
            today_invt_dict=stock_exchange.FullBuyStocks(today_invt_dict, i)
        else:   # 다른날은 전부 전략대로 수행
            recent_max=max(recent_max, stock_exchange.GetDayHighestPrice(i-1))  # 전고점 갱신 확인
            # 만약 어제 종가가 전고점*threshold 미만이라면: 풀매도 
            if (stock_exchange.GetDayClosePrice(i-1) < 
                    (start_cond_dict['sell_threshold_percent']/100)*recent_max):
                today_invt_dict=stock_exchange.FullSellStocks(today_invt_dict, i)
            # 매도조건을 만족 안 시킨 상황에서 n개월 모멘텀이 (+)면: 풀매수 -- n개월이 안지났으면 스킵
            elif (i > start_cond_dict['buy_momentum_days'] and 
                    stock_exchange.GetDayHighestPrice(i-start_cond_dict['buy_momentum_days']) <
                    stock_exchange.GetDayOpenPrice(i)):
                today_invt_dict=stock_exchange.FullBuyStocks(today_invt_dict, i)
            # 나머지 상황에선 포지션 홀드
            else:
                pass
        invt_daily_list.append(today_invt_dict)
        #print(today_invt_dict)     # for debug :)
        net_wealth_list.append(stock_exchange.EstimateNetWealth(today_invt_dict, i))
    
    PrintResult("Experimental Strategy", net_wealth_list)
    plt.plot(net_wealth_list)
    plt.title("Experimental Strategy")
    plt.ylabel('Net Worth in USD')  # Cash + Stock worth
    plt.show()

def PrintResult(title, net_wealth_list):
    print('========== {} =========='.format(title))
    print('First day net worth={} USD'.format(net_wealth_list[0]))
    print('Last day net worth={} USD'.format(net_wealth_list[-1]))
    print('Nominal profit margin (%)={} %'.format((net_wealth_list[-1]/net_wealth_list[0]-1)*100))
    return