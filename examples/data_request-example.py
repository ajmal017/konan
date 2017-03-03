"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
data_request-example.py
Created on 2017-02-21T17:23:00Z
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
from dateutil.parser import parse

# internal/custom imports
import api.broker as broker

ibdb = broker.IBDataBroker()

contract = ibdb.createContract(ticker = 'GOOG', instrument_type = 'STK')

ibdb.connect()

data = ibdb.getHistoricalMarketData(ticker_id = 1, type_data = 'OPEN', contract = c, time_start = dt.datetime(year=2017,month=2,day=21,hour=9,minute=30))

print(data)



''' ===================================== '''
''' Getting data at a specific time slice '''
''' ===================================== '''
'''
barsize:
   
1 secs, 5 secs, 10 secs, 15 secs, 30 secs, 1 min, 2 mins, 3 mins, 5 mins, 10 mins, 15 mins, 20 mins, 30 mins, 1 hour, 2 hours, 3 hours, 4 hours, 8 hours, 1 day, 1W, 1M"
'''


ib = broker.IBDataBroker()
ib.connect()

c = ib.createContract(ticker = 'GOOG', instrument_type = 'STK')

time_end = "20170222 9:30:00"
duration = "60 S"
bar = '1 min'
_id=3

ib._resetCallbackAttribute('historical_Data')

ib.tws.reqHistoricalData( tickerId = _id,
                         contract = c,
                         endDateTime = time_end ,
                         durationStr = duration,
                         barSizeSetting = bar, whatToShow = 'BID',
                         useRTH = 0, formatDate = 1)

data = pd.DataFrame(ib.callback.historical_Data, columns = ["reqId",
                                                                "date", "open",
                                                                "high", "low",
                                                                "close",
                                                                "volume",
                                                                "count", "WAP",
                                                                "hasGaps"])

data.drop(data.index[-1], inplace=True)
data['date'] = data['date'].apply(parse)
data.set_index('date', inplace=True)

