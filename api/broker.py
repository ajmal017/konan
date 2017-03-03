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
import dateutil as du
import glob
import fnmatch

# third party imports
import pandas as pd
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
import data
import position

class BrokerConnection(object):
    """
    Connection resource to be shared by brokers in a sytem's public environment
    without disrupting properties of the connection.
    E.g. connection status, object representation.
    """

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self):
        """
        Basic BrokerConnection constructor
        """
        super(BrokerConnection, self).__init__()

class IBBrokerConnection(BrokerConnection):
    """
    Connection interface implementing the Interactive Brokers (IB)
    EClientSocket API behaviours. Allows the EClientSocket object to be shared.
    """

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, callback = IBWrapper()):
        """
        IBBrokerConnection constructor.
        Initializes object properties.

        SIGNATURE:
        callback - IBWrapper()
            Implementation of an abstract class in the Interactive Brokers (IB)
            API which stores the results of API calls
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

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self):
        """
        Broker constructor.
        Initializes object properties.

        SIGNATURE:
        """
        super(Broker, self).__init__()

class IBBroker(Broker):
    """
    docstring for IBBroker.
    """

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, account_name = 'DU603835',
                    connection = IBBrokerConnection(), host = '', port = 7497,
                    client_id = 100, **kw):
        """
        Broker constructor.
        Initializes object properties.

        SIGNATURE:
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
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """
    def connect(self):
        self.tws.eConnect(self.host, self.port, self.client_id)

    def disconnect(self):
        self.tws.eDisconnect()

    def connected(self):
        return self.tws.isConnected()

    def nextOrderId(self):
        self.tws.reqIds(1)
        return self.callback.next_ValidId

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

    def createOrder(self, trade_type, amount_units, price_per_unit = 0.0,
                    order_type = '', time_in_force = 'GTC'):
        if order_type not in ('LIMIT', 'MARKET'):
            print("Given order_type is not a proper type.")
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

        return order

    def preparePosition(self, position = position.Position()):
        """Unpack position object into order and contracts"""
        return None

class DataBroker(Broker):
    """docstring for DataBroker."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, path_root = '/', project = '', data_file = '', **kw):
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
        files = glob.iglob(path_data + '*.' + type_data)
        while True:
            f = files.next()
            if fnmatch.fnmatch(f, '*' + file_name + '.' + type_data):
                return f
        return ''

class IBDataBroker(IBBroker, DataBroker):
    """docstring for IBDataBroker."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, path_root = '/', **kw):
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
        def fset(self, value):
            print("add to dictionary")#self._tickers = value
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

    def _incrementTickerID(self):
        self.current_ticker_id +=1

    def _addTicker(self, ticker = ''):
        if ticker in self.tickers:
            ticker_id = self.tickers[ticker]
        else:
            ticker_id = self.current_ticker_id
            self.tickers[ticker] = ticker_id
            self._incrementTickerID()
        return ticker_id

    def _isInTradingHours(self, yes = True):
        if yes:
            return 1
        return 0

    def getCallbackAttribute(self, attribute = ''):
        return getattr(self.callback, attribute)

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

        self._resetCallbackAttribute('account_Summary')

        if all_accounts:
            group = "All"
        self.tws.reqAccountSummary(reqId = self.current_request_id,
                                    group = group, tags = attributes)
        return pd.DataFrame(self.callback.account_Summary,
                        columns = ['Request_ID', 'Account', 'Tag', 'Value',
                                    'Curency'])

    def getDataAtTime(self, data_time, type_data = 'BID_ASK',
                        contract = Contract(), type_time = '',
                        in_trading_hours = False, duration = '60 S',
                        bar_size = '1 min'):
        """
        REQUIRED PARAMETERS:
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

        data.drop(data.index[-1], inplace=True)
        data['date'] = data['date'].apply(du.parser.parse)
        data.set_index('date', inplace=True)
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

        return data.loc[data_time.strftime(index_search_format)]
        #format must be same as bar_size
        #end modularize

    def getDataInRange(self):
        # EXTEND USING getDataAtTime()
        return pd.DataFrame()

    """
    def getLiveMarketData(self):
        self.tws.reqMktData()
        return self.callback.tick_Price
    """

    def getPositions(self):

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

class ExecutionBroker(Broker):
    """docstring for ExecutionBroker."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, **kw):
        super(ExecutionBroker, self).__init__()

class IBExecutionBroker(IBBroker, ExecutionBroker):
    """docstring for IBExecutionBroker."""

    """
    CLASS CONSTRUCTOR
    """
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, **kw):
        """
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
        self.tws.placeOrder(order_id, contract, order)

    def cancelOrder(self, order_id):
        self.tws.cancelOrder(order_id)

class IBBrokerTotal(IBExecutionBroker, IBDataBroker):
    """docstring for IBBrokerTotal."""
    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, path_root = '/'):
        """
        IBBrokerTotal constructor.
        Initializes object properties.
        Combines functionalties of <IBExecutionBroker> and <IBDataBroker>.

        SIGNATURE:
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

    def closeAllPositions(self, order_type = ''):
        if order_type not in ('LIMIT', 'MARKET'):
            print("Given order_type is not a proper type.")
            return None

        positions = self.getPositions()

        order_id = self.nextOrderId()
        for position_record in positions.iterrows():
            position_details = position_record[1]

            ticker = position_details['Symbol']
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
        if order_type not in ('LIMIT', 'MARKET'):
            print("Given order_type is not a proper type.")
            return None

        order_id = self.nextOrderId()

        positions = self.getPositions()

        try:
            position_details = positions.loc[positions.loc[:,'Symbol'] == symbol]
        except:
            print("Ticker was not found in positions.")
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

    def _totalPriceToTotalUnits(self, amount_price, contract):
        data_contract = self.getDataAtTime(data_time = dt.datetime.now(),
                                            contract = contract)
        price_per_unit = data_contract['open'].iloc[-1]
        return int(amount_price / price_per_unit)

    def createPriceOrder(self, amount_price, contract, trade_type,
                            price_per_unit = 0.0, order_type = ''):
        amount_units = self._totalPriceToTotalUnits(amount_price = amount_price,
                                                    contract = contract)

        order = self.createOrder(trade_type = trade_type,
                                    amount_units = amount_units,
                                    price_per_unit = price_per_unit,
                                    order_type = order_type)
        return order
