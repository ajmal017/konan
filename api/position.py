# -*- coding: utf-8 -*-
"""
api.position.py
Created on Mon Feb 13 18:16:00 2017
@author: Joshua Hu
"""
from __future__ import print_function
import datetime as dt

import broker as br

class Position(object):
    """docstring for Position."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, ID = '', instrument = '', ticker = '', trade_type = '',
                    amount_units = 0, amount_wealth = 0.0,
                    time_of_trade = dt.datetime.today(),
                    date_expiry = dt.date.today()
                    ):

        self._ID = ID

        self._instrument = instrument
        self._ticker = ticker
        self._trade_type = trade_type
        self._amount_units = amount_units
        self._amount_wealth = amount_wealth

        self._price_per_unit_entry = 0.0 # get from IB
        self._price_per_unit_today = 0.0 # get from IB

        self._time_of_trade = time_of_trade
        self._date_entry = self.time_of_trade.date()
        self._date_expiry = date_expiry
        self._age = dt.date.today() - self.date_entry

        self._PL_today = 0.0
        self._PL_total = 0.0

    """
    CLASS PROPERTIES
    """
    def ID():
        doc = "The ID property."
        def fget(self):
            return self._ID
        def fset(self, value):
            self._ID = value
        def fdel(self):
            del self._ID
        return locals()
    ID = property(**ID())

    def instrument():
        doc = "The instrument property."
        def fget(self):
            return self._instrument
        def fset(self, value):
            if value not in ('STOCK','FUTURE','OPTION'):
                raise ValueError("instrument must be 'STOCK','FUTURE', or \
                                    'OPTION'")
            self._instrument = value
        def fdel(self):
            del self._instrument
        return locals()
    instrument = property(**instrument())

    def ticker():
        doc = "The ticker property."
        def fget(self):
            return self._ticker
        def fset(self, value):
            if type(value) != str:
                raise TypeError("Ticker must be of type string")
            self._ticker = value
        def fdel(self):
            del self._ticker
        return locals()
    ticker = property(**ticker())

    def trade_type():
        doc = "The trade_type property."
        def fget(self):
            return self._trade_type
        def fset(self, value):
            if value not in ('BUY','SELL'):
                raise ValueError("Trade type must be 'BUY' or 'SELL'")
            self._trade_type = value
        def fdel(self):
            del self._trade_type
        return locals()
    trade_type = property(**trade_type())

    def amount_units():
        doc = "The amount_units property."
        def fget(self):
            return self._amount_units
        def fset(self, value):
            if type(value) != int:
                raise TypeError("Amount of units must be of type integer")
            self._amount_units = value
        def fdel(self):
            del self._amount_units
        return locals()
    amount_units = property(**amount_units())

    def amount_wealth():
        doc = "The amount_wealth property."
        def fget(self):
            return self._amount_wealth
        def fset(self, value):
            if type(value) != float:
                raise TypeError("Amount of wealth must be of type float")
            if value < 0:
                raise ValueError("Amount of wealth cannot be negative")
            self._amount_wealth = value
        def fdel(self):
            del self._amount_wealth
        return locals()
    amount_wealth = property(**amount_wealth())

    def time_of_trade():
        doc = "The time_of_trade property."
        def fget(self):
            return self._time_of_trade
        def fset(self, value):
            if type(value) != dt.datetime:
                raise TypeError("Time of Trade must be of type \
                                    datetime.datetime")
            self._time_of_trade = value
        def fdel(self):
            del self._time_of_trade
        return locals()
    time_of_trade = property(**time_of_trade())

    def date_entry():
        doc = "The date_entry property."
        def fget(self):
            return self._date_entry
        def fset(self, value):
            if type(value) != dt.date:
                raise TypeError("Date of entry must be of type datetime.date")
            self._date_entry = value
        def fdel(self):
            del self._date_entry
        return locals()
    date_entry = property(**date_entry())

    def date_expiry():
        doc = "The date_expiry property."
        def fget(self):
            return self._date_expiry
        def fset(self, value):
            if type(value) != dt.date:
                raise TypeError("Date of expiry must be of type datetime.date")
            self._date_expiry = value
        def fdel(self):
            del self._date_expiry
        return locals()
    date_expiry = property(**date_expiry())

    def age():
        doc = "The age property."
        def fget(self):
            return self._age.days
        def fset(self, value):
            if type(value) != dt.timedelta:
                raise TypeError("Age must be of type datetime.timedelta")
            self._age = value
        def fdel(self):
            del self._age
        return locals()
    age = property(**age())

    def PL_today():
        doc = "The PL_today property."
        def fget(self):
            return self._PL_today
        def fset(self, value):
            if type(value) != float:
                raise ValueError("PL today must be of type float")
            self._PL_today = value
        def fdel(self):
            del self._PL_today
        return locals()
    PL_today = property(**PL_today())

    def PL_total():
        doc = "The PL_total property."
        def fget(self):
            return self._PL_total
        def fset(self, value):
            if type(value) != float:
                raise ValueError("PL total must be of type float")
            self._PL_total = value
        def fdel(self):
            del self._PL_total
        return locals()
    PL_total = property(**PL_total())

    def price_per_unit_entry():
        doc = "The price_per_unit_entry property."
        def fget(self):
            return self._price_per_unit_entry
        def fset(self, value):
            if type(value) != float:
                raise ValueError("Price per unit entry must be of type float")
            self._price_per_unit_entry = value
        def fdel(self):
            del self._price_per_unit_entry
        return locals()
    price_per_unit_entry = property(**price_per_unit_entry())

    def price_per_unit_today():
        doc = "The price_per_unit_today property."
        def fget(self):
            return self._price_per_unit_today
        def fset(self, value):
            if type(value) != float:
                raise ValueError("Price per unit today must be of type float")
            self._price_per_unit_today = value
        def fdel(self):
            del self._price_per_unit_today
        return locals()
    price_per_unit_today = property(**price_per_unit_today())

    """
    CLASS PRIVATE METHODS
    """
    def _updatePrice(self):
        #TODO: pass to BROKER
        pass

    def _updateAge(self):
        self.age = dt.date.today() - self.date_entry

    def _updatePLToday(self):
        return PL_today

    def _updatePLTotal(self):
        return PL_total

    def updatePosition(self):
        self._updatePrice()
        self._updateAge()
        self._updatePLToday()
        self._updatePLTotal()

    """
    CLASS PUBLIC METHODS
    """
    def getPosition(self):
        return self

    def getCurrentPosition(self):
        updatePosition()
        return getPosition()

    def getPositionDF(self):
        df_position_record = pd.DataFrame(index = 'ID_position',
                                            columns = ['instrument','ticker',
                                            'trade_type','amount_units',
                                            'amount_wealth',
                                            'price_per_unit_entry',
                                            'price_per_unit_today',
                                            'time_of_trade', 'date_entry',
                                            'date_expiry', 'age', 'PL_today',
                                            'PL_total'])

        df_position_record['instrument'] = self.instrument
        df_position_record['ticker'] = self.ticker
        df_position_record['trade_type'] = self.trade_type
        df_position_record['amount_units'] = self.amount_units
        df_position_record['amount_wealth'] = self.amount_wealth

        df_position_record['price_per_unit_entry'] = self.price_per_unit_entry
        df_position_record['price_per_unit_today'] = self.price_per_unit_today

        df_position_record['time_of_trade'] = self.time_of_trade
        df_position_record['date_entry'] = self.date_entry
        df_position_record['date_expiry'] = self.date_expiry
        df_position_record['age'] = self.age

        df_position_record['PL_today'] = self.PL_today
        df_position_record['PL_total'] = self.PL_total

        return df_position_record

    def getCurrentPositionDF(self):
        getCurrentPosition()
        return getPositionDF()

    def reversePosition(self):
        print('WARNING: position_reverse may override previous object')
        position_reverse = self
        if position_reverse.trade_type == 'BUY':
            position_reverse.trade_type = 'SELL'
        elif position_reverse.trade_type == 'SELL':
            position_reverse.trade_type = 'BUY'

        return position_reverse

class PositionStock(Position):
    """docstring for PositionStock"""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, ID = '', instrument = '', ticker = '', trade_type = '',
                    amount_units = 0, amount_wealth = 0.0,
                    time_of_trade = dt.datetime.today(),
                    date_expiry = dt.date.today().day
                    ):

        super(PositionStock, self).__init__(ID = ID, instrument = instrument,
                ticker = ticker, trade_type = trade_type,
                amount_units = amount_units, amount_wealth = amount_wealth,
                time_of_trade = time_of_trade, date_expiry = date_expiry)

        self._stock_class_specific_attributes = None

class PositionFutures(Position):
    """docstring for postionFutures."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, ID = '', instrument = '', ticker = '', trade_type = '',
                    amount_units = 0, amount_wealth = 0.0,
                    time_of_trade = dt.datetime.today(),
                    date_expiry = dt.date.today().day
                    ):

        super(PositionFutures, self).__init__(ID = ID, instrument = instrument,
                ticker = ticker, trade_type = trade_type,
                amount_units = amount_units, amount_wealth = amount_wealth,
                time_of_trade = time_of_trade, date_expiry = date_expiry)

        self._futures_class_specific_attributes = None

class postionOptions(Position):
    """docstring for postionOptions."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, ID = '', instrument = '', ticker = '', trade_type = '',
                    amount_units = 0, amount_wealth = 0.0,
                    time_of_trade = dt.datetime.today(),
                    date_expiry = dt.date.today().day
                    ):

        super(postionOptions, self).__init__(ID = ID, instrument = instrument,
                ticker = ticker, trade_type = trade_type,
                amount_units = amount_units, amount_wealth = amount_wealth,
                time_of_trade = time_of_trade, date_expiry = date_expiry)

        self._options_class_specific_attributes = None


def test():
    pass
