"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.portfolio.py
Created on 2017-02-14T16:32:00Z
@author:Joshua Hu
"""
import pandas as pd

class Portfolio(object):
    """docstring for Portfolio."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, positions = pd.DataFrame(index = 'ID_position',
                                        columns = ['instrument','ticker',
                                        'trade_type','amount_units',
                                        'amount_wealth',
                                        'price_per_unit_entry',
                                        'price_per_unit_today',
                                        'time_of_trade', 'date_entry',
                                        'date_expiry', 'age', 'PL_today',
                                        'PL_total'])):

        self._positions = Positions

        self._strategy_PL = 0.0
        self._account_PL = {'accountID': 0.0} #OR pd.DataFrame()

        self._strategy_NAV = 0.0
        self._account_NAV = {'accountID': 0.0} #OR pd.DataFrame()

    """
    CLASS PROPERTIES
    """
    def positions():
        doc = "The positions property."
        def fget(self):
            return self._positions
        def fset(self, value):
            self._positions = value
        def fdel(self):
            del self._positions
        return locals()
    positions = property(**positions())

    def strategy_PL():
        doc = "The strategy_PL property."
        def fget(self):
            return self._strategy_PL
        def fset(self, value):
            self._strategy_PL = value
        def fdel(self):
            del self._strategy_PL
        return locals()
    strategy_PL = property(**strategy_PL())

    def account_PL():
        doc = "The account_PL property."
        def fget(self):
            return self._account_PL
        def fset(self, value):
            self._account_PL = value
        def fdel(self):
            del self._account_PL
        return locals()
    account_PL = property(**account_PL())

    def strategy_NAV():
        doc = "The strategy_NAV property."
        def fget(self):
            return self._strategy_NAV
        def fset(self, value):
            self._strategy_NAV = value
        def fdel(self):
            del self._strategy_NAV
        return locals()
    strategy_NAV = property(**strategy_NAV())

    def account_NAV():
        doc = "The account_NAV property."
        def fget(self):
            return self._account_NAV
        def fset(self, value):
            self._account_NAV = value
        def fdel(self):
            del self._account_NAV
        return locals()
    account_NAV = property(**account_NAV())

    """
    CLASS PUBLIC METHODS
    """
    def updatePositions(self, positions):
        pass

    def checkPositions(self, tickers = [''], all = False):
        return pd.DataFrame()

    def updateStrategyPL(self):
        pass

    def updateAccountPL(self, accounts = [''], all = False):
        return pd.DataFrame()

    def updateStrategyNAV(self):
        pass

    def updateAccountNAV(self, accounts = [''], all = False):
        return pd.DataFrame()
