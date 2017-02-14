#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
trade.py
Created on Thu Feb 09 16:48 2017
@author: Joshua Hu

///////////
Constants**
///////////
None

/////////
Classes**
/////////
Parent:

Children:

"""
import datetime as dt

class position(object):
    """docstring for position"""
    def __init__(self, ID = '', instrument = '', ticker = '', trade_type = '',
                    amount_units = 0, amount_value = 0.0,
                    time_of_trade = dt.datetime.today(),
                    expiry_date = dt.date.today().day,
                    entry_price_per_unit = 0.0):
        self._ID = ID
        self._instrument = instrument
        self._ticker = ticker
        self._trade_type = trade_type
        self._amount_units = amount_units
        self._amount_value = amount_value
        self._time_of_trade = time_of_trade
        self._entry_date = self.time_of_trade.date()
        self._expiry_date = expiry_date
        self._age = dt.date.today().date - self.entry_date
        self._entry_price_per_unit = entry_price_per_unit
        self._PL_total = 0.0
        self._PL_today = 0.0

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
            self._amount_units = value
        def fdel(self):
            del self._amount_units
        return locals()
    amount_units = property(**amount_units())

    def amount_value():
        doc = "The amount_value property."
        def fget(self):
            return self._amount_value
        def fset(self, value):
            self._amount_value = value
        def fdel(self):
            del self._amount_value
        return locals()
    amount_value = property(**amount_value())

    def time_of_trade():
        doc = "The time_of_trade property."
        def fget(self):
            return self._time_of_trade
        def fset(self, value):
            self._time_of_trade = value
        def fdel(self):
            del self._time_of_trade
        return locals()
    time_of_trade = property(**time_of_trade())

    def entry_date():
        doc = "The entry_date property."
        def fget(self):
            return self._entry_date
        def fset(self, value):
            self._entry_date = value
        def fdel(self):
            del self._entry_date
        return locals()
    entry_date = property(**entry_date())

    def expiry_date():
        doc = "The expiry_date property."
        def fget(self):
            return self._expiry_date
        def fset(self, value):
            self._expiry_date = value
        def fdel(self):
            del self._expiry_date
        return locals()
    expiry_date = property(**expiry_date())

    def age():
        doc = "The age property."
        def fget(self):
            return self._age
        def fset(self, value):
            self._age = value
        def fdel(self):
            del self._age
        return locals()
    age = property(**age())

    def entry_price_per_unit():
        doc = "The entry_price_per_unit property."
        def fget(self):
            return self._entry_price_per_unit
        def fset(self, value):
            self._entry_price_per_unit = value
        def fdel(self):
            del self._entry_price_per_unit
        return locals()
    entry_price_per_unit = property(**entry_price_per_unit())

    def updateAge(self):
        self.age = dt.date.today() - self.entry_date

    def calculatePLToday(self):
        return PL_today

    def updatePLTotal(self):
        return PL_total

class positionStock(position):
    """docstring for positionStock"""
    def __init__(self):
        pass

class positionFutures(position):
    def __init__(self):
        pass

class postionOptions(position):
    """docstring for postionOptions."""
    def __init__(self, arg):
        super(postionOptions, self).__init__()
        self.arg = arg
