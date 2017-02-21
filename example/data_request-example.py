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

# internal/custom imports
import api.broker as broker

ibdb = broker.IBDataBroker()

contract = ibdb.createContract(ticker = 'GOOG', instrument_type = 'STK')

ibdb.connect()

data = ibdb.getHistoricalMarketData(ticker_id = 1, type_data = 'OPEN', contract = c, time_start = dt.datetime(year=2017,month=2,day=21,hour=9,minute=30))

print(data)
