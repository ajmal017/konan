"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.Broker.py
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

from IBWrapper import IBWrapper
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ScannerSubscription import ScannerSubscription

from ib.ext.Contract import Contract
from ib.ext.ExecutionFilter import ExecutionFilter
from ib.ext.Order import Order

# internal/custom imports
import data
import position

class BrokerConnection(object):
    """docstring for BrokerConnection."""
    def __init__(self):
        super(BrokerConnection, self).__init__()
        #self.arg = arg

class IBBrokerConnection(BrokerConnection):
    """docstring for IBBrokerConnection."""
    def __init__(self, callback = IBWrapper()):
        super(IBBrokerConnection, self).__init__()
        self._interface = EClientSocket(callback)

    def interface():
        doc = "The interface property."
        def fget(self):
            return self._interface
        def fset(self, value):
            self._interface = value
        def fdel(self):
            del self._interface
        return locals()
    interface = property(**interface())

class Broker(object):
    """docstring for Broker."""
    def __init__(self):
        super(Broker, self).__init__()

class IBBroker(Broker):
    """docstring for IBBroker."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, account_name = 'DU603835',
                    connection = IBBrokerConnection(), host = '', port = 7497,
                    client_id = 100):
        super(IBBroker, self).__init__()
        self._account_name = account_name

        self._callback = IBWrapper()
        self.callback.initiate_variables()

        self._connection = IBBrokerConnection(self.callback)

        self._tws = self.connection.interface

        self._host = host
        self._port = port
        self._client_id = client_id

        #self.connect()

        #read state from file or call from IB
        #store as dictionary or DF?
        #keep trying to create a valid id?
        #apparently not needed
        #self._current_contract_id = 1

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

    def connection():
        doc = "The connection property."
        def fget(self):
            return self._connection
        def fset(self, value):
            self._connection = value
        def fdel(self):
            del self._connection
        return locals()
    connection = property(**connection())

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
   def current_contract_id():
        doc = "The current_contract_id property."
        def fget(self):
            return self._current_contract_id
        def fset(self, value):
            self._current_contract_id = value
        def fdel(self):
            del self._current_contract_id
        return locals()
    current_contract_id = property(**current_contract_id())
    """
    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """
    def connect(self):
        self.tws.eConnect(self.host, self.port, self.client_id)

    def disconnect(self):
        self.tws.eDisconnect()

    def nextOrderId(self):
        return self.tws.reqIds(1)

    def createContract(self, ticker, instrument_type,
                        exchange = 'SMART', currency = 'USD',
                        last_trade_date = None, expiry = None,
                        strike_price = None, right = None, multiplier = None,
                        primary_exchange_ticker = None, primary_exchange = None,
                        trading_class = None, include_expired = None,
                        secIdType = None, secId = None,
                        combo_legs_description = None, combo_legs = None,
                        under_comp = None):
        contract = Contract()

        #The unique IB contract identifier.
        #contract.m_conId = contract_id

        #The underlying's asset symbol.
        contract.m_symbol = ticker

        #The security's type: STK - stock (or ETF) OPT - option FUT - future
        #IND - index FOP - futures option CASH - forex pair BAG - combo
        #WAR - warrant BOND- bond CMDTY- commodity NEWS- news FUND- mutual fund.
        contract.m_secType = instrument_type

        #The destination exchange.
        contract.m_exchange = exchange

        #The underlying's cuurrency.
        contract.m_currency = currency

        """
        #The contract's symbol within its primary exchange.
        contract.m_localSymbol = primary_exchange_ticker

        #The contract's primary exchange.
        contract.m_primaryExch = primary_exchange

        #The trading class name for this contract.
        #Available in TWS contract description window as well.
        #For example, GBL Dec '13 future's trading class is "FGBL".
        contract.m_tradingClass = trading_class

        #If set to true, contract details requests and historical data queries
        #can be performed pertaining to expired contracts.
        #Note: Historical data queries on expired contracts are limited to
        #the last year of the contracts life, and are initially only supported
        #for expired futures contracts.
        contract.m_includeExpired = include_expired

        #Security's identifier when querying contract's details
        #or placing orders SIN - Example: Apple: US0378331005 CUSIP
        #- Example: Apple: 037833100 SEDOL - Consists of 6-AN + check digit.
        #Example: BAE: 0263494 RIC - Consists of exchange-independent RIC Root
        #and a suffix identifying the exchange.
        #Example: AAPL.O for Apple on NASDAQ.
        contract.m_secIdType = secIdType

        #Identifier of the security type.
        contract.m_secId = secId

        #Description of the combo legs.
        contract.m_comboLegsDescription = combo_legs_description

        #The legs of a combined contract definition.
        contract.m_comboLegs = combo_legs

        #Delta and underlying price for Delta-Neutral combo orders.
        #Underlying (STK or FUT), delta and underlying price
        #goes into this attribute.
        contract.m_underComp = under_comp
        """

        dict_instrument_type = {'STK':self._createStockContract,
                                'OPT':self._createOptionContract,
                                'FUT':self._createFutureContract,
                                'IND':self._createIndexContract,
                                'CASH':self._createCashContract,
                                'BAG':self._createCombinationContract,
                                'WAR':self._createWarrantContract,
                                'BOND':self._createBondContract,
                                'CMDTY':self._createCommodityContract,
                                'NEWS':self._createNewsContract,
                                'FUND':self._createMutualFundContract}

        return dict_instrument_type[instrument_type](contract = contract)

    def _createStockContract(self, contract = Contract()):
        return contract

    def _createOptionContract(self, contract = Contract()):
        #The contract's last trading day or contract month
        #(for Options and Futures).
        #Strings with format YYYYMM will be interpreted as the Contract Month
        #whereas YYYYMMDD will be interpreted as Last Trading Day.
        contract.m_lastTradeDateOrContractMonth = last_trade_date
        contract.m_expiry = expiry # is this the same as last_trade_date ?

        #The option's strike price.
        contract.m_strike = strike_price

        #Either Put or Call (i.e. Options). Valid values are P, PUT, C, CALL.
        contract.m_right = right

        #The instrument's multiplier (i.e. options, futures).
        contract.m_multiplier = multiplier
        return contract

    def _createFutureContract(self, contract = Contract()):
        #The contract's last trading day or contract month
        #(for Options and Futures).
        #Strings with format YYYYMM will be interpreted as the Contract Month
        #whereas YYYYMMDD will be interpreted as Last Trading Day.
        contract.m_lastTradeDateOrContractMonth = last_trade_date
        contract.m_expiry = expiry # is this the same as last_trade_date ?

        #The instrument's multiplier (i.e. options, futures).
        contract.m_multiplier = multiplier
        return contract

    def _createIndexContract(self, contract = Contract()):
        return contract

    def _createCashContract(self, contract = Contract()):
        return contract

    def _createCombinationContract(self, contract = Contract()):
        return contract

    def _createWarrantContract(self, contract = Contract()):
        return contract

    def _createBondContract(self, contract = Contract()):
        return contract

    def _createCommodityContract(self, contract = Contract()):
        return contract

    def _createNewsContract(self, contract = Contract()):
        return contract

    def _createMutualFundContract(self, contract = Contract()):
        return contract

    def createOrder(trade_type, amount_units, price_per_unit = None):
        if price_per_unit is not None:
            order = Order()
            order.m_orderType = 'LMT'
            order.m_totalQuantity = amount_units
            order.m_action = trade_type
            order.m_lmtPrice = price_per_unit
        else:
            order = Order()
            order.m_orderType = 'MKT'
            order.m_totalQuantity = amount_units
            order.m_action = trade_type
        return order

    def preparePosition(position = position.Position()):
        return None

class DataBroker(Broker):
    """docstring for DataBroker."""
    def __init__(self, path_root_data = '', project = '', data_file = ''):
        super(DataBroker, self).__init__()

        self._data_repository = data.Repository(root = path_root_data,
                                                project = project,
                                                data_file = data_file)
        self._path_root_data = path_root_data

    def getLocalData(self, root): #data.Repository()):
        return None

class IBDataBroker(IBBroker, DataBroker):
    """docstring for IBDataBroker."""
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100):
        super(IBDataBroker, self).__init__(account_name = account_name,
                                            host = host, port = port,
                                            client_id = client_id)

        #read state from file or call from IB
        #store as dictionary or DF?
        #keep trying to create a valid id?
        self._current_request_id = 1

    def current_request_id():
        doc = "The current_request_id property."
        def fget(self):
            return self._current_request_id
        def fset(self, value):
            self._current_request_id = value
        def fdel(self):
            del self._current_request_id
        return locals()
    current_request_id = property(**current_request_id())

    def getAccountInformation(self, all_accounts = True, attributes = ','):
        """
        attributes values:
        AccountType - Identifies the IB account structure
        NetLiquidation - The basis for determining the price of the assets in
            your account. Total cash value + stock value + options value + bond value
        TotalCashValue - Total cash balance recognized at the time of trade
            + futures PNL
        SettledCash - Cash recognized at the time of settlement
            - purchases at the time of trade - commissions - taxes - fees
        AccruedCash - Total accrued cash value of stock, commodities
            and securities
        BuyingPower - Buying power serves as a measurement of the dollar value
            of securities that one may purchase in a securities account
            without depositing additional funds
        EquityWithLoanValue - Forms the basis for determining whether a client
            has the necessary assets to either initiate
            or maintain security positions. Cash + stocks + bonds + mutual funds
        PreviousEquityWithLoanValue - Marginable Equity with Loan value
            as of 16:00 ET the previous day
        GrossPositionValue - The sum of the absolute value
            of all stock and equity option positions
        RegTEquity - Regulation T equity for universal account
        RegTMargin - Regulation T margin for universal account
        SMA - Special Memorandum Account: Line of credit created
            when the market value of securities in a Regulation T account
            increase in value
        InitMarginReq - Initial Margin requirement of whole portfolio
        MaintMarginReq - Maintenance Margin requirement of whole portfolio
        AvailableFunds - This value tells what you have available for trading
        ExcessLiquidity - This value shows your margin cushion,
            before liquidation
        Cushion - Excess liquidity as a percentage of net liquidation value
        FullInitMarginReq - Initial Margin of whole portfolio
            with no discounts or intraday credits
        FullMaintMarginReq - Maintenance Margin of whole portfolio
            with no discounts or intraday credits
        FullAvailableFunds - Available funds of whole portfolio
            with no discounts or intraday credits
        FullExcessLiquidity - Excess liquidity of whole portfolio
            with no discounts or intraday credits
        LookAheadNextChange - Time when look-ahead values take effect
        LookAheadInitMarginReq - Initial Margin requirement of whole portfolio
            as of next period's margin change
        LookAheadMaintMarginReq - Maintenance Margin requirement
            of whole portfolio as of next period's margin change
        LookAheadAvailableFunds - This value reflects your available funds
            at the next margin change
        LookAheadExcessLiquidity - This value reflects your excess liquidity
            at the next margin change
        HighestSeverity - A measure of how close the account is to liquidation
        DayTradesRemaining - The Number of Open/Close trades a user
            could put on before Pattern Day Trading is detected.
            A value of "-1" means that the user can put on unlimited day trades.
        Leverage - GrossPositionValue / NetLiquidation
        """

        if all_accounts:
            group = "All"
        self.tws.reqAccountSummary(reqId = self.current_request_id,
                                    group = group, tags = attributes)
        return pd.DataFrame(self.callback.account_Summary,
                        columns =
                        ['Request_ID','Account','Tag','Value','Curency'])

    def getHistoricalMarketData(self, ticker_id, type_data = '',
                        contract = Contract(),
                        time_start = dt.datetime.now(),
                        time_end = dt.datetime.now(), resolution = '1 min'):
        dict_data_type = {'OPEN':self._getHistoricalMarketOpenData,
                            'CLOSE':self._getHistoricalMarketCloseData,
                            'HI':self._getHistoricalMarketHighData,
                            'LO':self._getHistoricalMarketLowData,
                            'TIME':self._getHistoricalMarketTimeData}
        if type_data not in dict_data_type:
            raise ValueError("Market data type is not valid")

        return dict_data_type[type_data](ticker_id = ticker_id,
                                        contract = contract,
                                        time_start = time_start,
                                        time_end = time_end)

    def _getHistoricalMarketOpenData(self,
                            ticker_id, contract = Contract(),
                            time_start = dt.datetime.now(),
                            time_end = dt.datetime.now()):
        duration = str((time_end - time_start).seconds)+' S'
        print(duration)
        # external dictionary or association that allows for contracts
        # to be associated with a tickerId
        #dict_ticker_id = {'AAPL':1}
        #ticker_id = self.dict_ticker_id[contract.m_symbol]
        self.tws.reqHistoricalData(tickerId = ticker_id, contract = contract,
                                    endDateTime = time_end.strftime("%Y%m%d %H:%M:%S"),
                                    durationStr = duration,
                                    barSizeSetting = '1 min', whatToShow = 'BID',
                                    useRTH = 0, formatDate = 1)

        time.sleep(1)

        data= pd.DataFrame(self.callback.historical_Data, columns = ["reqId",
                                                                "date", "open",
                                                                "high", "low",
                                                                "close",
                                                                "volume",
                                                                "count", "WAP",
                                                                "hasGaps"])
        return data.iloc[0:1]

    def _getHistoricalMarketCloseData(self,
                            ticker_id, contract = Contract(),
                            time_start = dt.datetime.now(),
                            time_end = dt.datetime.now()):
        return data.iloc[-2:-1]

    def _getHistoricalMarketHighData(self,
                            ticker_id, contract = Contract(),
                            time_start = dt.datetime.now(),
                            time_end = dt.datetime.now()):
        return None

    def _getHistoricalMarketLowData(self,
                            ticker_id, contract = Contract(),
                            time_start = dt.datetime.now(),
                            time_end = dt.datetime.now()):
        return None

    def _getHistoricalMarketTimeData(self,
                            ticker_id, contract = Contract(),
                            time_start = dt.datetime.now(),
                            time_end = dt.datetime.now()):
        return None

    def getLiveMarketData(self):
        self.tws.reqMktData()
        return self.callback.tick_Price

class ExecutionBroker(Broker):
    """docstring for ExecutionBroker."""
    def __init__(self):
        super(ExecutionBroker, self).__init__()

class IBExecutionBroker(IBBroker, ExecutionBroker):
    """docstring for IBExecutionBroker."""
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100):
        super(IBExecutionBroker, self).__init__(account_name = account_name,
                                                host = host, port = port,
                                                client_id = client_id)
    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """

    def placeOrder(self, order_id, contract, order):
        self.tws.placeOrder(order_id, contract, order)

    def cancelOrder(self, order_id):
        self.tws.cancelOrder(order_id)
