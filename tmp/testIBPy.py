from __future__ import (absolute_import, division, print_function)
'''
More details on this script can be found in this tutorial:
https://github.com/anthonyng2/ib/blob/master/IbPy%20Demo.ipynb
https://nbviewer.jupyter.org/github/anthonyng2/ib/blob/master/IbPy%20Demo.ipynb
'''

import sys
import traceback
import warnings
warnings.filterwarnings('ignore')

import time
import datetime as dt

import pandas as pd
import numpy as np
from tqdm import tqdm

'''
IBWrapper is an implemented version of the abstract EWrapper class by Anthony Ng
- https://github.com/anthonyng2/ib


'''
from IBWrapper import IBWrapper, contract
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ScannerSubscription import ScannerSubscription
################################################################################
'''
Specifying Account Details:
- instantiate IBWrapper class (custom)
- accountName cannot be changed (is set for papar252)
- port and clientId are arbitrary but must match values in TWS/IB Gateway config file
'''
accountName = "DU603835"
callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7497
clientId = 100
################################################################################
tws.eConnect(host, port, clientId)

#outputs server information to commandline
#tws.setServerLogLevel(5)

contract = contract()
callback.initiate_variables()
################################################################################
'''

https://www.interactivebrokers.com/en/software/api/api.htm

Requesting Account Changes:
- I believe this allows you to subcribe to changes to your account after orders
- this could also be implemented by an explicit call to Account Summary
'''
tws.reqAccountUpdates(1, accountName)
time.sleep(2)

df_account_updates = pd.DataFrame(callback.update_AccountValue, columns = ['key', 'value', 'currency', 'accountName'])
print('df_account_updates:\n',df_account_updates,'\n\n')

df_portfolio = pd.DataFrame(callback.update_Portfolio, columns=['Account Name', 'Contract ID'
                                                                'Currency', 'Expiry','Include Expired',
                                                                'Local Symbol','Multiplier',
                                                                'Primary Exchange','Right',
                                                                'Security Type','Strike',
                                                                'Symbol','Trading Class',
                                                                'Position','Market Price'
                                                                'Market Value', 'Average Cost',
                                                                'Unrealised PnL', 'Realised PnL',])
print('df_portfolio:\n',df_portfolio,'\n\n')
################################################################################
'''
Requesting Account Attributes:
- can request attributes in third parameter position
'''
tws.reqAccountSummary(2,"All","NetLiquidation")
time.sleep(2)

df_account_summary = pd.DataFrame(callback.account_Summary,
             columns = ['Request_ID','Account','Tag','Value','Curency'])
print('df_account_summary:\n',df_account_summary,'\n\n')
################################################################################
'''
Requesting Portfolio Positions Across All Accounts:
'''
tws.reqPositions()
time.sleep(2)

df_positions = pd.DataFrame(callback.update_Position,
                   columns=['Account','Contract ID','Currency','Exchange','Expiry',
                            'Include Expired','Local Symbol','Multiplier','Right',
                            'Security Type','Strike','Symbol','Trading Class',
                            'Position','Average Cost'])
print('df_positions:\n',df_positions[df_positions["Account"] == accountName],'\n\n')
################################################################################

'''
Placing Orders:
- calls next valid order_id for placing 'BUY' or 'SELL' orders
- I don't believe that the incrementing needs to be done but need to confirm
'''


tws.reqIds(1)
order_id = callback.next_ValidId + 1

contract_info = contract.create_contract("GOOG", "STK", "SMART", "USD")
#order_info = contract.create_order(accountName, "MKT", 100, "BUY")

order_info = contract.create_order(accountName, "MKT", 100, "BUY")


tws.placeOrder(order_id, contract_info, order_info)

tws.cancelOrder(order_id)

'''
df_order_status = pd.DataFrame(callback.order_Status,
                    columns = ['orderId', 'status', 'filled', 'remaining', 'avgFillPrice',
                                'permId', 'parentId', 'lastFillPrice', 'clientId', 'whyHeld'])

print('df_order_status:\n',df_order_status,'\n\n')
'''

print(callback.open_Order[:1])




################################################################################

''' Get historical data  '''


################################################################################

# [1, 321, "Error validating request:-'yd' : cause - Historical data bar size setting is invalid. Legal ones are: 1 secs, 
# 5 secs, 10 secs, 15 secs, 30 secs, 1 min, 2 mins, 3 mins, 5 mins, 10 mins, 15 mins, 20 mins, 30 mins, 1 hour, 
# 2 hours, 3 hours, 4 hours, 8 hours, 1 day, 1W, 1M"]

tws.reqHistoricalData(tickerId=1, 
                      contract= contract_info,
                      endDateTime='20170208 15:59:59 EST',
                      durationStr='2 D',
                      barSizeSetting='1 day',
                      whatToShow='MIDPOINT', 
                      useRTH=   1,
                      formatDate = 1,                      
                      )
'''
# reqId - int
# date - str
# open - double
# high - double
# low - double
# close - double
# Volume - int
# Counts - int
# WAP - double
# hasGaps - Bool

# Bar data is stored in callback.historical_Data
'''

print( len(callback.historical_Data) )

callback.historical_Data[-4]
callback.historical_Data[-3]
callback.historical_Data[-2]
callback.historical_Data[-1]



################################################################################
''' This function will get the data from open     '''
################################################################################

callback.historical_Data = []


def getPriceAtSpecificTime(tws=None, contract_info=None, targetDateTime='20170208 15:59:59 EST', callback=callback):
    
    #del callback.historical_Data[:]
    
    tws.reqHistoricalData( tickerId=1, 
                      contract = contract_info,
                      endDateTime = targetDateTime,
                      durationStr = '10 S',
                      barSizeSetting = '1 secs',
                      whatToShow = 'MIDPOINT', 
                      useRTH = 1,
                      formatDate = 1
                      )
    try:
        callback.historical_Data[1][1], callback.historical_Data[0] 
    except:
        callback.historical_Data[1][1], callback.historical_Data[0] 
    
    
#    time = callback.historical_Data[1][1].split("-")
    
    return ( callback.historical_Data[1][1], callback.historical_Data[0] )




MC = '20170208 15:59:59 EST'
MO = '20170208 9:30:00 EST'

tws.reqHistoricalData( tickerId=1, 
                  contract = contract_info,
                  endDateTime = MC,
                  durationStr = '1 D',
                  barSizeSetting = '1 secs',
                  whatToShow = 'MIDPOINT', 
                  useRTH = 1,
                  formatDate = 1
                  )

callback.historical_Data

CB = getPriceAtSpecificTime( tws=tws, contract_info = contract_info, targetDateTime = MO )



getPriceAtSpecificTime( tws=tws, contract_info = contract_info, targetDateTime = MC )

# MC then MO

for i in np.arange(0, len(callback.historical_Data)):
    
    print(i,callback.historical_Data[i])


#print( type(callback.historical_Data) )


################################################################################
''' This function will get the data from close     '''
################################################################################











