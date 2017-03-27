"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
deltix_strategy_example.py
Created on 2017-03-03T13:35:00Z
@author:Joshua Hu
"""
# imports from future
from __future__ import print_function

#imports from stdlib
import sys

import datetime as dt
import time

import collections

import numpy as np
import os

import pickle
import pandas as pd

import traceback
# NOT USED
# import random

# internal/custom imports
import konan.api.broker as br
import konan.api.strategy as st
# NOT USED
# import konan.api.position as position

# object imports
#import deltix_algorithm_example
import konan.examples.deltix_example.deltix_algorithm_example as deltixAlgo

# TODO: implement portfolio API
# import <portfolio>
# import portfolio_example

if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    pass
elif sys.platform == "darwin":
    # OS X: Josh
    nyse = pickle.load( open('./rd/mcal_test.p', 'rb') )
    nysecal = list(nyse.index.date)
elif sys.platform == "win32":
    # Windows: Ray
    import utils
    import utils.paths as utp

    dropbox = utp.dropbox_path().path
    google_drive = utp.google_drive_path().path

    nyse = pickle.load( open(google_drive+"myPythonprojects\\konan\\rd\\mcal_test.p", 'rb') )
    nysecal = list(nyse.index.date)
    
    
def getID():
    time.sleep(0.2)
    dt_ = dt.datetime.now()    
#    strID = "".join( (str(dt_.year)[-2:], str(dt_.month), str(dt_.day), str(dt_.hour), str(dt_.minute), str(dt_.second), str(dt_.microsecond)[0:1]) )
    strID = "".join( (str(dt_.month), str(dt_.day), str(dt_.hour), str(dt_.minute), str(dt_.second), str(dt_.microsecond)[0:1]) )
    return (int(strID))
    
    

# Create a child class that inherits from the base <strategy> class
# and rename appropriately for system import purposes
class deltixStrategy(st.Strategy):
    """
    """
    def __init__(self, broker = None,
                    time_execution = dt.datetime.now().time(),
                    time_end = dt.time(hour = 16, minute = 30), time_sleep = 30):
        decision_algorithm = deltixAlgo.deltixAlgorithm()
        portfolio = None #portfolio_example.examplePortfolio()

        self.time_stamp_open_day = '09:30:00.0'
        self.time_stamp_close_day = '15:45:00.0'
#        self.time_stamp_close_day = '10:53:00.0'
#        self.time_stamp_close_day = '13:02:0.0'

        action_arguments_none = None

        has_executed = False

        open_day = self.openDay
        #hedge_one = self.hedgePositions
        #momentum_guard = self.momentumGuard
        end_day = self.endDay
        #test_connection = self.testConnection

        # TODO: MAP & ZIP HERE
        dict_event_schedule = {  self.time_stamp_open_day: [open_day, action_arguments_none, has_executed],
                            self.time_stamp_close_day: [end_day, action_arguments_none, has_executed]}

        event_schedule = collections.OrderedDict(sorted(dict_event_schedule.items(), key = lambda x: x[0]))

        print("Event schedule: ", event_schedule)

#        event_schedule = { self.time_stamp_close_day: [end_day, action_arguments_none, has_executed] }

        # TODO: argument mapping is not finished

        super(deltixStrategy, self).__init__(broker = broker,
                                                decision_algorithm = decision_algorithm,
                                                portfolio = portfolio,
                                                time_execution = time_execution,
                                                time_end = time_end,
                                                time_sleep = time_sleep,
                                                event_schedule = event_schedule)

        self.dW = 1000 # position size
        self.hedgeInstrument = 'SPY'

    #create specific actions groups below contstructor in function form
    def testConnection(self):
        if self.broker.connected():
            print('IS CONNECTED')
            self.broker.disconnect()
            print('DISCONNECTED')
        self.broker.connect()
        print('CONNECTED')

    def openDay(self, thing = None):
        date = dt.date.today()

        openM = int(self.time_stamp_open_day.split(":")[1])
        openH = int(self.time_stamp_open_day.split(":")[0])

        openDT = dt.datetime.combine( date, dt.time(openH,openM) ) #could just use time

        # LOAD DATA
        print('Loading WSH data for today')
        WSHdata = self.decision_algorithm.getData(dataType='WSH', date=date)
        print('Loading last saved Earnings Calendar')
        self.decision_algorithm.getData(dataType='WSHEarningsCalendar', date=date)
        print('Loading last saved cutoff calendar')
        self.decision_algorithm.getData(dataType='WSHCutoffCalendar', date=date)

        # UPDATE DATA
        print('Update earnings calendar')
        self.decision_algorithm.constructEarningsCalendar(WSHdata, date)
        print('Generate positions')
        self.decision_algorithm.generatePositionsForClose(WSHdata, date)
        print("Tentative entries:")
        print("TO LONG:")
        print(self.decision_algorithm.bulls)
        print("TO SHORT:")
        print(self.decision_algorithm.bears)

        print('Pickling earnings calendar')
        self.decision_algorithm.pickleCalendars()

        print('Momentum Guard')
        self.momentumGuard()
        print('Hedge positions')
        self.hedgePositions(data_time=openDT)
        
        
        

    def endDay(self):
        date = dt.date.today()

        closeM = int(self.time_stamp_close_day.split(":")[1])
        closeH = int(self.time_stamp_close_day.split(":")[0])

        closeDT = dt.datetime.combine( date, dt.time(closeH,closeM) ) #could just use time

        print('Close all positions')
        self.broker.closeAllTypePositions(order_type='MARKET', instruments=['STK'], exclude_symbol=['SPY'])
        print('Enter new positions')
        self.enterNewPositions()
        print('Hedge positions')
        self.hedgePositions( data_time=closeDT )

        print('Scrub earnings calendar')
        #self.decision_algorithm.scrubEarningsCalendar(date=date)

        print('Pickling calendar')
        #self.decision_algorithm.pickleCalendars()
                
        print('Record today PL ')
        performancepath = google_drive+'myPythonProjects\\papertrader\\papar252\\performance\\Deltix\\'
        self.broker.recordPNLToday( path=os.path.join(performancepath, str(date)+"positionPNL.csv" ) )
        self.broker.recordPNLDailyPerformance( path=os.path.join(performancepath, "deltixAggregatedPNL.csv" ) )
                
        

    def momentumGuard(self):
        pos = self.broker.getPositions()

        for key, position_ in pos.iterrows():
            if (position_['Symbol'] == self.hedgeInstrument):
                continue

            sgn = np.sign( position_['Number_of_Units'] )
            ticker = ( position_['Symbol'] )

            if(sgn!=0):
                ''' Check if returns have moved against us '''
                contract = self.broker.createContract(ticker=ticker, instrument_type=position_['Financial_Instrument'])
                #todayOpen = dt.datetime.now().replace( hour=9, minute=30,second=0 )
                idx = utils.find_date_in_list(calendar=nysecal,
                                              target_date=dt.date.today(),
                                              move=0)
                prevClose = dt.datetime.combine( nysecal[idx-1], dt.time(16,0,0) )                                                
                prevClosePrice = self.broker.getDataAtTime( type_data='MIDPOINT',
                                             contract = contract,
                                             data_time = prevClose,
                                             bar_size='1 secs'
                                             )['close'].iloc[-1]
                
                
                print(ticker, prevClosePrice)
#                prevClose = self.broker.getDailyData(ticker, provider='yahoo', date_start=nysecal[idx-1], date_end=nysecal[idx-1] )
#                prevClosePrice = prevClose['Adj Close'].values[0]
                                                           
                liveData = self.broker.getLiveMarketData(contract=contract)
                                
                askPrice = liveData['price'][ liveData['Type']=='ASK PRICE' ].values[0]
                bidPrice = liveData['price'][ liveData['Type']=='BID PRICE' ].values[0]
                
                todayOpenPrice = ( askPrice +bidPrice )*0.5 #mid point
#                todayOpenPrice = self.broker.getDataAtTime( type_data='MIDPOINT',
#                                             contract = contract,
#                                             data_time = todayOpen,
#                                             bar_size='1 secs'
#                                             )['close'].iloc[-1]
                                
                interDayRtns = sgn*( todayOpenPrice -  prevClosePrice ) / prevClosePrice
                print(ticker, interDayRtns)

                if ( interDayRtns <= 0 ):
                    self.broker.closePosition(symbol=ticker, order_type='MARKET')

    def hedgePositions(self, data_time):
        ''' data_time would be the time we intend to hedge '''
        pos = self.broker.getPositions()
        shorts = pos[ (pos['Number_of_Units']<0) & (pos['Symbol']!= self.hedgeInstrument) ]
        print("Shorts: ", shorts['Symbol'])
        longs = pos[ (pos['Number_of_Units']>0) & (pos['Symbol']!= self.hedgeInstrument) ]
        print("Longs: ", longs['Symbol'])
        shortExp, longExp = 0, 0

        ''' Get short exposure '''
        for row, stk in shorts.iterrows():
            shortContract = self.broker.createContract(ticker=stk['Symbol'], instrument_type='STK')
                        
#            avgPrice = self.broker.getDataAtTime( type_data='MIDPOINT',
#                                     contract = shortContract,
#                                     data_time=data_time,
#                                     bar_size='1 secs'
#                                     )['close'].iloc[-1]
                        
            liveData = self.broker.getLiveMarketData(contract=shortContract)
                                
            askPrice = liveData['price'][ liveData['Type']=='ASK PRICE' ].values[0]
            bidPrice = liveData['price'][ liveData['Type']=='BID PRICE' ].values[0]
            avgPrice = ( askPrice +bidPrice )*0.5 #mid point
                                                 
            shortExp = shortExp + stk['Number_of_Units']*avgPrice                        
            time.sleep(1)

        ''' Get long exposure '''
        for row, stk in longs.iterrows():
            
            longContract = self.broker.createContract(ticker=stk['Symbol'], instrument_type='STK')
            
            liveData = self.broker.getLiveMarketData( contract=longContract )
            askPrice = liveData['price'][ liveData['Type']=='ASK PRICE' ].values[0]            
            bidPrice = liveData['price'][ liveData['Type']=='BID PRICE' ].values[0]         
            
            avgPrice = ( askPrice +bidPrice )*0.5 #mid point
            
#            avgPrice = self.broker.getDataAtTime( type_data='MIDPOINT',
#                                     contract = longContract,
#                                     data_time=data_time,
#                                     bar_size='1 secs'
#                                     )['close'].iloc[-1]

            longExp = longExp + stk['Number_of_Units']*avgPrice
            time.sleep(1)

        ''' target exposure '''
        desiredFinalExposure = -( longExp + shortExp )
        print("Desired final exposure: ", desiredFinalExposure)

        hedgePosition = pos[ pos['Symbol']== self.hedgeInstrument  ]

        hedgeContract = self.broker.createContract(ticker=self.hedgeInstrument, instrument_type='STK')
#        avgPrice = self.broker.getDataAtTime( type_data='MIDPOINT',
#                                 contract = hedgeContract,
#                                 data_time=data_time,
#                                 bar_size='1 secs'
#                                 )['close'].iloc[-1]
        
        liveData = self.broker.getLiveMarketData( contract=hedgeContract )
        askPrice = liveData['price'][ liveData['Type']=='ASK PRICE' ].values[0]            
        bidPrice = liveData['price'][ liveData['Type']=='BID PRICE' ].values[0]         
        avgPrice = ( askPrice +bidPrice )*0.5 #mid point
       
        

        if( not hedgePosition.empty) :
            currentHedgeExp = (hedgePosition['Number_of_Units']*avgPrice).values[0]
            print("Current hedge exposure: ", currentHedgeExp)
        else:
            currentHedgeExp = 0

        delta_stkExposureReq = int( ( desiredFinalExposure - currentHedgeExp ) / avgPrice )  #units of stocks

        print ("Hedge required: ", delta_stkExposureReq, " stock units")

        action = { 1: 'BUY', -1: 'SELL' }
#        order_id = self.broker.nextOrderId()+1        
#        order_id = getID()
        order_id = self.broker.nextOrderId()

        if (delta_stkExposureReq !=0):
#            order_id = order_id + 1
            order_id = self.broker.nextOrderId()
            hedgeTrade = action[ np.sign(delta_stkExposureReq) ]
            hedge_order = self.broker.createOrder( trade_type=hedgeTrade, amount_units= int(abs(delta_stkExposureReq)), order_type='MARKET' )
            self.broker.placeOrder(order_id=order_id,
                                       contract=hedgeContract,
                                       order=hedge_order)
        elif ( (delta_stkExposureReq==0) and (desiredFinalExposure ==0) ):
#            order_id = order_id + 1
            order_id = self.broker.nextOrderId()
            self.broker.closePosition(symbol=self.hedgeInstrument , order_type='MARKET')


    def enterNewPositions(self):
        ''' This should be entered at the close '''
#        order_id = self.broker.nextOrderId()+2
        order_id = self.broker.nextOrderId()
            
        
        todayBulls = pd.Series()
        todayBears = pd.Series()
        
        # Get top 30 positions
               
        for stk in self.decision_algorithm.bulls.keys():
            
            
            ''' live Data '''
            contract = self.broker.createContract(ticker=stk, instrument_type='STK')
            liveData = self.broker.getLiveMarketData(contract=contract)                                
            askPrice = liveData['price'][ liveData['Type']=='ASK PRICE' ].values[0]
            bidPrice = liveData['price'][ liveData['Type']=='BID PRICE' ].values[0]
            
            todayClosePrice = ( askPrice +bidPrice )*0.5 #mid point
                        
            ''' prevClose '''            
            idx = utils.find_date_in_list(calendar=nysecal,
                                          target_date=dt.date.today(),
                                          move=0)
            prevClose = dt.datetime.combine( nysecal[idx-1], dt.time(16,0,0) )                                                
            prevClosePrice = self.broker.getDataAtTime( type_data='MIDPOINT',
                                         contract = contract,
                                         data_time = prevClose,
                                         bar_size='1 secs',                                         
                                         )['close'].iloc[-1]
                                    
            ''' Inter Close-Close returns '''
            todayBulls[stk] = (todayClosePrice - prevClosePrice) /prevClosePrice
            
#            print(stk, todayBulls[stk])
        
        
        for stk in self.decision_algorithm.bears.keys():
                    
            
            ''' live Data '''
            contract = self.broker.createContract(ticker=stk, instrument_type='STK')
            liveData = self.broker.getLiveMarketData(contract=contract)
                                
            askPrice = liveData['price'][ liveData['Type']=='ASK PRICE' ].values[0]
            bidPrice = liveData['price'][ liveData['Type']=='BID PRICE' ].values[0]
            
            todayClosePrice = ( askPrice +bidPrice )*0.5 #mid price
                        
            ''' prevClose '''            
            idx = utils.find_date_in_list(calendar=nysecal,
                                          target_date=dt.date.today(),
                                          move=0)
            prevClose = dt.datetime.combine( nysecal[idx-1], dt.time(16,0,0) )                                                
            prevClosePrice = self.broker.getDataAtTime( type_data='MIDPOINT',
                                         contract = contract,
                                         data_time = prevClose,
                                         bar_size='1 secs'
                                         )['close'].iloc[-1]
            
            ''' Inter Close-Close returns '''
            todayBears[stk] = (todayClosePrice - prevClosePrice) /prevClosePrice
            
        
        todayBulls.sort_values( inplace=True, ascending=True )
        todayBears.sort_values( inplace=True, ascending=False )
        
        
        
        ''' keep only the top 30 '''
        
        todayBears = todayBears.iloc[ :min(self.decision_algorithm.params[2], todayBears.size)]
        todayBulls = todayBulls.iloc[ :min(self.decision_algorithm.params[2], todayBulls.size)]       
        
        
        
        ''' List of tickers to remove '''
        # Bears
        popBear = []                
        for stk in self.decision_algorithm.bears.keys():            
            if stk not in todayBears.keys():
                popBear.append(stk)
        
        # Bulls
        popBull = []
        for stk in self.decision_algorithm.bulls.keys():
            if stk not in todayBulls.keys():
                popBull.append(stk)


        ''' Remove those not in top 30 '''
        for stk in popBull: 
            self.decision_algorithm.bulls.pop(stk, "None")
            
        for stk in popBear:
            self.decision_algorithm.bears.pop(stk, "None")
            
            
        print("Bears: ", self.decision_algorithm.bears)
        print("Bulls: ", self.decision_algorithm.bulls)


        for stk in self.decision_algorithm.bulls.keys():
            try:
                stk_ = stk.replace("."," ")
#                order_id = getID()
                order_id =self.broker.nextOrderId()
                print('Long: ', stk, order_id)
                c = self.broker.createContract(ticker=stk_,
                                                   instrument_type="STK",
                                                   primary_exchange ='NYSE')
                buy_order = self.broker.createDollarOrder(trade_type = 'BUY',
                                                             contract = c,
                                                             amount_dollars = self.dW,
                                                             order_type='MARKET' )  # default is market order
                self.broker.placeOrder(order_id, c, buy_order )

                time.sleep(1)
                self.broker.callback.order_Status
                time.sleep(1)
            except:
                print("error:", traceback.format_exc())
                continue


        for stk in self.decision_algorithm.bears.keys():

            try:
                stk_ = stk.replace("."," ")
                print('Short: ', stk, order_id)
                c = self.broker.createContract(ticker=stk_,
                                                   instrument_type="STK",
                                                   primary_exchange ='NYSE')
                sell_order = self.broker.createDollarOrder( trade_type = 'SELL',
                                                               amount_dollars = self.dW,
                                                               contract = c,
                                                               order_type='MARKET')  # default is market order
                time.sleep(1)
                self.broker.placeOrder( order_id, c, sell_order )
                time.sleep(1)
            except:
                continue

#            order_id = order_id + 1
            order_id = self.broker.nextOrderId()
