#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# api.broker.py
# Created on 2017-02-14T16:36:00Z
# @author:jsrhu
# @author:Joshua Hu

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
import data as dat
import position as pos


class BrokerConnection(object):
    """
    CLASS SUMMARY:
        Connection resource to be shared by brokers in a system's public
        environment without disrupting properties of the connection.
        E.g. connection status, object representation.

    CLASS PROPERTIES:
        None

    CLASS SPECIAL METHODS:
        None

    CLASS PRIVATE METHODS:
        None

    CLASS PUBLIC METHODS:
        None
    """
    def __init__(self):
        """
        SUMMARY:
            Basic BrokerConnection initializer. Initializes object properties.
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            Creates BrokerConnection object.
        """
        super(BrokerConnection, self).__init__()

    """
    CLASS PROPERTIES
    """

    """
    CLASS SPECIAL METHODS
    """

    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """

class IBBrokerConnection(BrokerConnection):
    """
    CLASS SUMMARY:
        Connection interface implementing the Interactive Brokers (IB)
        EClientSocket API behaviours. Allows the EClientSocket object
        to be shared.
    
    CLASS PROPERTIES:
        interface:
            EClientSocket object that takes in the implemented IBWrapper class in which
            API calls are stored.

    CLASS SPECIAL METHODS:
        None
    
    CLASS PRIVATE METHODS:
        None
    
    CLASS PUBLIC METHODS:
        None
    """
    def __init__(self, callback = IBWrapper()):
        """
        SUMMARY:
            IBBrokerConnection initializer. Initializes object properties.
        
        PARAMETERS:
            callback - IBWrapper()
                Implementation of an abstract class in the
                Interactive Brokers (IB) API which stores the results of
                API calls
        
        RETURNS:
            None
        
        RESULTS:
            Creates IBBrokerConnection object.
        """
        super(IBBrokerConnection, self).__init__()
        self._interface = EClientSocket(callback)

    """
    CLASS PROPERTIES
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

    """
    CLASS SPECIAL METHODS
    """

    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """


class Broker(object):
    """
    CLASS SUMMARY:
        Parent template for <Broker> type objects.

    CLASS PROPERTIES:
        None

    CLASS SPECIAL METHODS:
        None

    CLASS PRIVATE METHODS:
        None

    CLASS PUBLIC METHODS:
        None
    """
    def __init__(self):
        """
        SUMMARY:
            Broker initializer. Initializes object properties.

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            Creates a <Broker> object.
        """
        super(Broker, self).__init__()

    """
    CLASS PROPERTIES
    """

    """
    CLASS SPECIAL METHODS
    """

    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """


