# python 3.6, anaconda 5.2
# Backtester Main Engine source code.
# 20180901, gunheecs.lee@samsung.com
import BacktestStrategies
import enaml
from enaml.qt.qt_application import QtApplication
from StartingCondition import StartingCondition

if __name__=='__main__':
    #inventory_dict={'cash_usd':0, 'stock_price_usd':0, 'stock_amount':0}
    with enaml.imports():
        from start_window import StartWindow

    arg_obj = StartingCondition(initial_capital_usd=1000, sell_threshold_percent=75.0,
            buy_momentum_days=270)

    app = QtApplication()

    view = StartWindow(StartingCondition=arg_obj)
    view.show()

    app.start()
    exit(0)