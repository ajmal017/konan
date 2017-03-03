# -*- coding: utf-8 -*-

import konan.api.broker as broker
from ib.ext.Contract import Contract
import pandas as pd
from dateutil.parser import parse
import time
import numpy as np
import datetime
import utils
import pickle


ib = broker.IBExecutionBroker()


nyse = pickle.load( open('C:\\Users\\Ray\\Google Drive\\myPythonProjects\\konan\\rd\\mcal_test.p', 'rb') )
nysecal = list(nyse.index.date)


assert( ib.account_name == 'DU603835') 
assert( ib.port == 7497 ) 
assert( ib.client_id == 100 ) 


def create_contract(symbol, secType, exchange, currency,
                    right = None, strike = None, expiry = None,
                    multiplier = None, tradingClass = None):
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


#ib = broker.IBDataBroker()
#ib.connect()

ib = broker.IBBrokerTotal()

if( not ib.connected() ):
    ib.connect()

ib.account_name

#ib.tws.reqMktData()

#ib.getDataAtTime(type_data='MIDPOINT')


''' MOMENTUM GUARD '''

pos = ib.getPositions()

hedgeInstrument = 'SPY'
            
for key, position in pos.iterrows():
    
    if (position['Symbol'] == hedgeInstrument):
        continue
    
    sgn = np.sign( position['Number_of_Units'] )
    ticker = ( position['Symbol'] )
    
    if(sgn!=0):
        
        ''' Check if returns have moved against us '''           
        contract = ib.createContract(ticker=ticker, instrument_type=position['Financial_Instrument'])
        
        todayOpen = datetime.datetime.now().replace( hour=9, minute=30 )        
        
        
        idx = utils.find_date_in_list(calendar=nysecal, 
                                      target_date=datetime.date.today(), 
                                      move=0)
        
        prevClose = datetime.datetime.combine( nysecal[idx-1], datetime.time(15,59) )

        
        prevClosePrice = ib.getDataAtTime( type_data='MIDPOINT', 
                                     contract = contract,
                                     data_time = prevClose,
                                     bar_size='1 secs'
                                     )['close'].iloc[-1]
        
        
        todayOpenPrice = ib.getDataAtTime( type_data='MIDPOINT', 
                                     contract = contract,
                                     data_time = todayOpen,
                                     bar_size='1 secs'
                                     )['close'].iloc[-1]
        
        interDayRtns = ( todayOpenPrice -  prevClosePrice ) / prevClosePrice
        
        print ticker, interDayRtns
                
#        if ( interDayRtns <= 0. ):            
#            ib.closePosition(symbol=ticker, order_type='MARKET')
            
ib.disconnect()


''' HEDGE POSITIONS '''

dW = 3500

hedgeInstrument = 'SPY'

out = ib.getPositions()

shorts = out[ (out['Number_of_Units']<0) & (out['Symbol']!= hedgeInstrument) ]        
longs = out[ (out['Number_of_Units']>0) & (out['Symbol']!= hedgeInstrument) ]


# Here is a more exact way of hedging

shortExp, longExp = 0, 0

for row, stk in shorts.iterrows():    

    shortContract = ib.createContract(ticker=stk['Symbol'], instrument_type='STK')    
    avgPrice = ib.getDataAtTime( type_data='MIDPOINT', 
                             contract = shortContract, 
                             data_time=datetime.datetime.now(),
                             bar_size='1 secs'
                             )['close']    
    
    shortExp = shortExp + stk['Number_of_Units']*avgPrice
    

for row, stk in longs.iterrows():    
    longContract = ib.createContract(ticker=stk['Symbol'], instrument_type='STK')    
    avgPrice = ib.getDataAtTime( type_data='MIDPOINT', 
                             contract = longContract, 
                             data_time=datetime.datetime.now(),
                             bar_size='1 secs'
                             )['close']    
    longExp = longExp + stk['Number_of_Units']*avgPrice


#netExposure = ( longs.shape[0] -  shorts.shape[0] )

desiredFinalExposure = -( longExp + shortExp )
hedgePosition = out[ out['Symbol']== hedgeInstrument  ]
hedgeContract = ib.createContract(ticker=hedgeInstrument, instrument_type='STK')


avgPrice = ib.getDataAtTime( type_data='MIDPOINT', 
                         contract = hedgeContract, 
                         data_time=datetime.datetime.now(),
                         bar_size='1 secs'
                         )['close']
        
    
currentHedgeExp = ( hedgePosition['Number_of_Units']*avgPrice ).values[0]

delta_stkExposureReq = int( ( desiredFinalExposure - currentHedgeExp ) / avgPrice )  #units of stocks

action = { 1: 'BUY', -1: 'SELL' }

order_id = ib.nextOrderId()    

if (delta_stkExposureReq !=0):
   
    order_id = order_id + 1    

    hedgeTrade = action[ np.sign(delta_stkExposureReq) ]    

    hedge_order = ib.createOrder( trade_type=hedgeTrade, amount_units=(abs(delta_stkExposureReq)), order_type='MARKET' )    
    
    ib.placeOrder(order_id=order_id, 
                  contract=hedgeContract, 
                  order=hedge_order)



''' CLOSE OUT SOME POSITIONS '''

#ib.closeAllPositions(order_type='MARKET')

ib = broker.IBBrokerTotal()

ib.disconnect()
if( not ib.connected() ):
    ib.connect()
    
out = ib.getPositions()

hedgeContract = ib.createContract(ticker='SPY', instrument_type='STK')
hedge_order = ib.createOrder( trade_type='BUY', amount_units=1000, order_type='MARKET' )    

order_id = ib.nextOrderId()+1
ib.placeOrder(order_id=order_id, contract=hedgeContract, order=hedge_order)



#ib.closePosition(symbol='GOOG', order_type='MARKET')

#
#ib.connected()

#


'''
barsize:
    
1 secs, 5 secs, 10 secs, 15 secs, 30 secs, 1 min, 2 mins, 3 mins, 5 mins, 10 mins, 15 mins, 20 mins, 30 mins, 1 hour, 2 hours, 3 hours, 4 hours, 8 hours, 1 day, 1W, 1M"
'''

#
#c = ib.createContract(ticker = 'GOOG', instrument_type = 'STK')
#
#time_end = "20170222 9:30:00"
#duration = "60 S"
#bar = '1 min'
#_id=3
#
#ib._resetCallbackAttribute('historical_Data')
#
#ib.tws.reqHistoricalData( tickerId = _id,
#                         contract = c,
#                         endDateTime = time_end ,
#                         durationStr = duration,
#                         barSizeSetting = bar, whatToShow = 'BID',
#                         useRTH = 0, formatDate = 1)
#
#data = pd.DataFrame(ib.callback.historical_Data, columns = ["reqId",
#                                                                "date", "open",
#                                                                "high", "low",
#                                                                "close",
#                                                                "volume",
#                                                                "count", "WAP",
#                                                                "hasGaps"])
#
#data.drop(data.index[-1], inplace=True)
#data['date'] = data['date'].apply(parse)
#data.set_index('date', inplace=True)
#
#
#
#ib.tws.eDisconnect()