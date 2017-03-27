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
import dateutil as du
import glob
import fnmatch

# third party imports
import pandas as pd
#import pandas_datareader as pdr
from pandas_datareader import data as web
import numpy as np
from tqdm import tqdm

# Interactive Brokers related packages; IbPy package
from IBWrapper import IBWrapper
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ScannerSubscription import ScannerSubscription

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.ext.ExecutionFilter import ExecutionFilter

# internal/custom imports
import directory as dr
import data
import position as pos

class BrokerConnection(object):
    """
    Connection resource to be shared by brokers in a sytem's public environment
    without disrupting properties of the connection.
    E.g. connection status, object representation.
    """
    def __init__(self):
        """
        __init__:
        Basic BrokerConnection constructor. Initializes object properties.
        
        PARAMETERS:
        None
        
        RETURNS:
        None
        
        RESULTS:
        Creates BrokerConnection object.
        """
        super(BrokerConnection, self).__init__()

class IBBrokerConnection(BrokerConnection):
    """
    Connection interface implementing the Interactive Brokers (IB)
    EClientSocket API behaviours. Allows the EClientSocket object to be shared.
    """
    def __init__(self, callback = IBWrapper()):
        """
        __init__:
        IBBrokerConnection constructor. Initializes object properties.
        
        PARAMETERS:
        callback - IBWrapper()
            Implementation of an abstract class in the Interactive Brokers (IB)
            API which stores the results of API calls
        
        RETURNS:
        None
        
        RESULTS:
        Creates IBBrokerConnection object.
        """
        super(IBBrokerConnection, self).__init__()
        self._interface = EClientSocket(callback)

    """
    CLASS PROPERTIES

    interface:
        EClientSocket object that takes in the implemented IBWrapper class in which
        API calls are stored
    """
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
        """
        Broker constructor.
        Initializes object properties.

        PARAMETERS:

        RETURNS:

        RESULTS:
        """
        super(Broker, self).__init__()

class IBBroker(Broker):
    """
    docstring for IBBroker.
    """
    def __init__(self, account_name = 'DU603835',
                    connection = IBBrokerConnection(), host = '', port = 7497,
                    client_id = 100, **kw):
        """
        Broker constructor.
        Initializes object properties.

        PARAMETERS:
        account_name -
        connection -
        host -
        port -
        client_id -
        """
        super(IBBroker, self).__init__()
        self._account_name = account_name

        self._callback = IBWrapper()
        self.callback.initiate_variables()

        self._connection = IBBrokerConnection(self.callback)

        self._tws = self.connection.interface #could just assign to _connection

        self._host = host
        self._port = port
        self._client_id = client_id

    """
    CLASS PROPERTIES
    """
    def account_name():
        doc = "The unique Interactive Brokers acccount name."
        def fget(self):
            return self._account_name
        def fset(self, value):
            self._account_name = value
        def fdel(self):
            del self._account_name
        return locals()
    account_name = property(**account_name())

    def callback():
        doc = "The callback initialized by this broker instance."
        def fget(self):
            return self._callback
        def fset(self, value):
            self._callback = value
        def fdel(self):
            del self._callback
        return locals()
    callback = property(**callback())

    def connection():
        doc = "The connection initialized for this broker instance."
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
    CLASS SPECIAL METHODS
    """
    def __str__(self):
        return "Acount Name:{} on Port:{} with Client ID:{} ".format(self.account_name, self.client_id, self.port)

    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """
    def connect(self):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if self.connected():
            print('Broker is already connected.')
            pass
        self.tws.eConnect(self.host, self.port, self.client_id)

    def disconnect(self):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        self.tws.eDisconnect()

    def connected(self):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return self.tws.isConnected()

    def nextOrderId(self, from_IB = False):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if from_IB:
            self.tws.reqIds(1)
            return self.callback.next_ValidId
        else:
            dt_ = dt.datetime.now()