class IBBroker(Broker):
    """
    CLASS SUMMARY:
        Interactive Brokers <Broker> interface object.

    CLASS PROPERTIES:
        account_name -
        callback -
        connection -
        tws -
        host -
        port -
        client_id -
        current_order_id -

    CLASS SPECIAL METHODS:
        __str__ -

    CLASS PRIVATE METHODS:
        _createStockContract -
        _createOptionContract -
        _createFutureContract -
        _createIndexContract -
        _createStockCashContract -
        _createCombinationContract -
        _createWarrantContract -
        _createBondContract -
        _createCommodityContract -
        _createNewsContract -
        _createMutualFundContract -

    CLASS PUBLIC METHODS:
        connect -
        disconnect -
        connected -
        nextOrderId -
        createContract -
        createOrder -
        preparePosition -
        createExecutionFilter -
    """
    def __init__(self, account_name = 'DU603835',
                    connection = IBBrokerConnection(), host = '', port = 7497,
                    client_id = 100, **kwargs):
        """
        SUMMARY:
            Broker initializer. Initializes object properties.

        PARAMETERS:
            account_name - string
                The name of the Interactive Brokers account represented as a
                string.
            connection - IBBrokerConnection()
                The connection object for the broker.
            host -
            port -
            client_id -
            
        RETURNS:
            None
            
        RESULTS:
            Creates an <IBBroker> object.
        """
        super(IBBroker, self).__init__(**kwargs)
        self._account_name = account_name

        self._callback = IBWrapper()
        self.callback.initiate_variables()

        self._connection = IBBrokerConnection(self.callback)

        self._tws = self.connection.interface #could just assign to _connection

        self._host = host
        self._port = port
        self._client_id = client_id

        self.connect()

    """
    CLASS PROPERTIES
    """
    def account_name():
        doc = "The unique Interactive Brokers account name."
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

    def current_order_id():
        doc = "The current_order_id property."
        def fget(self):
            return self._current_order_id
        def fset(self, value):
            self._current_order_id = value
        def fdel(self):
            del self._current_order_id
        return locals()
    current_order_id = property(**current_order_id())

    """
    CLASS SPECIAL METHODS
    """
    def __str__(self):
        return "Account Name:{} on Port:{} with Client ID:{} ".format(self.account_name, self.client_id, self.port)

    """
    CLASS PRIVATE METHODS
    """
    # MAY NOT NEED ANY; SEE <createContract>
    def _createStockContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        return contract

    def _createOptionContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        # The contract's last trading day or contract month
        # (for Options and Futures).
        # Strings with format YYYYMM will be interpreted as the Contract Month
        # whereas YYYYMMDD will be interpreted as Last Trading Day.
        contract.m_lastTradeDateOrContractMonth = last_trade_date
        contract.m_expiry = expiry  # is this the same as last_trade_date ?

        # The option's strike price.
        contract.m_strike = strike_price

        # Either Put or Call (i.e. Options). Valid values are P, PUT, C, CALL.
        contract.m_right = right

        # The instrument's multiplier (i.e. options, futures).
        contract.m_multiplier = multiplier
        return contract

    def _createFutureContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        # The contract's last trading day or contract month
        # (for Options and Futures).
        # Strings with format YYYYMM will be interpreted as the Contract Month
        # whereas YYYYMMDD will be interpreted as Last Trading Day.

        #        contract.m_expiry = expiry # is this the same as last_trade_date ?

        # The instrument's multiplier (i.e. options, futures).
        #        contract.m_multiplier = multiplier
        return contract

    def _createIndexContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        return contract

    def _createCashContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        return contract

    def _createCombinationContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        return contract

    def _createWarrantContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        return contract

    def _createBondContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        return contract

    def _createCommodityContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        return contract

    def _createNewsContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        return contract

    def _createMutualFundContract(self, contract=Contract()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        return contract

    """
    CLASS PUBLIC METHODS
    """
    def connect(self):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        if self.connected():
            print('Broker is already connected.')
            pass
        self.tws.eConnect(self.host, self.port, self.client_id)

    def disconnect(self):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        self.tws.eDisconnect()

    def connected(self):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        return self.tws.isConnected()

    def nextOrderId(self, from_IB = False, from_datetime = True):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        if from_IB:
            self.tws.reqIds(1)
            id = self.callback.next_ValidId
            self.current_order_id = id + 1
            return id
        if from_datetime:
            now = dt.datetime.now()
            strID = "".join((str('{:02d}'.format(now.day)),
                             str('{:02d}'.format(now.hour)),
                             str('{:02d}'.format(now.minute)),
                             str('{:02d}'.format(now.second)),
                             str('{:02d}'.format(now.microsecond)[:1])))
            id = int(strID)
            self.current_order_id = id + 1
            return id

        id = self.current_order_id
        self.current_order_id += 1
        return id

    def createContract(self, ticker, instrument_type,
                       exchange='SMART', currency='USD',
                       last_trade_date=None, expiry=None,
                       strike_price=None, right=None, multiplier=None,
                       primary_exchange_ticker=None, primary_exchange=None,
                       trading_class=None, include_expired=None,
                       secId_type=None, secId=None,
                       combo_legs_description=None, combo_legs=None,
                       under_comp=None, localSymbol=None
                       ):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        # TODO: IMPLEMENT CONTRACT LOGIC FOR ALL CASES
        # possibly use private methods commented out
        contract = Contract()

        # The unique IB contract identifier.
        # contract.m_conId = contract_id

        # The underlying's asset symbol.
        contract.m_symbol = ticker

        # The security's type: STK - stock (or ETF) OPT - option FUT - future
        # IND - index FOP - futures option CASH - forex pair BAG - combo
        # WAR - warrant BOND- bond CMDTY- commodity NEWS- news FUND- mutual fund.
        contract.m_secType = instrument_type

        # The destination exchange.
        contract.m_exchange = exchange

        # The underlying's currency.
        contract.m_currency = currency

        contract.m_primaryExch = primary_exchange

        ''' Futures '''
        contract.m_multiplier = multiplier
        contract.m_expiry = expiry
        contract.m_localSymbol = localSymbol
        contract.m_includeExpired = include_expired

        ''' Others '''
        contract.m_comboLegs = combo_legs
        contract.m_comboLegsDescrip = combo_legs_description
        contract.m_lastTradeDateOrContractMonth = last_trade_date
        contract.m_strike = strike_price
        contract.m_right = right
        contract.m_localSymbol = primary_exchange_ticker
        contract.m_tradingClass = trading_class
        contract.m_secId = secId
        contract.m_secIdType = secId_type
        contract.m_underComp = under_comp

        """
        The contract's symbol within its primary exchange.
        contract.m_localSymbol = primary_exchange_ticker

        The contract's primary exchange.
        contract.m_primaryExch = primary_exchange

        The trading class name for this contract.
        Available in TWS contract description window as well.
        For example, GBL Dec '13 future's trading class is "FGBL".
        contract.m_tradingClass = trading_class

        If set to true, contract details requests and historical data queries
        can be performed pertaining to expired contracts.
        Note: Historical data queries on expired contracts are limited to
        the last year of the contracts life, and are initially only supported
        for expired futures contracts.
        contract.m_includeExpired = include_expired

        Security's identifier when querying contract's details
        or placing orders SIN - Example: Apple: US0378331005 CUSIP
        - Example: Apple: 037833100 SEDOL - Consists of 6-AN + check digit.
        Example: BAE: 0263494 RIC - Consists of exchange-independent RIC Root
        and a suffix identifying the exchange.
        Example: AAPL.O for Apple on NASDAQ.
        contract.m_secIdType = secIdType

        Identifier of the security type.
        contract.m_secId = secId

        Description of the combo legs.
        contract.m_comboLegsDescription = combo_legs_description

        The legs of a combined contract definition.
        contract.m_comboLegs = combo_legs

        Delta and underlying price for Delta-Neutral combo orders.
        Underlying (STK or FUT), delta and underlying price
        goes into this attribute.
        contract.m_underComp = under_comp
        """

        """
        # DO NOT REMOVE: POSSIBLE FUTURE USE WITH SPECIFIC CASES
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
        """
        return contract

    def createOrder(self, trade_type, amount_units, price_per_unit = 0.0,
                    total_price = 0.0, order_type = '', time_in_force = None,
                    solicited = None):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
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

        # TODO: implement function dictionary similar to <createContract>
        # https://interactivebrokers.github.io/tws-api/basic_orders.html#gsc.tab=0
        # What are the possible values of trade_types 
        
        if order_type == 'LIMIT':
            order.m_orderType = 'LMT'
            order.m_lmtPrice = price_per_unit * amount_units
        elif order_type == 'MARKET':
            order.m_orderType = 'MKT'
        else:
            order.m_orderType = order_type

        if order_type in ('MTL', 'MKT', 'LMT'):
            """
            DAY - Valid for the day only.
            GTC - Good until canceled.
                The order will continue to work within the system and in the
                marketplace until it executes or is canceled.
                GTC orders will be automatically be cancelled under the
                following conditions:
                    If a corporate action on a security results in a stock split
                    (forward or reverse), exchange for shares, or
                    distribution of shares.
                    If you do not log into your IB account for 90 days.
                    At the end of the calendar quarter following thecurrent quarter.
                        For example, an order placed during the third quarter of
                        2011 will be canceled at the end of the first quarter
                        of 2012.
                    If the last day is a non-trading day, the cancellation will
                    occur at the close of the final trading day of that quarter.
                        For example, if the last day of the quarter is Sunday,
                        the orders will be cancelled on the preceding Friday.
                Orders that are modified will be assigned a new "Auto Expire"
                date consistent with the end of the calendar quarter
                following the current quarter.
                Orders submitted to IB that remain in force for more than
                one day will not be reduced for dividends. To allow adjustment
                to your order price on ex-dividend date, consider using a
                Good-Til-Date/Time (GTD) or Good-after-Time/Date (GAT)
                order type, or a combination of the two.
            IOC - Immediate or Cancel. Any portion that is not filled as soon as it becomes available in the market is canceled.
            GTD - Good until Date. It will remain working within the system and in the marketplace until it executes or until the close of the market on the date specified
            OPG - Use OPG to send a market-on-open (MOO) or limit-on-open (LOO) order.
            FOK - If the entire Fill-or-Kill order does not execute as soon as it becomes available, the entire order is canceled.
            DTC - Day until Canceled.
            """
            if order_type == 'MTL' and time_in_force == 'AUC':
                order.m_tif = time_in_force
            elif order_type == 'MKT' and time_in_force == 'OPG':
                order.m_tif = time_in_force
            elif order_type == 'LMT' and time_in_force == 'OPG':
                order.m_tif = time_in_force
            else:
                print("WARNING: <<order_type>>:", order_type,
                      "and <<time_in_force>>:",
                      time_in_force, "parameters are not an appropriate pair.",
                      "Appropriate pairs include:"\
                      "<<order_type>> = 'MTL' : <<time_in_force>> = 'AUC',"\
                      "<<order_type>> = 'MKT' : <<time_in_force>> = 'OPG'," \
                      "<<order_type>> = 'LMT' : <<time_in_force>> = 'OPG,")

        #order.m_orderId = None
        order.m_solicited = solicited

        """
        OrderId - The API client's order id.
        IS THIS NEEDED
        
        double 	LmtPrice [get, set]
            The LIMIT price. Used for limit, stop-limit and relative orders. In all other cases specify zero. For relative orders with no limit price, also specify zero. 

        double 	AuxPrice [get, set]
            Generic field to contain the stop price for STP LMT orders, trailing amount, etc. 

        string 	Tif [get, set]
            The time in force. Valid values are: 
        
        string 	OcaGroup [get, set]
            One-Cancels-All group identifier. 

        int 	OcaType [get, set]
            Tells how to handle remaining orders in an OCA group when one order or part of an order executes. Valid values are:
        1 = Cancel all remaining orders with block.
        2 = Remaining orders are proportionately reduced in size with block.
        3 = Remaining orders are proportionately reduced in size with no block.
        If you use a value "with block" gives your order has overfill protection. This means that only one order in the group will be routed at a time to remove the possibility of an overfill. 

        string 	OrderRef [get, set]
            The order reference. Intended for institutional customers only, although all customers may use it to identify the API client that sent the order when multiple API clients are running. 

        bool 	Transmit [get, set]
            Specifies whether the order will be transmitted by TWS. If set to false, the order will be created at TWS but will not be sent. 

        int 	ParentId [get, set]
            The order ID of the parent order, used for bracket and auto trailing stop orders. 

        bool 	BlockOrder [get, set]
            If set to true, specifies that the order is an ISE Block order. 

        bool 	SweepToFill [get, set]
            If set to true, specifies that the order is a Sweep-to-Fill order. 

        int 	DisplaySize [get, set]
            The publicly disclosed order size, used when placing Iceberg orders. 

        int 	TriggerMethod [get, set]
            Specifies how Simulated Stop, Stop-Limit and Trailing Stop orders are triggered. Valid values are:
        0 - The default value. The "double bid/ask" function will be used for orders for OTC stocks and US options. All other orders will used the "last" function.
        1 - use "double bid/ask" function, where stop orders are triggered based on two consecutive bid or ask prices.
        2 - "last" function, where stop orders are triggered based on the last price.
        3 double last function.
        4 bid/ask function.
        7 last or bid/ask function.
        8 mid-point function.
        . 

        bool 	OutsideRth [get, set]
            If set to true, allows orders to also trigger or fill outside of regular trading hours. 

        bool 	Hidden [get, set]
            If set to true, the order will not be visible when viewing the market depth. This option only applies to orders routed to the ISLAND exchange. 

        string 	GoodAfterTime [get, set]
            Specifies the date and time after which the order will be active. Format: yyyymmdd hh:mm:ss {optional Timezone}. 

        string 	GoodTillDate [get, set]
            The date and time until the order will be active. You must enter GTD as the time in force to use this string. The trade's "Good Till Date," format "YYYYMMDD hh:mm:ss (optional time zone)". 

        bool 	OverridePercentageConstraints [get, set]
            Overrides TWS constraints. Precautionary constraints are defined on the TWS Presets page, and help ensure tha tyour price and size order values are reasonable. Orders sent from the API are also validated against these safety constraints, and may be rejected if any constraint is violated. To override validation, set this parameter’s value to True. 

        string 	Rule80A [get, set]

        Individual = 'I'
        Agency = 'A'
        AgentOtherMember = 'W'
        IndividualPTIA = 'J'
        AgencyPTIA = 'U'
        AgentOtherMemberPTIA = 'M'
        IndividualPT = 'K'
        AgencyPT = 'Y'
        AgentOtherMemberPT = 'N'


        bool 	AllOrNone [get, set]
            Indicates whether or not all the order has to be filled on a single execution. 

        int 	MinQty [get, set]
            Identifies a minimum quantity order type. 

        double 	PercentOffset [get, set]
            The percent offset amount for relative orders. 

        double 	TrailStopPrice [get, set]
            Trail stop price for TRAILIMIT orders. 

        double 	TrailingPercent [get, set]
            Specifies the trailing amount of a trailing stop order as a percentage. Observe the following guidelines when using the trailingPercent field:
        . More...

        string 	FaGroup [get, set]
            The Financial Advisor group the trade will be allocated to. Use an empty string if not applicable. 

        string 	FaProfile [get, set]
            The Financial Advisor allocation profile the trade will be allocated to. Use an empty string if not applicable. 

        string 	FaMethod [get, set]
            The Financial Advisor allocation method the trade will be allocated to. Use an empty string if not applicable. 

        string 	FaPercentage [get, set]
            The Financial Advisor percentage concerning the trade's allocation. Use an empty string if not applicable. 

        string 	OpenClose [get, set]
            For institutional customers only. Available for institutional clients to determine if this order is to open or close a position. Valid values are O (open), C (close). 

        int 	Origin [get, set]
            The order's origin. Same as TWS "Origin" column. Identifies the type of customer from which the order originated. Valid values are 0 (customer), 1 (firm). 

        int 	ShortSaleSlot [get, set]

        For institutions only. Valid values are: 1 (broker holds shares) or 2 (shares come from elsewhere).


        string 	DesignatedLocation [get, set]
            Used only when shortSaleSlot is 2. For institutions only. Indicates the location where the shares to short come from. Used only when short sale slot is set to 2 (which means that the shares to short are held elsewhere and not with IB). 

        int 	ExemptCode [get, set]



        double 	DiscretionaryAmt [get, set]
            The amount off the limit price allowed for discretionary orders. 

        bool 	ETradeOnly [get, set]
            Trade with electronic quotes. 

        bool 	FirmQuoteOnly [get, set]
            Trade with firm quotes. 

        double 	NbboPriceCap [get, set]
            Maximum smart order distance from the NBBO. 

        bool 	OptOutSmartRouting [get, set]
            Use to opt out of default SmartRouting for orders routed directly to ASX. This attribute defaults to false unless explicitly set to true. When set to false, orders routed directly to ASX will NOT use SmartRouting. When set to true, orders routed directly to ASX orders WILL use SmartRouting. 

        int 	AuctionStrategy [get, set]

        For BOX orders only. Values include: 1 - match 
        2 - improvement 
        3 - transparent 


        double 	StartingPrice [get, set]
            The auction's starting price. For BOX orders only. 

        double 	StockRefPrice [get, set]
            The stock's reference price. The reference price is used for VOL orders to compute the limit price sent to an exchange (whether or not Continuous Update is selected), and for price range monitoring. 

        double 	Delta [get, set]
            The stock's Delta. For orders on BOX only. 

        double 	StockRangeLower [get, set]
            The lower value for the acceptable underlying stock price range. For price improvement option orders on BOX and VOL orders with dynamic management. 

        double 	StockRangeUpper [get, set]
            The upper value for the acceptable underlying stock price range. For price improvement option orders on BOX and VOL orders with dynamic management. 

        double 	Volatility [get, set]
            The option price in volatility, as calculated by TWS' Option Analytics. This value is expressed as a percent and is used to calculate the limit price sent to the exchange. 

        int 	VolatilityType [get, set]
            Values include:
        1 - Daily Volatility 2 - Annual Volatility. 

        int 	ContinuousUpdate [get, set]
            Specifies whether TWS will automatically update the limit price of the order as the underlying price moves. VOL orders only. 

        int 	ReferencePriceType [get, set]
            Specifies how you want TWS to calculate the limit price for options, and for stock range price monitoring. VOL orders only. Valid values include: 
        1 - Average of NBBO 
        2 - NBB or the NBO depending on the action and right. 
        . 

        string 	DeltaNeutralOrderType [get, set]
            Enter an order type to instruct TWS to submit a delta neutral trade on full or partial execution of the VOL order. VOL orders only. For no hedge delta order to be sent, specify NONE. 

        double 	DeltaNeutralAuxPrice [get, set]
            Use this field to enter a value if the value in the deltaNeutralOrderType field is an order type that requires an Aux price, such as a REL order. VOL orders only. 

        int 	DeltaNeutralConId [get, set]

        DOC_TODO


        string 	DeltaNeutralSettlingFirm [get, set]

        DOC_TODO


        string 	DeltaNeutralClearingAccount [get, set]

        DOC_TODO


        string 	DeltaNeutralClearingIntent [get, set]

        DOC_TODO


        string 	DeltaNeutralOpenClose [get, set]
            Specifies whether the order is an Open or a Close order and is used when the hedge involves a CFD and and the order is clearing away. 

        bool 	DeltaNeutralShortSale [get, set]
            Used when the hedge involves a stock and indicates whether or not it is sold short. 

        int 	DeltaNeutralShortSaleSlot [get, set]

        Has a value of 1 (the clearing broker holds shares) or 2 (delivered from a third party). If you use 2, then you must specify a deltaNeutralDesignatedLocation.


        string 	DeltaNeutralDesignatedLocation [get, set]

        Used only when deltaNeutralShortSaleSlot = 2.


        double 	BasisPoints [get, set]

        DOC_TODO For EFP orders only.


        int 	BasisPointsType [get, set]

        DOC_TODO For EFP orders only.


        int 	ScaleInitLevelSize [get, set]
            Defines the size of the first, or initial, order component. For Scale orders only. 

        int 	ScaleSubsLevelSize [get, set]
            Defines the order size of the subsequent scale order components. For Scale orders only. Used in conjunction with scaleInitLevelSize(). 

        double 	ScalePriceIncrement [get, set]
            Defines the price increment between scale components. For Scale orders only. This value is compulsory. 

        double 	ScalePriceAdjustValue [get, set]

        DOC_TODO For extended Scale orders.


        int 	ScalePriceAdjustInterval [get, set]

        DOC_TODO For extended Scale orders.


        double 	ScaleProfitOffset [get, set]

        DOC_TODO For extended scale orders.


        bool 	ScaleAutoReset [get, set]

        DOC_TODO For extended scale orders.


        int 	ScaleInitPosition [get, set]

        DOC_TODO For extended scale orders.


        int 	ScaleInitFillQty [get, set]

        DOC_TODO For extended scale orders.


        bool 	ScaleRandomPercent [get, set]

        DOC_TODO For extended scale orders.


        string 	HedgeType [get, set]
            For hedge orders. Possible values include:
        D - delta 
        B - beta 
        F - FX 
        P - Pair 
        . 

        string 	HedgeParam [get, set]

        DOC_TODO Beta = x for Beta hedge orders, ratio = y for Pair hedge order


        string 	Account [get, set]
            The account the trade will be allocated to. 

        string 	SettlingFirm [get, set]

        DOC_TODO Institutions only. Indicates the firm which will settle the trade.


        string 	ClearingAccount [get, set]
            Specifies the true beneficiary of the order. For IBExecution customers. This value is required for FUT/FOP orders for reporting to the exchange. 

        string 	ClearingIntent [get, set]
            For exeuction-only clients to know where do they want their shares to be cleared at. Valid values are: IB, Away, and PTA (post trade allocation). 

        string 	AlgoStrategy [get, set]
            The algorithm strategy. As of API verion 9.6, the following algorithms are supported:
        ArrivalPx - Arrival Price 
        DarkIce - Dark Ice 
        PctVol - Percentage of Volume 
        Twap - TWAP (Time Weighted Average Price) 
        Vwap - VWAP (Volume Weighted Average Price) 
        For more information about IB's API algorithms, refer to https://www.interactivebrokers.com/en/software/api/apiguide/tables/ibalgo_parameters.htm. 

        List< TagValue > 	AlgoParams [get, set]
            The list of parameters for the IB algorithm. For more information about IB's API algorithms, refer to https://www.interactivebrokers.com/en/software/api/apiguide/tables/ibalgo_parameters.htm. 

        bool 	WhatIf [get, set]
            Allows to retrieve the commissions and margin information. When placing an order with this attribute set to true, the order will not be placed as such. Instead it will used to request the commissions and margin information that would result from this order. 

        string 	AlgoId [get, set]

        bool 	NotHeld [get, set]
            Orders routed to IBDARK are tagged as “post only” and are held in IB's order book, where incoming SmartRouted orders from other IB customers are eligible to trade against them. For IBDARK orders only. 

        List< TagValue > 	SmartComboRoutingParams [get, set]
            Parameters for combo routing. For more information, refer to https://www.interactivebrokers.com/en/software/api/apiguide/tables/smart_combo_routing.htm. 

        List< OrderComboLeg > 	OrderComboLegs [get, set]
            The attributes for all legs within a combo order. 

        List< TagValue > 	OrderMiscOptions [get, set]

        DOC_TODO


        string 	ActiveStartTime [get, set]
            for GTC orders. 

        string 	ActiveStopTime [get, set]
            for GTC orders. 

        string 	ScaleTable [get, set]
            Used for scale orders. 

        string 	ModelCode [get, set]
            model code 

        string 	ExtOperator [get, set]
            This is a regulartory attribute that applies to all US Commodity (Futures) Exchanges, provided to allow client to comply with CFTC Tag 50 Rules. 

        double 	CashQty [get, set]
            The native cash quantity. 

        bool 	RandomizeSize [get, set]

        DOC_TODO


        bool 	RandomizePrice [get, set]

        DOC_TODO


        int 	ReferenceContractId [get, set]
            Pegged-to-benchmark orders: this attribute will contain the conId of the contract against which the order will be pegged. 

        bool 	IsPeggedChangeAmountDecrease [get, set]
            Pegged-to-benchmark orders: indicates whether the order's pegged price should increase or decreases. 

        double 	PeggedChangeAmount [get, set]
            Pegged-to-benchmark orders: amount by which the order's pegged price should move. 

        double 	ReferenceChangeAmount [get, set]
            Pegged-to-benchmark orders: the amount the reference contract needs to move to adjust the pegged order. 

        string 	ReferenceExchange [get, set]
            Pegged-to-benchmark orders: the exchange against which we want to observe the reference contract. 

        string 	AdjustedOrderType [get, set]
            Adjusted Stop orders: the parent order will be adjusted to the given type when the adjusted trigger price is penetrated. 

        double 	TriggerPrice [get, set]

        DOC_TODO


        double 	LmtPriceOffset [get, set]

        DOC_TODO


        double 	AdjustedStopPrice [get, set]
            Adjusted Stop orders: specifies the stop price of the adjusted (STP) parent. 

        double 	AdjustedStopLimitPrice [get, set]
            Adjusted Stop orders: specifies the stop limit price of the adjusted (STPL LMT) parent. 

        double 	AdjustedTrailingAmount [get, set]
            Adjusted Stop orders: specifies the trailing amount of the adjusted (TRAIL) parent. 

        int 	AdjustableTrailingUnit [get, set]
            Adjusted Stop orders: specifies where the trailing unit is an amount (set to 0) or a percentage (set to 1) 

        List< OrderCondition > 	Conditions [get, set]
            Conditions determining when the order will be activated or canceled. 

        bool 	ConditionsIgnoreRth [get, set]
            Indicates whether or not conditions will also be valid outside Regular Trading Hours. 

        bool 	ConditionsCancelOrder [get, set]
            Conditions can determine if an order should become active or canceled. 

        SoftDollarTier 	Tier [get, set]
            Define the Soft Dollar Tier used for the order. Only provided for registered professional advisors and hedge and mutual funds. 
        """
        return order

    def preparePosition(self, position = pos.Position()):
        """
        SUMMARY:
            Unpack position object into order and contracts.
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        raise NotImplementedError("API method preparePosition has not been implemented.")
        #return None

    def createExecutionFilter(self, contract = None, order_time = None):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
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
    """
    CLASS SUMMARY:
        General data broker.

    CLASS PROPERTIES:
        data_repository -
        path_root -
        exec_path -

    CLASS SPECIAL METHODS:
        None

    CLASS PRIVATE METHODS:
        None

    CLASS PUBLIC METHODS:
        getLocalData -
    """
    def __init__(self, path_root = '/', project = '', data_file = '',
                 exec_path = '', **kwargs):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        super(DataBroker, self).__init__(**kwargs)

        self._data_repository = dat.Repository(path_root = path_root,
                                                project = project,
                                                data_file = data_file)
        self._path_root = path_root

        self._exec_path = exec_path

    """
    CLASS PROPERTIES
    """
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

    def exec_path():
        doc = "The exec_path property."
        def fget(self):
            return self._exec_path
        def fset(self, value):
            self._exec_path = value
        def fdel(self):
            del self._exec_path
        return locals()
    exec_path = property(**exec_path())

    """
    CLASS SPECIAL METHODS
    """

    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """
    def getLocalData(self, type_data = '', path_data = '', file_name = ''): #data.Repository()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        files = glob.iglob(path_data + '*.' + type_data)
        while True:
            f = files.next()
            if fnmatch.fnmatch(f, '*' + file_name + '.' + type_data):
                return f


class IBDataBroker(IBBroker, DataBroker):
    """
    CLASS SUMMARY:
        <DataBroker> for <IBBroker>.

    CLASS PROPERTIES:
        current_request_id -
        tickers -
        current_ticker_id -

    CLASS SPECIAL METHODS:
        None

    CLASS PRIVATE METHODS:
        _resetCallbackAttribute -
        _incrementTickerID -
        _addTicker -
        _isInTradingHours -

    CLASS PUBLIC METHODS:
        getCallbackAttribute -
        searchTickers -
        tickerSearch -
        contractSearch -
        removeFromTickers -
        getAccountInformation -
        getDataAtTime -
        getDataInRange -
        getDailyData -
        getContractDetails -
        getLiveMarketData -
        getPostiions -
        getPortfolio -
        getExecutedOrders -
        getPNLToday -
        recordPNLToday -
        recordPNLDailyPerformance -
        recordTransaction -
        getTransactions -
    """

    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, path_root = '/', **kwargs):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        super(IBDataBroker, self).__init__(account_name = account_name,
                                            host = host, port = port,
                                            client_id = client_id,
                                            path_root = path_root, **kwargs)

        #read state from file or call from IB
        #store as dictionary or DF?
        #keep trying to create a valid id?
        self._current_request_id = 1

        self._tickers = {}
        self._current_ticker_id = 1

    """
    CLASS PROPERTIES
    """
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

    """
    CLASS SPECIAL METHODS
    """

    """
    CLASS PRIVATE METHODS
    """
    def _resetCallbackAttribute(self, attribute = ''):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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
                            'historical_Data', 'scanner_Data', 'real_timeBar', 'contract_Details'):
            setattr(self.callback, attribute, [])

        else:
            print("Attribute not found.\nNo attribute reset.")

    def getCallbackAttribute(self, attribute = ''):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        return getattr(self.callback, attribute)

    def _incrementTickerID(self):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        self.current_ticker_id += 1

    # MAY NOT NEED ANYMORE
    def _addTicker(self, ticker = '', contract = Contract()):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        if yes:
            return 1
        return 0

    """
    CLASS PUBLIC METHODS
    """
    def searchTickers(self, search_object, type_search = '', type_data = ''):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
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
            # FOR ERROR HANDLING THE BELOW IF STATEMENT WAS ADDED 10/07/17            
            if len(ticker_id) == 0:
                return
            del self.tickers[ticker_id[0]]

    def getAccountInformation(self, all_accounts = True, attributes = ','):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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
                                    'Currency'])
        return data

    def getDataAtTime(self, data_time, type_data = 'BID_ASK',
                        contract = Contract(), type_time = '',
                        in_trading_hours = False, duration = '60 S',
                        bar_size = '1 min', try_time = 2, time_out = 15):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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

#        ticker_id = self._addTicker(ticker = contract.m_symbol)
        ticker_id = self.nextOrderId(from_datetime=True)

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

            time.sleep(try_time)
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
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        # EXTEND USING getDataAtTime()
        raise NotImplementedError("API method getDataInRange has not been implemented.")
        #return None

    def getDailyData(self, stock_list, provider, date_start, date_end = None):
        """
        SUMMARY:
            Method summary

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
            None
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

    def getContractDetails(self, contract=Contract(), time_out=5):
        """
        SUMMARY:
            Returns data frame of chain of contracts meeting certain
            requirements. Used to obtain non-expired future chain right now.

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        self._resetCallbackAttribute('contract_Details')        
        self.tws.reqContractDetails(1,contract)
        
        time.sleep(1)
        
#        print( self.callback.contract_Details. ) 
        
#        print(self.callback.contract_Details.m_contractMonth)
        
        contract_details = self.callback.contract_Details
        
        
        fut_cont_dict = {}

        for detail in contract_details:
            fut_cont_dict[detail.m_summary.m_localSymbol] = ( detail.m_marketName,
                                                          detail.m_contractMonth,
                                                          detail.m_summary.m_expiry,
                                                          detail.m_summary.m_symbol,
                                                          detail.m_summary )
        fut_cont_dict = pd.DataFrame.from_dict(fut_cont_dict, orient='index' )
        fut_cont_dict.columns = ['market_symbol', 'contractMonth', 'Expiry', 'IB_symbol', 'Contract object']
        fut_cont_dict.sort_values('Expiry', inplace=True, ascending=True)
        
        def convertExpiry(x):                    
            if( type(x) == str ):
                return (dt.datetime.strptime(x, "%Y%m%d" )).date() # should be string
            else:
                pass

        fut_cont_dict['Expiry'] = fut_cont_dict['Expiry'].apply( convertExpiry )

        return fut_cont_dict

    def getLiveMarketData(self, contract = Contract(), time_out = 5):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
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
        """
         self.tickers = contract
        
        ticker_id = self.searchTickers(search_object = contract,
                                type_search = 'CONTRACT',
                                type_data = 'ID')[0]
        """
