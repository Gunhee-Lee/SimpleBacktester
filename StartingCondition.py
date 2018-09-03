# StartingCondition.py
from atom.api import Atom, Unicode, Range, FloatRange, Bool, Value, Int, Tuple, Typed, observe

class StartingCondition(Atom):
    initial_capital_usd = Range(low=0)
    sell_threshold_percent = FloatRange(0.0, 100.0, 75.0)
    buy_momentum_days = Range(low=1)