#            strID = "".join((str(dt_.month), str(dt_.day), str(dt_.hour),
#                             str(dt_.minute), str(dt_.second),
#                             str(dt_.microsecond)[0:1]))
            
            strID = "".join((str(dt_.day), str(dt_.hour),
                             str(dt_.minute), str(dt_.second),
                             str(dt_.microsecond)[0:1]))
            return (int(strID))

    def createContract(self, ticker, instrument_type,
                        exchange = 'SMART', currency = 'USD',
                        last_trade_date = None, expiry = None,
                        strike_price = None, right = None, multiplier = None,
                        primary_exchange_ticker = None, primary_exchange = None,
                        trading_class = None, include_expired = None,
                        secIdType = None, secId = None,
                        combo_legs_description = None, combo_legs = None,
                        under_comp = None):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
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

        contract.m_primaryExch = primary_exchange

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

        # TODO: NEED TO PASS ALL THE AVAILABLE PARAMETERS TO LOWER METHODS
        return dict_instrument_type[instrument_type](contract = contract)

    def _createStockContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def _createOptionContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
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
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
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
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def _createCashContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def _createCombinationContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def _createWarrantContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def _createBondContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def _createCommodityContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def _createNewsContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def _createMutualFundContract(self, contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return contract

    def createOrder(self, trade_type, amount_units, price_per_unit = 0.0,
                    order_type = '', time_in_force = 'GTC'):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        """
        ORDER TYPES:
        Limit	LMT
        Limit Risk
        Bracket
        Market-to-Limit	MTL
        Market with Protection	MKT PRT
        Request for Quote	QUOTE
        Stop	STP
        Stop Limit	STP LMT
        Trailing Limit if Touched	TRAIL LIT
        Trailing Market If Touched	TRAIL MIT
        Trailing Stop	TRAIL
        Trailing Stop Limit	TRAIL LIMIT
        Speed of Execution
        At Auction
        Discretionary
        Market	MKT
        Market-if-Touched	MIT
        Market-on-Close	MOC
        Market-on-Open	MOO
        Pegged-to-Market	PEG MKT
        Relative	REL
        Sweep-to-Fill
        Price Improvement
        Box Top	BOX TOP
        Price Improvement Auction
        Block
        Limit-on-Close	LOC
        Limit-on-Open	LOO
        Limit if Touched	LIT
        Pegged-to-Midpoint	PEG MID
        Privacy
        Hidden
        Iceberg/Reserve
        VWAP - Guaranteed	VWAP
        Time to Market
        All-or-None
        Fill-or-Kill
        Good-after-Time/Date	GAT
        Good-till-Date/Time	GTD
        Good-till-Canceled	GTC
        Immediate-or-Cancel	IOC
        Advanced Trading
        One-Cancels-All	OCA
        Spreads
        Volatility	VOL
        Algorithmic Trading (Algos)
        Arrival Price
        Balance Impact and Risk
        Minimize Impact
        Percent of volume
        Scale
        TWAP
        VWAP - Best Effort
        Accumulate/Distribute
        IBDARK
        """
        if order_type not in ('LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT',
                              'QUOTE', 'STP', 'STP LMT', 'TRAIL LIT',
                              'TRAIL MIT', 'TRAIL', 'TRAIL LIMIT', 'MIT', 'MOO',
                              'PEG MKT', 'REL', 'BOX TOP', 'LOC', 'LOO', 'LIT',
                              'PEG MID', 'VWAP', 'GAT', 'GTD', 'GTC', 'IOC',
                              'OCA', 'VOL'):
            print("Given order_type is not a proper type.\nMust be one of: "\
                  "'LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT', 'QUOTE', 'STP',"\
                  "'STP LMT', 'TRAIL LIT', 'TRAIL MIT', 'TRAIL',"\
                  "'TRAIL LIMIT','MIT', 'MOO', 'PEG MKT', 'REL', 'BOX TOP',"\
                  "'LOC', 'LOO', 'LIT', 'PEG MID', 'VWAP', 'GAT', 'GTD',"\
                  "'GTC','IOC', 'OCA', 'VOL'.")
            return None

        order = Order()
        order.m_totalQuantity = amount_units
        order.m_action = trade_type
        order.m_tif = time_in_force

        if order_type == 'LIMIT':
            order.m_orderType = 'LMT'
            order.m_lmtPrice = price_per_unit * amount_units

        elif order_type == 'MARKET':
            order.m_orderType = 'MKT'
            
        elif order_type == 'MOC':
            order.m_orderType = 'MOC'
            

        return order

    def preparePosition(self, position = pos.Position()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        """Unpack position object into order and contracts"""
        raise NotImplementedError("API method preparePosition has not been implemented.")
        return None

    def createExecutionFilter(self, contract = None, order_time = None):
        if contract == None:
            return ExecutionFilter()
        execution_filter = ExecutionFilter()
        execution_filter.m_clientId = self.client_id
        execution_filter.m_acctCode = self.account_name
        execution_filter.m_symbol = contract.m_symbol
        execution_filter.m_secType = contract.m_secType
        execution_filter.m_exchange = contract.m_exchange

        if order_time == None:
            execution_filter.m_time = dt.datetime.now().strftime('%Y%m%d %H:%M:%S')
        else:
            execution_filter.m_time = order_time.strftime('%Y%m%d %H:%M:%S')
        return execution_filter

class DataBroker(Broker):
    """docstring for DataBroker."""
    def __init__(self, path_root = '/', project = '', data_file = '', **kw):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        super(DataBroker, self).__init__()

        self._data_repository = data.Repository(path_root = path_root,
                                                project = project,
                                                data_file = data_file)
        self._path_root = path_root

    def data_repository():
        doc = "The data_repository property."
        def fget(self):
            return self._data_repository
        def fset(self, value):
            self._data_repository = value
        def fdel(self):
            del self._data_repository
        return locals()
    data_repository = property(**data_repository())

    def path_root():
        doc = "The path_root property."
        def fget(self):
            return self._path_root
        def fset(self, value):
            self._path_root = value
        def fdel(self):
            del self._path_root
        return locals()
    path_root = property(**path_root())

    def getLocalData(self, type_data = '', path_data = '', file_name = ''): #data.Repository()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        files = glob.iglob(path_data + '*.' + type_data)
        while True:
            f = files.next()
            if fnmatch.fnmatch(f, '*' + file_name + '.' + type_data):
                return f
        return ''

class IBDataBroker(IBBroker, DataBroker):
    """docstring for IBDataBroker."""
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, path_root = '/', **kw):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        super(IBDataBroker, self).__init__(account_name = account_name,
                                            host = host, port = port,
                                            client_id = client_id,
                                            path_root = path_root)

        #read state from file or call from IB
        #store as dictionary or DF?
        #keep trying to create a valid id?
        self._current_request_id = 1

        self._tickers = {}
        self._current_ticker_id = 1

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

    def tickers():
        doc = "The tickers property."
        def fget(self):
            return self._tickers
        def fset(self, contract): # ('ticker', Contract())
            if self.current_ticker_id in self._tickers:
                self._incrementTickerID()
            ticker_id = self.current_ticker_id
            ticker = contract.m_symbol
            if self._tickers == {}:
                self._tickers[ticker_id] = (ticker, contract)
                return
            for element in self._tickers:
                if contract == self._tickers[element][1]:
                    print("Contract already in dictionary.")
                    return
            self._tickers[ticker_id] = (ticker, contract)
            self._incrementTickerID()
        def fdel(self):
            del self._tickers
        return locals()
    tickers = property(**tickers())

    def current_ticker_id():
        doc = "The current_ticker_id property."
        def fget(self):
            return self._current_ticker_id
        def fset(self, value):
            self._current_ticker_id = value
        def fdel(self):
            del self._current_ticker_id
        return locals()
    current_ticker_id = property(**current_ticker_id())

    def _resetCallbackAttribute(self, attribute = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if attribute in ('accountDownloadEnd_flag', 'account_SummaryEnd_flag',
                            'positionEnd_flag', 'tickSnapshotEnd_flag',
                            'connection_Closed', 'exec_DetailsEnd_flag',
                            'contract_Details_flag', 'historical_DataEnd_flag',
                            'scanner_Data_End_flag'):
            setattr(self.callback, attribute, False)

        if attribute in ('open_OrderEnd_flag'):
            setattr(self.callback, attribute, True)

        if attribute in ('update_AccountValue', 'update_Portfolio',
                            'account_Summary', 'update_Position',
                            'order_Status', 'open_Order', 'tick_Price',
                            'tick_Size', 'tick_OptionComputation',
                            'tick_Generic', 'tick_String', 'tick_EFP',
                            'tickSnapshotEnd_reqId', 'exec_Details_reqId',
                            'exec_Details_contract', 'exec_Details_execution',
                            'update_MktDepth', 'update_MktDepthL2',
                            'historical_Data', 'scanner_Data', 'real_timeBar'):
            setattr(self.callback, attribute, [])

        else:
            print("Attribute not found.\nNo attribute reset.")

    def getCallbackAttribute(self, attribute = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        return getattr(self.callback, attribute)

    def _incrementTickerID(self):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        self.current_ticker_id += 1

    # MAY NOT NEED ANYMORE
    def _addTicker(self, ticker = '', contract = Contract()):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if ticker in self.tickers:
            ticker_id = self.tickers[ticker]
        else:
            ticker_id = self.current_ticker_id
            self.tickers[ticker] = (ticker_id, contract)
            self._incrementTickerID()
        return ticker_id

    def _isInTradingHours(self, yes = True):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if yes:
            return 1
        return 0

    def searchTickers(self, search_object, type_search = '', type_data = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if type_data not in ('ID','CONTRACT','TUPLE'):
            print("Type of data must be 'ID', 'CONTRACT' or 'TUPLE'.")
            return None

        if type_search not in ('TICKER','CONTRACT'):
            print("Type of search must be 'ID' or 'CONTRACT'.")
            return None

        if type_search == 'TICKER':
            return self.tickerSearch(ticker = search_object,
                                        type_data = type_data)

        if type_search == 'CONTRACT':
            return self.contractSearch(contract = search_object,
                                        type_data = type_data)

    def tickerSearch(self, ticker, type_data = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        items = []
        for element in self.tickers:
            if ticker == self.tickers[element][0]:
                if type_data == 'ID':
                    items.append(element)
                if type_data == 'CONTRACT':
                    items.append(self.tickers[element][1])
                if type_data == 'TUPLE':
                    items.append(self.tickers[element])
        return items

    def contractSearch(self, contract, type_data = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        items = []
        for element in self.tickers:
            if contract == self.tickers[element][1]:
                if type_data == 'ID':
                    items.append(element)
                if type_data == 'CONTRACT':
                    items.append(self.tickers[element][1])
                if type_data == 'TUPLE':
                    items.append(self.tickers[element])
        return items

    def removeFromTickers(self, search_object, type_object):
        if type_object not in ('ID','TICKER','CONTRACT'):
            print("Type of data must be 'ID', 'TICKER' or 'CONTRACT'.")
            return None

        if type_object == 'ID':
            del self.tickers[search_object]

        if type_object == 'TICKER':
            ticker_id = self.tickerSearch(ticker = search_object,
                                            type_data = 'ID')
            del self.tickers[ticker_id[0]]

        if type_object == 'CONTRACT':
            ticker_id = self.contractSearch(contract = search_object,
                                            type_data = 'ID')
            del self.tickers[ticker_id[0]]

    def getAccountInformation(self, all_accounts = True, attributes = ','):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
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

        self._resetCallbackAttribute('account_Summary')

        if all_accounts:
            group = "All"
        self.tws.reqAccountSummary(reqId = self.current_request_id,
                                    group = group, tags = attributes)

        time.sleep(1)

        data =  pd.DataFrame(self.callback.account_Summary,
                        columns = ['Request_ID', 'Account', 'Tag', 'Value',
                                    'Curency'])
        return data

    def getDataAtTime(self, data_time, type_data = 'BID_ASK',
                        contract = Contract(), type_time = '',
                        in_trading_hours = False, duration = '60 S',
                        bar_size = '1 min', time_out = 10):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        """
        REQUIRED PARAMETERS:
        data_time
        contract

        type_data:
        TRADES
        MIDPOINT
        BID
        ASK
        BID_ASK
        HISTORICAL_VOLATILITY
        OPTION_IMPLIED_VOLATILITY
        REBATE_RATE	Starting rebate rate
        FEE_RATE
        """

        self._resetCallbackAttribute('historical_Data')

        ticker_id = self._addTicker(ticker = contract.m_symbol)

        if type_time in ('OPEN', 'CLOSE'):
            if type_time == 'OPEN':
                data_time = dt.datetime(year = data_time.year,
                                        month = data_time.month,
                                        day = data_time.day,
                                        hour = 9, minute = 30)
            if type_time == 'CLOSE':
                data_time = dt.datetime(year = data_time.year,
                                        month = data_time.month,
                                        day = data_time.day,
                                        hour = 16)

        trading_hours = self._isInTradingHours(in_trading_hours)

        #could modularize
        now = dt.datetime.now()
        end_wait = now + dt.timedelta(seconds = time_out)

        data = pd.DataFrame(self.callback.historical_Data,
                            columns = ['reqId','date', 'open', 'high', 'low',
                                        'close', 'volume', 'count', 'WAP',
                                        'hasGaps'])
        data_null = data
        while data.equals(data_null) and now <= end_wait:
            self.tws.reqHistoricalData( tickerId = ticker_id,
                                     contract = contract,
                                     endDateTime = (data_time + dt.timedelta(seconds=1)).strftime('%Y%m%d %H:%M:%S'),
                                     durationStr = duration,
                                     barSizeSetting = bar_size,
                                     whatToShow = type_data,
                                     useRTH = trading_hours, formatDate = 1)

            time.sleep(1)
            #end modularize

            #could modularize
            data = pd.DataFrame(self.callback.historical_Data,
                                columns = ['reqId','date', 'open', 'high', 'low',
                                            'close', 'volume', 'count', 'WAP',
                                            'hasGaps'])

            now = dt.datetime.now()

            try:
                data.drop(data.index[-1], inplace=True)
                data['date'] = data['date'].apply(du.parser.parse)
                data.set_index('date', inplace=True)

            except:
                # FIX LOGIC BRANCH, CANNOT RETURN HERE
                print("Error retrieving data for: ", contract.m_symbol,
                        "\nEmpty callback.\nTrying again.")
                time.sleep(15)

        if data.equals(data_null):
            print("Error retrieving data for: ", contract.m_symbol,
                    "\nEmpty callback.\nWait time out.")
            return None

        #end modularize

        #%Y%m%d %H:%M:%S

        #could modularize
        if bar_size.endswith('sec') or bar_size.endswith('secs'):
            index_search_format = '%Y%m%d %H:%M:%S'
        if bar_size.endswith('min') or bar_size.endswith('mins'):
            index_search_format = '%Y%m%d %H:%M:00'
        if bar_size.endswith('hour') or bar_size.endswith('hours'):
            index_search_format = '%Y%m%d %H:00:00'

        #CHECK THE FOLLOWING FOR APPROPRIATE INDEX FORMATS
        if bar_size.endswith('day'):
            index_search_format = '%Y%m%d 00:00:00'
        if bar_size.endswith('week'):
            index_search_format = '%Y%m%d 00:00:00'
        if bar_size.endswith('month'):
            index_search_format = '%Y%m%d 00:00:00'

        #print(data) #TODO:REMOVE

        try:
           return data.loc[data_time.strftime(index_search_format)]
        except:
           print("Index not found problem")
           print(traceback.format_exc)
           return data.iloc[-1]
        #format must be same as bar_size
        #end modularize

    def getDataInRange(self):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        # EXTEND USING getDataAtTime()
        raise NotImplementedError("API method getDataInRange has not been implemented.")
        return None

    def getDailyData(self, stock_list, provider, date_start, date_end = None):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:
            date_start - days will consider from this date to current days
                            market data
            date_end - specify for date range

            TO BE DECIDED:
            return_as_panel = False

        RETURNS:
            data: pandas Panel
                items - <<stock_list>> items
                major axis (rows) - days from <<date_start>> and <<date_end>>
                minor axis (columns) - Open, High, Low, Close, Volume, Adj Close

            data_frame: pandas Dataframe
            Returned when only one item is in the <<stock_list>> or when
            <<return_as_panel>> method parameter is set to <<False>>

        RESULTS:

        """
#        data = pdr.data.DataReader(stock_list, provider, date_start, date_end)
        data = web.DataReader(stock_list, provider, date_start, date_end)
        
        if type(data) == type(pd.DataFrame()):
            return data
        if type(data) == type(pd.Panel()):
            # MORE INFORMATION REGARDING PANDAS PANELS:
            # http://pandas.pydata.org/pandas-docs/stable/dsintro.html#panel

            # if not return_as_panel:
            # data_frame = data.to_frame()
            # return data_frame

            # ASSIGNS ORIGINAL MINOR INDEX (2: <<stock_list>>)
            # TO ITEMS INDEX (0: [stock values])
            data.transpose(2, 1, 0)
            """
            GRAB BY TICKER
            data['ticker']

            GRAB BY DATE
            data.major_xs('%Y-%m%d')

            GRAB BY Value
            data.minor_xs('value')
            """
            return data

    def getLiveMarketData(self, contract = Contract(), time_out = 5):
        """
        genericTickList options:
        100 Option Volume (currently for stocks)
        101 Option Open Interest (currently for stocks)
        104 Historical Volatility (currently for stocks)
        106 Option Implied Volatility (currently for stocks)
        162 Index Future Premium
        165 Miscellaneous Stats
        221 Mark Price (used in TWS P&L computations)
        225 Auction values (volume, price and imbalance)
        233 RTVolume - contains the last trade price, last trade size, last trade time, total volume, VWAP, and single trade flag.
        236 Shortable
        256 Inventory
        258 Fundamental Ratios
        411 Realtime Historical Volatility
        456 IBDividends
        """
        tick_type = {0 : "BID SIZE",
                        1 : "BID PRICE",
                        2 : "ASK PRICE",
                        3 : "ASK SIZE",
                        4 : "LAST PRICE",
                        5 : "LAST SIZE",
                        6 : "HIGH",
                        7 : "LOW",
                        8 : "VOLUME",
                        9 : "CLOSE PRICE",
                        10 : "BID OPTION COMPUTATION",
                        11 : "ASK OPTION COMPUTATION",
                        12 : "LAST OPTION COMPUTATION",
                        13 : "MODEL OPTION COMPUTATION",
                        14 : "OPEN_TICK",
                        15 : "LOW 13 WEEK",
                        16 : "HIGH 13 WEEK",
                        17 : "LOW 26 WEEK",
                        18 : "HIGH 26 WEEK",
                        19 : "LOW 52 WEEK",
                        20 : "HIGH 52 WEEK",
                        21 : "AVG VOLUME",
                        22 : "OPEN INTEREST",
                        23 : "OPTION HISTORICAL VOL",
                        24 : "OPTION IMPLIED VOL",
                        27 : "OPTION CALL OPEN INTEREST",
                        28 : "OPTION PUT OPEN INTEREST",
                        29 : "OPTION CALL VOLUME"}

        """
        self.tickers = contract

        ticker_id = self.searchTickers(search_object = contract,
                                        type_search = 'CONTRACT',
                                        type_data = 'ID')[0]
        """
        self.tickers = contract
        
        ticker_id = self.searchTickers(search_object = contract,
                                type_search = 'CONTRACT',
                                type_data = 'ID')[0]

#        ticker_id = 1 # SOME SORT OF INCREMENTAL VALUE

        self._resetCallbackAttribute('tick_Price')
        data = pd.DataFrame(self.callback.tick_Price,
                            columns = ['tickerId', 'field', 'price',
                                        'canAutoExecute'])
        data_null = data

        now = dt.datetime.now()
        end_wait = now + dt.timedelta(seconds = time_out)

        while data.equals(data_null) and now <= end_wait:

            self.tws.reqMktData(tickerId = ticker_id, contract = contract,
                                genericTickList = '', snapshot = True)

            time.sleep(1)

            data = pd.DataFrame(self.callback.tick_Price,
                                columns = ['tickerId', 'field', 'price',
                                            'canAutoExecute'])

            now = dt.datetime.now()

        if data.equals(data_null):
            print("Error retrieving data for: ", contract.m_symbol, ':',
                    contract, "\nEmpty callback.\nWait time out.")

            self.removeFromTickers(search_object = contract,
                                    type_object = 'CONTRACT')
            return None

        data["Type"] = data["field"].map(tick_type)

        return data

    def getPositions(self):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        self._resetCallbackAttribute('update_Position')

        self.tws.reqPositions()

        time.sleep(1)

        data = pd.DataFrame(self.callback.update_Position,
                            columns = ['Account_Name', 'Contract_Id',
                                        'Currency', 'Exchange', 'Expiry',
                                        'Include_Expired', 'Local_Symbol',
                                        'Multiplier', 'Right',
                                        'Financial_Instrument', 'Strike_Price',
                                        'Symbol', 'Trading_Class',
                                        'Number_of_Units',
                                        'Average_Unit_Price'])
        data.set_index(keys = ['Contract_Id'], inplace = True)
        return data

    # TODO: CHECK IF IT IS POSSIBLE TO ACQUIRE PAST PORTFOLIO VALUES
    def getPortfolio(self):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        self._resetCallbackAttribute('update_Portfolio')

        self.tws.reqAccountUpdates(True, self.account_name)

        time.sleep(1)
        """
        VALUE WAIT ALTERNATIVE TO TIME WAIT:
        def acctUp():
        ib._resetCallbackAttribute('update_Portfolio')
        ib.tws.reqAccountUpdates(True, 'DU550479')
        updated = ib.callback.accountDownloadEnd_flag
        while not updated:
                updated = ib.callback.accountDownloadEnd_flag
        print pd.DataFrame(ib.callback.update_Portfolio)
        ib.tws.reqAccountUpdates(False, 'DU550479')
        """

        self.tws.reqAccountUpdates(False, self.account_name)

        portfolio = pd.DataFrame(self.callback.update_Portfolio,
                                    columns = ['Contract_ID', 'Currency',
                                                'Expiry', 'Include_Expired',
                                                'Local_Symbol', 'Multiplier',
                                                'Primary_Exchange', 'Right',
                                                'Security_Type', 'Strike',
                                                'Symbol', 'Trading_Class',
                                                'Position', 'Market_Price',
                                                'Market_Value', 'Average_Cost',
                                                'Unrealized_PnL',
                                                'Realized_PnL', 'Account_Name'])
        return portfolio

    def getExecutedOrders(self, contract = Contract(), since = None):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if since == None:
            execution_filter = self.createExecutionFilter(contract = contract)
        else:
            execution_filter = self.createExecutionFilter(contract = contract,
                                                            order_time = since)

        self.tws.reqExecutions(1, execution_filter) # TODO: check if request_id is valid and static

        time.sleep(1)

        execution_contract = self.callback.exec_Details_contract.__dict__
        execution_details = self.callback.exec_Details_execution.__dict__
        execution = dict(execution_contract, **execution_details)

        data = pd.DataFrame.from_dict([execution])
        data.rename(columns = {'m_acctNumber': 'Account_Name',
                                'm_avgPrice': 'Average_Unit_Price',
                                'm_clientId': 'Client_ID',
                                'm_conId': 'Contract_ID',
                                'm_cumQty': 'Cumulative_Quantity',
                                'm_currency': 'Currency',
                                'm_evMultiplier': 'Economic_Value_Multiplier',
                                'm_evRule': 'Economic_Value_Rule',
                                'm_exchange': 'Exchange',
                                'm_execId': 'Execution_ID',
                                'm_expiry': 'Expiry',
                                'm_includeExpired': 'Include_Expired',
                                'm_liquidation': 'Liquidation',
                                'm_localSymbol': 'Local_Symbol',
                                'm_multiplier': 'Multiplier',
                                'm_orderId': 'Order_ID',
                                'm_orderRef': 'Order_Reference',
                                'm_permId': 'Permanent_ID',
                                'm_price': 'Price',
                                'm_right': 'Right',
                                'm_secType': 'Financial_Instrument',
                                'm_shares': 'Shares',
                                'm_side': 'Side',
                                'm_strike': 'Strike',
                                'm_symbol': 'Ticker',
                                'm_time': 'Server_Time',
                                'm_tradingClass':'Trading_Class'},
                    inplace = True)

        #self._resetCallbackAttribute('exec_Details_contract')
        #self._resetCallbackAttribute('exec_Details_execution')

        return data

    # TODO: MAKE RECORD AND GETTING STRATEGY SPECIFIC; STRATEGY PNL NOT RECORDED
    # ONLY ACCOUNT WIDE PNL
    # TODO: CHECK IF IT IS POSSIBLE TO ACQUIRE PAST PORTFOLIO VALUES
    def getPNLToday(self):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        portfolio = self.getPortfolio()

        PNL = portfolio.loc[:, ['Date', 'Contract_ID', 'Symbol',
                                'Market_Value', 'Market_Price', 'Position',
                                'Unrealized_PnL', 'Realized_PnL']]

        PNL.loc[:,['Date']] = dt.date.today()

        return PNL

    # TODO: MAKE RECORD AND GETTING STRATEGY SPECIFIC; STRATEGY PNL NOT RECORDED
    # ONLY ACCOUNT WIDE PNL
    def recordPNLToday(self, path = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        # TODO: always write a new file
        PNL = self.getPNLToday()

        PNL.to_csv(path_or_buf = path, encoding = 'utf-8', mode = 'w+')

    def recordPNLDailyPerformance(self, path = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        # TODO: append to an existing file if it exists
        PNL = self.getPNLToday()

        # TODO: sum positions to one record
        PNL_day = pd.DataFrame(index = [0])
        PNL_day['Date'] = PNL['Date'].max()
        PNL_day['Unrealized_PnL'] = PNL['Unrealized_PnL'].sum()
        PNL_day['Realized_PnL'] = PNL['Realized_PnL'].sum()

        if dr.checkPath(path = path):
            header = None
            PNL_day.to_csv(path_or_buf=path, encoding='utf-8', mode='a+',
                           header=header)
            return

        PNL_day.to_csv(path_or_buf = path, encoding = 'utf-8', mode = 'a+')

    def recordTransaction(self, contract, path = '', additional_values = {}):
        order_details = self.getExecutedOrder(contract)

        if additional_values:
            additional_details = pd.DataFrame.from_dict([additional_values])
            transaction_details = pd.concat([order_details,additional_details],
                                            axis = 1)
            transaction_details.to_csv(path_or_buf = path, encoding = 'utf-8',
                                       mode = 'a+', header = None,
                                       index_label=['Server_Time'])

        order_details.to_csv(path_or_buf = path, encoding = 'utf-8',
                             mode = 'a+', header = None,
                             index_label = ['Server_Time'])

class ExecutionBroker(Broker):
    """docstring for ExecutionBroker."""
    def __init__(self, **kw):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        super(ExecutionBroker, self).__init__()

class IBExecutionBroker(IBBroker, ExecutionBroker):
    """docstring for IBExecutionBroker."""
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, **kw):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
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
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        self.tws.placeOrder(order_id, contract, order)

    def cancelOrder(self, order_id):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        """
        ORDER TYPES:
        Limit	LMT
        Limit Risk
        Bracket
        Market-to-Limit	MTL
        Market with Protection	MKT PRT
        Request for Quote	QUOTE
        Stop	STP
        Stop Limit	STP LMT
        Trailing Limit if Touched	TRAIL LIT
        Trailing Market If Touched	TRAIL MIT
        Trailing Stop	TRAIL
        Trailing Stop Limit	TRAIL LIMIT
        Speed of Execution
        At Auction
        Discretionary
        Market	MKT
        Market-if-Touched	MIT
        Market-on-Close	MOC
        Market-on-Open	MOO
        Pegged-to-Market	PEG MKT
        Relative	REL
        Sweep-to-Fill
        Price Improvement
        Box Top	BOX TOP
        Price Improvement Auction
        Block
        Limit-on-Close	LOC
        Limit-on-Open	LOO
        Limit if Touched	LIT
        Pegged-to-Midpoint	PEG MID
        Privacy
        Hidden
        Iceberg/Reserve
        VWAP - Guaranteed	VWAP
        Time to Market
        All-or-None
        Fill-or-Kill
        Good-after-Time/Date	GAT
        Good-till-Date/Time	GTD
        Good-till-Canceled	GTC
        Immediate-or-Cancel	IOC
        Advanced Trading
        One-Cancels-All	OCA
        Spreads
        Volatility	VOL
        Algorithmic Trading (Algos)
        Arrival Price
        Balance Impact and Risk
        Minimize Impact
        Percent of volume
        Scale
        TWAP
        VWAP - Best Effort
        Accumulate/Distribute
        IBDARK
        """
        self.tws.cancelOrder(order_id)

class IBBrokerTotal(IBExecutionBroker, IBDataBroker):
    """docstring for IBBrokerTotal."""
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, path_root = '/'):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        """
        IBBrokerTotal constructor.
        Initializes object properties.
        Combines functionalties of <IBExecutionBroker> and <IBDataBroker>.

        PARAMETERS:
        account_name -
        host -
        port -
        client_id -
        path_root -
        """
        super(IBBrokerTotal, self).__init__(account_name = account_name,
                                            host = host, port = port,
                                            client_id = client_id,
                                            path_root = path_root)

    def closeAllPositions(self, order_type = '', exclude_symbol = [''],
                            exclude_instrument = ['']):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if order_type not in ('LIMIT', 'MARKET','MOC'):
            print("Given order_type is not a proper type.")
            return None

        positions = self.getPositions()

        order_id = self.nextOrderId()
        for position_record in positions.iterrows():
            position_details = position_record[1]

            ticker = position_details['Symbol']
            if ticker in exclude_symbol:
                continue

            instrument_type = position_details['Financial_Instrument']
            if instrument_type in exclude_instrument:
                continue

            contract = self.createContract(ticker = ticker,
                                            instrument_type = instrument_type,
                                            exchange = 'SMART',
                                            currency = 'USD')
            # Make new contract? or is there some way to access previous contracts?

            direction = position_details['Number_of_Units']
            amount_units = int(abs(direction))
            price_per_unit = float(position_details['Average_Unit_Price'])

            if direction < 0:
                trade_type = 'BUY'
            elif direction > 0:
                trade_type = 'SELL'
            elif direction == 0:
                print(str(ticker) + ": Position is already closed.")
                continue

            order = self.createOrder(trade_type = trade_type,
                                        amount_units = amount_units,
                                        price_per_unit = price_per_unit,
                                        order_type = order_type)

            self.placeOrder(order_id = order_id, contract = contract, order = order)
            time.sleep(1)

            order_id += 1

    def closeAllTypePositions(self, order_type = '', instruments = [''],
                                exclude_symbol = ['']):
        if order_type not in ('LIMIT', 'MARKET', 'MOC'):
            print("Given order_type is not a proper type.")
            return None

        positions = self.getPositions()

        order_id = self.nextOrderId()
        for position_record in positions.iterrows():
            position_details = position_record[1]

            ticker = position_details['Symbol']
            if ticker in exclude_symbol:
                continue

            instrument_type = position_details['Financial_Instrument']
            if instrument_type not in instruments:
                continue

            contract = self.createContract(ticker = ticker,
                                            instrument_type = instrument_type,
                                            exchange = 'SMART',
                                            currency = 'USD')
            # Make new contract? or is there some way to access previous contracts?

            direction = position_details['Number_of_Units']
            amount_units = int(abs(direction))
            price_per_unit = float(position_details['Average_Unit_Price'])

            if direction < 0:
                trade_type = 'BUY'
            elif direction > 0:
                trade_type = 'SELL'
            elif direction == 0:
                print(str(ticker) + ": Position is already closed.")
                continue

            order = self.createOrder(trade_type = trade_type,
                                        amount_units = amount_units,
                                        price_per_unit = price_per_unit,
                                        order_type = order_type)

            self.placeOrder(order_id = order_id, contract = contract, order = order)
            time.sleep(1)

            order_id += 1

    def closeAllNamePositions(self, order_type = '', tickers = ['']):
        if order_type not in ('LIMIT', 'MARKET', 'MOC'):
            print("Given order_type is not a proper type.")
            return None

        positions = self.getPositions()

        order_id = self.nextOrderId()
        for position_record in positions.iterrows():
            position_details = position_record[1]

            ticker = position_details['Symbol']
            if ticker not in tickers:
                continue

            instrument_type = position_details['Financial_Instrument']

            contract = self.createContract(ticker = ticker,
                                            instrument_type = instrument_type,
                                            exchange = 'SMART',
                                            currency = 'USD')
            # Make new contract? or is there some way to access previous contracts?

            direction = position_details['Number_of_Units']
            amount_units = int(abs(direction))
            price_per_unit = float(position_details['Average_Unit_Price'])

            if direction < 0:
                trade_type = 'BUY'
            elif direction > 0:
                trade_type = 'SELL'
            elif direction == 0:
                print(str(ticker) + ": Position is already closed.")
                continue

            order = self.createOrder(trade_type = trade_type,
                                        amount_units = amount_units,
                                        price_per_unit = price_per_unit,
                                        order_type = order_type)

            self.placeOrder(order_id = order_id, contract = contract, order = order)
            time.sleep(1)

            order_id += 1

    def closePosition(self, symbol = '', order_type = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if order_type not in ('LIMIT', 'MARKET', 'MOC'):
            print("Given order_type is not a proper type.")
            return None

        order_id = self.nextOrderId()

        positions = self.getPositions()

        try:
            position_details = positions.loc[positions.loc[:,'Symbol'] == symbol]
        except:
            print("Ticker was not found in positions.")
            return None
        if(position_details.empty):
            return None
        ticker = position_details['Symbol'].iloc[0]
        instrument_type = position_details['Financial_Instrument'].iloc[0]

        contract = self.createContract(ticker = ticker,
                                        instrument_type = instrument_type,
                                        exchange = 'SMART',
                                        currency = 'USD')

        direction = position_details['Number_of_Units'].iloc[0]
        amount_units = int(abs(direction))
        price_per_unit = float(position_details['Average_Unit_Price'].iloc[0])

        if direction < 0:
            trade_type = 'BUY'
        elif direction > 0:
            trade_type = 'SELL'
        else:
            print("Position is already closed.")
            return None

        order = self.createOrder(trade_type = trade_type,
                                    amount_units = amount_units,
                                    price_per_unit = price_per_unit,
                                    order_type = order_type)

        self.placeOrder(order_id = order_id, contract = contract, order = order)
        time.sleep(1)

    def _totalDollarToTotalUnits(self, amount_dollars, contract,
                                    data_time = None):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        if data_time == None:
            data_time = dt.datetime.now()

#        data_contract = self.getDataAtTime(data_time = data_time,
#                                            contract = contract,
#                                            bar_size = '1 secs')
#        
        
#        liveData = self.broker.getLiveMarketData( contract= contract )
        liveData = self.getLiveMarketData( contract= contract )
        askPrice = liveData['price'][ liveData['Type']=='ASK PRICE' ].values[0]            
        bidPrice = liveData['price'][ liveData['Type']=='BID PRICE' ].values[0]         
            
        price_per_unit = ( askPrice +bidPrice )*0.5 #mid point
        
#       price_per_unit = data_contract['open'].iloc[-1]
        return int(amount_dollars / price_per_unit)

    def createDollarOrder(self, amount_dollars, contract, trade_type,
                            price_per_unit = 0.0, order_type = ''):
        """
        METHOD SUMMARY
        METHOD DESCRIPTION

        PARAMETERS:

        RETURNS:

        RESULTS:

        """
        amount_units = self._totalDollarToTotalUnits(amount_dollars = amount_dollars,
                                                    contract = contract)

        order = self.createOrder(trade_type = trade_type,
                                    amount_units = amount_units,
                                    price_per_unit = price_per_unit,
                                    order_type = order_type)
        return order

    def placeRecordedOrder(self, order_id, contract, order, path = '',
                           additional_values = {}):
        """
        placeRecordedOrder:
        Places an [order] on the [#Interactive Brokers server] and records the
        transaction.
        
        PARAMETERS:
        order_id - 
        contract - 
        order - 
        path - 
        additional_values - 
        
        RETURNS:
        None
        
        RESULTS:
        Creates a local record of an [executed order] at the <<path>> location.
        """
        self.tws.placeOrder(order_id, contract, order)
        return self.recordTransaction(contract=contract, path=path,
                                      additional_values=additional_values)

    def getLiveMidPriceData(self, contract):
        """
        getLiveMidPriceData:
        Method summary
        
        PARAMETERS:
        None
        
        RETURNS:
        None
        
        RESULTS:
        None
        """
        
        liveData = self.getLiveMarketData(contract)

        askPrice = liveData['price'][liveData['Type'] == 'ASK PRICE'].values[0]
        bidPrice = liveData['price'][liveData['Type'] == 'BID PRICE'].values[0]

        midPrice = (askPrice + bidPrice) * 0.5  # mid point
        return midPrice