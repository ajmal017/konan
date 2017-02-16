"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.broker.py
Created on 2017-02-14T16:36:00Z
@author:Joshua Hu
"""
# imports from future
from __future__ import print_function

#imports from stdlib
import sys
import traceback
import time
import datetime as dt

# third party imports
import pandas as pd
import numpy as np
from tqdm import tqdm

from IBWrapper import IBWrapper, contract
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ScannerSubscription import ScannerSubscription

from ib.ext.Contract import Contract
from ib.ext.ExecutionFilter import ExecutionFilter
from ib.ext.Order import Order

# internal/custom imports
import position

class Broker(object):
    """docstring for broker."""
    def __init__(self):
        super(broker, self).__init__()

class IBBroker(broker):
    """docstring for IBBroker."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100):
        super(IBBroker, self).__init__()
        self._account_name = account_name
        self._callback = IBWrapper()
        # one callback or more? i.e. reset callback vs new instace
        self._tws = EClientSocket(self.callback)
        self._host = host
        self._port = port
        self._client_id = client_id

        self.tws.eConnect(self.host, self.port, self.client_id)
        # may have to connect repeatedly

    """
    CLASS PROPERTIES
    """
    def account_name():
        doc = "The account_name property."
        def fget(self):
            return self._account_name
        def fset(self, value):
            self._account_name = value
        def fdel(self):
            del self._account_name
        return locals()
    account_name = property(**account_name())

    def callback():
        doc = "The callback property."
        def fget(self):
            return self._callback
        def fset(self, value):
            self._callback = value
        def fdel(self):
            del self._callback
        return locals()
    callback = property(**callback())

    def tws():
        doc = "The tws property."
        def fget(self):
            return self._tws
        def fset(self, value):
            self._tws = value
        def fdel(self):
            del self._tws
        return locals()
    tws = property(**tws())

    def host():
        doc = "The host property."
        def fget(self):
            return self._host
        def fset(self, value):
            self._host = value
        def fdel(self):
            del self._host
        return locals()
    host = property(**host())

    def port():
        doc = "The port property."
        def fget(self):
            return self._port
        def fset(self, value):
            self._port = value
        def fdel(self):
            del self._port
        return locals()
    port = property(**port())

    def client_id():
        doc = "The client_id property."
        def fget(self):
            return self._client_id
        def fset(self, value):
            self._client_id = value
        def fdel(self):
            del self._client_id
        return locals()
    client_id = property(**client_id())

    """
    CLASS PRIVATE METHODS
    """
    #can the connect method be encapsulated?
    def connect(self):
        pass

    """
    CLASS PUBLIC METHODS
    """
    def nextOrderId(self):
        return self.tws.reqIds(1)

    def createContract(self, symbol, secType, exchange, currency, right = None,
                        strike = None, expiry = None, multiplier = None,
                        tradingClass = None):

        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = secType
        contract.m_exchange = exchange
        contract.m_currency = currency
        contract.m_right = right
        contract.m_strike = strike
        contract.m_expiry = expiry
        contract.m_multiplier = multiplier
        contract.m_tradingClass = tradingClass
        return contract

    def createOrder():
        pass

    def make_order(action,quantity, price = None):
        if price is not None:
            order = Order()
            order.m_orderType = 'LMT'
            order.m_totalQuantity = quantity
            order.m_action = action
            order.m_lmtPrice = price
        else:
            order = Order()
            order.m_orderType = 'MKT'
            order.m_totalQuantity = quantity
            order.m_action = action
        return order

    def prepareOrder(position = position.Position()):
        pass



class DataBroker(broker):
    """docstring for DataBroker."""
    def __init__(self):
        super(DataBroker, self).__init__()

    def getLocalData(path = data.Repository()):
        return None

class IBDataBroker(IBBroker, DataBroker):
    """docstring for IBDataBroker."""
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100):
        super(IBDataBroker, self).__init__(account_name, host, port, client_id)

    def getMarketData(type_data = '', time = dt.datetime.now()):
        dict_data_type = {'OPEN':_getMarketOpenData,
                            'CLOSE':_getMarketCloseData,
                            'HI':_getMarketHighData, 'LO':_getMarketLowData,
                            'TIME':_getMarketTimeData}
        if type_data not in dict_data_type:
            raise ValueError("Market data type is not valid")

        return dict_data_type[type_data](time)

    def _getMarketOpenData(time = dt.datetime.now()):
        order_id = self.nextOrderId()

        return None

    def _getMarketCloseData(time = dt.datetime.now()):
        return None

    def _getMarketHighData(time = dt.datetime.now()):
        return None

    def _getMarketLowData(time = dt.datetime.now()):
        return None

    def _getMarketTimeData(time = dt.datetime.now()):
        return None


class ExecutionBroker(broker):
    """docstring for ExecutionBroker."""
    def __init__(self):
        super(ExecutionBroker, self).__init__()

class IBExecutionBroker(IBBroker, ExecutionBroker):
    """docstring for IBExecutionBroker."""
    def __init__(self):
        super(IBExecutionBroker, self).__init__()
    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """
