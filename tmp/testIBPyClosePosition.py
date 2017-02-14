
'''
For ticker X and trading day t
- At Market Open (MO), compute ROC(X,t) , the Open to Close returns for ticker X:
    ROC(X,t) = ( Open(X,t) -Close(X,t-1) ) / Close(X,t-1)
    -This is a cheap momentum indicator
- If ROC(X,t) > 0, then Long 1 dollar worth of X at  time To where To >= MO
- If ROC(X,t) < 0, then Short 1 dollar worth of X at time To where To >= MO
- Exit the position on day t at Tf = To+dT, where Tf \in [To, MC]
'''
from __future__ import (absolute_import, division, print_function)

import sys
import getopt
import traceback
import datetime as dt
from dateutil.parser import parse as dateParse
from time import sleep, strftime, ctime

import pandas as pd
from tqdm import tqdm
import numpy as np

import QTS.lib.readWriteData as rwd
import QTS.lib.directory as dr
import QTS.lib.parsers as prs
import QTS.lib.utilities as ut
import QTS.dataHandler as dh

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message, ibConnection

import collections
import sys

if sys.version_info.major == 2:
    import Queue as queue
    import itertools
    map = itertools.imap

else:  # >= 3
    import queue

def make_contract(symbol, sec_type, exch, prim_exch, curr):
    Contract.m_symbol = symbol
    Contract.m_secType = sec_type
    Contract.m_exchange = exch
    Contract.m_primaryExch = prim_exch
    Contract.m_currency = curr
    return Contract

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

past_day_close = 0
current_day_open = 0

def hist_data_handler(msg):
    try:
        #print(msg)
        values = msg.values()
        #print(msg.values())
        if values[1][0] == 'f':
            print('done')
            return

        print("date:", dt.date(int(values[1][:4]), int(values[1][4:6]), int(values[1][6:8])).strftime("%Y-%m-%d"))
        price_open = values[2]
        print("open:", price_open)
        price_close = values[5]
        print("close:", price_close)

        global past_day_close
        global current_day_open

        if past_day_close == 0:
            past_day_close = price_close

        elif past_day_close != 0 and current_day_open == 0:
            current_day_open = price_open

        if past_day_close != 0 and current_day_open != 0:
            ROC = (current_day_open - past_day_close) / float(past_day_close)

            if ROC > 0:
                offer = make_order('BUY', 1)

            elif ROC < 0:
                offer = make_order('SELL', 1)

            connection.placeOrder(1, contract, offer)
        print('\n')
    except:
        print("error:", traceback.format_exc())

def tick_price_handler(msg):
    try:
        print(msg)
        print(msg.values())
    except:
        print('error')

def order_handler(msg):
    try:
        '''print(msg)
        print('\n',msg.values())'''
        pass
    except:
        print("error:", traceback.format_exc())

def id_handler(msg):
    try:
        global orderId
        orderId = msg.values()[0]
    except:
        print("error:", traceback.format_exc())
def time_handler(msg):
    try:
        '''print(msg.values()[0])'''
        pass
    except:
        print(traceback.format_exc())

def position_handler(msg):
    try:
        values = msg.values()
        print(values)
        contract = values[1]
        position = values[2]
        amount = abs(position)
        action = ''

        if position < 0 :
            action = 'BUY'
        elif position > 0:
            action = 'SELL'

        offer = make_order(action, amount)

        global orderId
        connection.placeOrder(orderId, contract, offer)
    except:
        print(traceback.format_exc())

def account_handler(msg):
    try:
        values = msg.values()
        print(msg)
        print(values)

        contract = values[0]
        print(contract)
        position = values[1]
        amount = abs(position)
        action = ''

        if position < 0 :
            action = 'BUY'
        elif position > 0:
            action = 'SELL'

        offer = make_order(action, amount)

        global orderId
        connection.placeOrder(orderId, contract, offer)
    except:
        print(traceback.format_exc())

#callback = IBWrapper()
connection = ibConnection(port=7497, clientId=100)
#connection.register(hist_data_handler, message.historicalData)
#connection.register(tick_price_handler, message.tickPrice)
#connection.register(order_handler, message.openOrder)
connection.register(time_handler, message.currentTime)
connection.register(id_handler, message.nextValidId)
#connection.register(position_handler, message.position)
connection.register(account_handler, message.updatePortfolio)
connection.connect()
contract = make_contract('SPY', 'STK', 'SMART', 'SMART', 'USD')


#connection.reqOpenOrders()
'''
endtime = '20170124 12:00:00 US/Eastern'

connection.reqHistoricalData(tickerId=1,
                    contract=contract,
                    endDateTime=endtime,
                    durationStr="2 D",
                    barSizeSetting='1 day',
                    whatToShow='MIDPOINT',
                    useRTH=0,
                    formatDate=1)

connection.reqMktData(tickerId=1,
                contract = contract,
                genericTickList = '',
                snapshot = False)
'''
count = 1
orderId = 0
currentTime = dt.datetime.now()
year = currentTime.year
month = currentTime.month
day = currentTime.day
while dt.datetime.now() < dt.datetime(year = year, month = month, day = day, hour = 15, minute = 59, second = 50):
    print(count)
    count += 1

    offer = make_order('BUY', 10)

    connection.reqIds(1)
    sleep(1)
    print("order:",orderId)
    print(dt.datetime.now())
    connection.placeOrder(orderId, contract, offer)
    sleep(119)

    connection.reqIds(1)
    sleep(1)
    print("order:",orderId)
    print(dt.datetime.now())
    #offer = make_order('SELL', 10)
    #connection.reqPositions()
    #connection.placeOrder(orderId, contract, offer)
    connection.reqAccountUpdates(subscribe = True, acctCode = 'DU603835')
    sleep(119)


print("Outside of regular trading hours")
print('Disconnected:', connection.disconnect())