#        ticker_id = self.nextOrderId(from_datetime=True)

        self._resetCallbackAttribute('tick_Price')
        data = pd.DataFrame(self.callback.tick_Price,
                            columns = ['tickerId', 'field', 'price',
                                        'canAutoExecute'])
        data_null = data

        now = dt.datetime.now()
        end_wait = now + dt.timedelta(seconds = time_out)

        while data.equals(data_null) and now <= end_wait:

            self.tws.reqMktData(tickerId = self.nextOrderId(), contract = contract,
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
            return pd.DataFrame()
            # CHANGED FUNDAMENTAL ASSUMPTION; ALWAYS RETURNING A DATAFRAME FOR EASIER ERROR HANDLING 10/07/17

        data["Type"] = data["field"].map(tick_type)

        return data

    def getPositions(self):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        self._resetCallbackAttribute('update_Position')

        self.tws.reqPositions()

        time.sleep(1)

        data = pd.DataFrame(self.callback.update_Position,
                            columns = ['Account_Name', 'Contract_Id','Contract_Object',
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
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        if since == None:
            execution_filter = self.createExecutionFilter(contract = contract)
        else:
            execution_filter = self.createExecutionFilter(contract = contract,
                                                            order_time = since)

        self.tws.reqExecutions(1, execution_filter)

        time.sleep(2)
        
        ''' this will complain if MOC is used '''
        ''' It's trying to look fo rexecutions before it has happened '''
        ''' We should store this internally eventually '''
        try:
            execution_contract = self.callback.exec_Details_contract.__dict__
            execution_details = self.callback.exec_Details_execution.__dict__            
        except:            
            return pd.DataFrame()
        
            
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

        self._resetCallbackAttribute('exec_Details_contract')
        self._resetCallbackAttribute('exec_Details_execution')

        return data
#        pass

    # TODO: MAKE RECORD AND GETTING STRATEGY SPECIFIC; STRATEGY PNL NOT RECORDED
    # ONLY ACCOUNT WIDE PNL
    # TODO: CHECK IF IT IS POSSIBLE TO ACQUIRE PAST PORTFOLIO VALUES
    def getPNLToday(self):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
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
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        PNL = self.getPNLToday()

        PNL.to_csv(path_or_buf = path, encoding = 'utf-8', mode = 'w+')

    def recordPNLDailyPerformance(self, path = ''):
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        PNL = self.getPNLToday()

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
        """
        SUMMARY:
            Method summary

        PARAMETERS:
            None

        RETURNS:
            None

        RESULTS:
            None
        """
        order_details = self.getExecutedOrders(contract)

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

    def getTransactions(self, path = ''):
        """
        SUMMARY:
            Returns the executed transactions by a [system] read from a file
            at the location of <<path>>.

        PARAMETERS:
            path -

        RETURNS:
            data -

        RESULTS:
            Gets the executed transactions of the current day.
        """
        """
        TODO: just a read or prepare in some fashion? from strategy POV how
        should the strategy deal with reading from state?
        """
        raise NotImplementedError("API method <getTransactions >"\
                                  "has not been implemented.")
        #return None


class ExecutionBroker(Broker):
    """
    CLASS SUMMARY:
        Broker for trade executions.

    CLASS PROPERTIES:
        None

    CLASS SPECIAL METHODS:
        None

    CLASS PRIVATE METHODS:
        None

    CLASS PUBLIC METHODS:
        None
    """

    def __init__(self, **kwargs):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        super(ExecutionBroker, self).__init__(**kwargs)

    """
    CLASS PROPERTIES
    """

    """
    CLASS SPECIAL METHODS
    """

    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """


class IBExecutionBroker(IBBroker, ExecutionBroker):
    """
    CLASS SUMMARY:
        <ExecutionBroker> for <IBBroker>.

    CLASS PROPERTIES:
        None

    CLASS SPECIAL METHODS:
        None

    CLASS PRIVATE METHODS:
        None

    CLASS PUBLIC METHODS:
        placeOrder -
        cancelOrder -
    """

    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, **kwargs):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        super(IBExecutionBroker, self).__init__(account_name = account_name,
                                                host = host, port = port,
                                                client_id = client_id, **kwargs)

    """
    CLASS PROPERTIES
    """

    """
    CLASS SPECIAL METHODS
    """

    """
    CLASS PRIVATE METHODS
    """

    """
    CLASS PUBLIC METHODS
    """
    def placeOrder(self, order_id, contract, order):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        self.tws.placeOrder(order_id, contract, order)

    def cancelOrder(self, order_id):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
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
    """
    CLASS SUMMARY:
        Aggregate <Broker> for Interactive Brokers.

    CLASS PROPERTIES:
        None

    CLASS SPECIAL METHODS:
        None

    CLASS PRIVATE METHODS:
        _totalDollarToTotalUnits -

    CLASS PUBLIC METHODS:
        closeAllPositions -
        closeAllTypePositions -
        closeAllNamePositions -
        closePosition -
        createDollarOder -
        palceRecordedOrder -
        getLiveMidPriceData -
    """

    def __init__(self, account_name = 'DU603835', host = '', port = 7497,
                    client_id = 100, path_root = '/', **kwargs):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        """
        IBBrokerTotal initializer.
        Initializes object properties.
        Combines functionality of <IBExecutionBroker> and <IBDataBroker>.

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
                                            path_root = path_root, **kwargs)
        
        pass

    """
    CLASS PROPERTIES
    """

    """
    CLASS SPECIAL METHODS
    """

    """
    CLASS PRIVATE METHODS
    """

    def _totalDollarToTotalUnits(self, amount_dollars, contract, at_time=False,
                                 data_time=None):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        if at_time == True and data_time == None:
            data_time = dt.datetime.now()

            data = self.getDataAtTime(data_time=data_time, contract=contract)

            askPrice = data['price'][data['Type'] == 'ASK PRICE'].values[0]
            bidPrice = data['price'][data['Type'] == 'BID PRICE'].values[0]

            price_per_unit = (askPrice + bidPrice) * 0.5  # mid point

            return int(amount_dollars / price_per_unit)

        liveData = self.getLiveMarketData(contract=contract)

        liveData = liveData[liveData['price'] != -1]  # remove -1's

        try:
            askPrice = \
            liveData['price'][liveData['Type'] == 'ASK PRICE'].values[
                0]  # Try to get mid price .. if not use Close price
            bidPrice = \
            liveData['price'][liveData['Type'] == 'BID PRICE'].values[0]

            price_per_unit = (askPrice + bidPrice) * 0.5  # mid point

        except:
            price_per_unit = \
            liveData['price'][liveData['Type'] == 'CLOSE PRICE'].values[0]

        return int(amount_dollars / price_per_unit)

    """
    CLASS PUBLIC METHODS
    """
    def closeAllPositions(self, order_type = '', exclude_symbol = [''],
                            exclude_instrument = [''], record = False):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
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
            print("Given order_type is not a proper type.\nMust be one of: " \
                  "'LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT', 'QUOTE', 'STP'," \
                  "'STP LMT', 'TRAIL LIT', 'TRAIL MIT', 'TRAIL'," \
                  "'TRAIL LIMIT','MIT', 'MOO', 'PEG MKT', 'REL', 'BOX TOP'," \
                  "'LOC', 'LOO', 'LIT', 'PEG MID', 'VWAP', 'GAT', 'GTD'," \
                  "'GTC','IOC', 'OCA', 'VOL'.")
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

            if record:
                self.placeRecordedOrder(order_id=order_id, contract=contract,
                                        order=order, path=self.exec_path)
            else:
                self.placeOrder(order_id = order_id, contract = contract,
                                order = order)
            time.sleep(1)

#            order_id += 1
            order_id = self.nextOrderId()

    def closeAllTypePositions(self, order_type = '', instruments = [''],
                                exclude_symbol = [''], record = False, exchange='SMART'):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        if order_type not in ('LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT',
                              'QUOTE', 'STP', 'STP LMT', 'TRAIL LIT',
                              'TRAIL MIT', 'TRAIL', 'TRAIL LIMIT', 'MIT', 'MOO',
                              'PEG MKT', 'REL', 'BOX TOP', 'LOC', 'LOO', 'LIT',
                              'PEG MID', 'VWAP', 'GAT', 'GTD', 'GTC', 'IOC',
                              'OCA', 'VOL'):
            print("Given order_type is not a proper type.\nMust be one of: " \
                  "'LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT', 'QUOTE', 'STP'," \
                  "'STP LMT', 'TRAIL LIT', 'TRAIL MIT', 'TRAIL'," \
                  "'TRAIL LIMIT','MIT', 'MOO', 'PEG MKT', 'REL', 'BOX TOP'," \
                  "'LOC', 'LOO', 'LIT', 'PEG MID', 'VWAP', 'GAT', 'GTD'," \
                  "'GTC','IOC', 'OCA', 'VOL'.")
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
            
            if ( instrument_type=='STK' ):
                contract = self.createContract(ticker = ticker,
                                                instrument_type = instrument_type,
                                                exchange = 'SMART',
                                                currency = 'USD')
                
            if ( instrument_type=='FUT' ):            
#                print( position_details['Local_Symbol'] )
#                
##                localSymbol = position_details['Local_Symbol']#.values[0]
#                expiry = position_details['Expiry']#.values[0]
#                symbol = position_details['Symbol']#.values[0]
#                mult = position_details['Multiplier']#.values[0]
#                
#                contract = self.createContract( ticker=symbol, #localSymbol=localSymbol,
#                                                    instrument_type = instrument_type,
#                                                    expiry=expiry,
#                                                    multiplier = mult,
#                                                    exchange = 'DTB',
#                                                    currency = 'USD')                
                contract = position_details['Contract_Object']
                

            
            for ex in exchange:
                contract.m_exchange = ex
            
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
    
                if record:
                    self.placeRecordedOrder(order_id=self.nextOrderId(), contract=contract,
                                            order=order, path=self.exec_path)
                else:
                    self.placeOrder(order_id = self.nextOrderId(), contract = contract, order = order)
                time.sleep(1)
    
    #            order_id += 1
                order_id = self.nextOrderId()

    def closeAllNamePositions(self, order_type = '', tickers = [''],
                              record = False):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        if order_type not in ('LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT',
                              'QUOTE', 'STP', 'STP LMT', 'TRAIL LIT',
                              'TRAIL MIT', 'TRAIL', 'TRAIL LIMIT', 'MIT', 'MOO',
                              'PEG MKT', 'REL', 'BOX TOP', 'LOC', 'LOO', 'LIT',
                              'PEG MID', 'VWAP', 'GAT', 'GTD', 'GTC', 'IOC',
                              'OCA', 'VOL'):
            print("Given order_type is not a proper type.\nMust be one of: " \
                  "'LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT', 'QUOTE', 'STP'," \
                  "'STP LMT', 'TRAIL LIT', 'TRAIL MIT', 'TRAIL'," \
                  "'TRAIL LIMIT','MIT', 'MOO', 'PEG MKT', 'REL', 'BOX TOP'," \
                  "'LOC', 'LOO', 'LIT', 'PEG MID', 'VWAP', 'GAT', 'GTD'," \
                  "'GTC','IOC', 'OCA', 'VOL'.")
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

            if record:
                self.placeRecordedOrder(order_id=order_id, contract=contract,
                                        order=order, path=self.exec_path)
            else:
                self.placeOrder(order_id = order_id, contract = contract, order = order)
            time.sleep(1)

#            order_id += 1
            order_id = self.nextOrderId()

    def closePosition(self, symbol = '', order_type = '', record = False):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        if order_type not in ('LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT',
                              'QUOTE', 'STP', 'STP LMT', 'TRAIL LIT',
                              'TRAIL MIT', 'TRAIL', 'TRAIL LIMIT', 'MIT', 'MOO',
                              'PEG MKT', 'REL', 'BOX TOP', 'LOC', 'LOO', 'LIT',
                              'PEG MID', 'VWAP', 'GAT', 'GTD', 'GTC', 'IOC',
                              'OCA', 'VOL'):
            print("Given order_type is not a proper type.\nMust be one of: " \
                  "'LIMIT', 'MARKET', 'MOC', 'MTL', 'MKT PRT', 'QUOTE', 'STP'," \
                  "'STP LMT', 'TRAIL LIT', 'TRAIL MIT', 'TRAIL'," \
                  "'TRAIL LIMIT','MIT', 'MOO', 'PEG MKT', 'REL', 'BOX TOP'," \
                  "'LOC', 'LOO', 'LIT', 'PEG MID', 'VWAP', 'GAT', 'GTD'," \
                  "'GTC','IOC', 'OCA', 'VOL'.")
            return None


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
        
#        order_id = self.nextOrderId()    
#        print( symbol, order_id )

        if record:
            self.placeRecordedOrder(order_id=self.nextOrderId(), contract=contract,
                                order=order, path=self.exec_path)
            
#            print( symbol, order_id )
        else:
            self.placeOrder(order_id = self.nextOrderId(), contract = contract, order = order)
        time.sleep(1.1)

    def createDollarOrder(self, amount_dollars, contract, trade_type,
                            price_per_unit = 0.0, order_type = '',
                          time_in_force = ''):
        """
        SUMMARY:
            Method summary
        
        PARAMETERS:
            None
        
        RETURNS:
            None
        
        RESULTS:
            None
        """
        amount_units = self._totalDollarToTotalUnits( amount_dollars = amount_dollars,
                                                      contract = contract)

        if( amount_units==0 ):
            print ( "We are trying to buy " + str(amount_units) + " units of a stock. Something is wrong. ")

        order = self.createOrder(trade_type = trade_type,
                                    amount_units = amount_units,
                                    price_per_unit = price_per_unit,
                                    order_type = order_type,
                                    time_in_force=time_in_force)
        return order

    def placeRecordedOrder(self, order_id, contract, order, path = '',
                           additional_values = {}):
        """
        SUMMARY:
            Places an [order] on the [#Interactive Brokers server] and records
            the transaction.
        
        PARAMETERS:
            order_id - 
            contract - 
            order - 
            path - 
            additional_values - 
        
        RETURNS:
            None
        
        RESULTS:
            Creates a local record of an [executed order] at the
            <<path>> location.
        """
        self.tws.placeOrder(order_id, contract, order)
        if (path != ''):
            self.recordTransaction(contract=contract, path=path,
                                          additional_values=additional_values)

    def getLiveMidPriceData(self, contract):
        """
        SUMMARY:
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