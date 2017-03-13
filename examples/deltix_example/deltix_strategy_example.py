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
import datetime as dt
import time
import numpy as np
import utils
import pickle
# NOT USED
# import random

# internal/custom imports
import konan.api.broker as broker
import konan.api.strategy as strategy
# NOT USED
# import konan.api.position as position

# object imports
import deltix_algorithm_example

# TODO: implement portfolio API
# import <portfolio>
# import portfolio_example

nyse = pickle.load( open('./rd/mcal_test.p', 'rb') )

nysecal = list(nyse.index.date)

# Create a child class that inherits from the base <strategy> class
# and rename appropriately for system import purposes
class deltixStrategy(strategy.Strategy):
    """
    """
    def __init__(self, broker = broker.IBBrokerTotal(),
                    time_execution = dt.datetime.now().time(),
                    time_end = dt.time(hour = 16, minute = 30), time_sleep = 30):
                    # time_execution = dt.time(hour = 9, minute = 30

        decision_algorithm = deltix_algorithm_example.deltixAlgorithm()
        portfolio = None #portfolio_example.examplePortfolio()

        time_format = '%H:%M:%S.%f' # NOT USED

        time_stamp_open_day = '09:30:00.0'
        time_stamp_close_day = '15:55:00.0'

        action_arguments_none = None

        open_day = self.openDay
        #hedge_one = self.hedgePositions
        #momentum_guard = self.momentumGuard
        end_day = self.endDay
        #test_connection = self.testConnection

        # TODO: MAP & ZIP HERE
        event_schedule = {time_stamp_open_day: (open_day, action_arguments_none),
                            time_stamp_close_day: (end_day, action_arguments_none)}
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
        # LOAD DATA
        WSHdata = self.decision_algorithm.getData(dataType='WSH', date=date)
        self.decision_algorithm.getData(dataType='WSHEarningsCalendar', date=date)
        self.decision_algorithm.getData(dataType='WSHCutoffCalendar', date=date)

        # UPDATE DATA
        self.decision_algorithm.constructEarningsCalendar(WSHdata, date)
        self.decision_algorithm.generatePositionsForClose(WSHdata, date)
        self.decision_algorithm.pickleCalendars()

        self.momentumGuard()
        self.hedgePositions()

    def endDay(self):
        date = dt.date.today()

        closeDT = dt.datetime.combine( date, dt.time(15,55) ) #could just use time
        self.broker.closeAllPositions()
        self.enterNewPositions()
        self.hedgePositions( data_time=closeDT )

        self.decision_algorithm.scrubEarningsCalendar(date=date)

        self.decision_algorithm.pickleCalendars()

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
                todayOpen = dt.datetime.now().replace( hour=9, minute=30 )
                idx = utils.find_date_in_list(calendar=nysecal,
                                              target_date=dt.date.today(),
                                              move=0)
                prevClose = dt.datetime.combine( nysecal[idx-1], dt.time(16,00) )
                prevClosePrice = self.broker.getDataAtTime( type_data='MIDPOINT',
                                             contract = contract,
                                             data_time = prevClose,
                                             bar_size='1 secs'
                                             )['close'].iloc[-1]
                todayOpenPrice = self.broker.getDataAtTime( type_data='MIDPOINT',
                                             contract = contract,
                                             data_time = todayOpen,
                                             bar_size='1 secs'
                                             )['close'].iloc[-1]
                interDayRtns = sgn*( todayOpenPrice -  prevClosePrice ) / prevClosePrice
                print(ticker, interDayRtns)

                if ( interDayRtns <= 0 ):
                    self.broker.closePosition(symbol=ticker, order_type='MARKET')

    def hedgePositions(self, data_time):
        ''' data_time would be the time we intend to hedge '''
        pos = self.broker.getPositions()
        shorts = pos[ (pos['Number_of_Units']<0) & (pos['Symbol']!= self.hedgeInstrument) ]
        longs = pos[ (pos['Number_of_Units']>0) & (pos['Symbol']!= self.hedgeInstrument) ]
        shortExp, longExp = 0, 0

        ''' Get short exposure '''
        for row, stk in shorts.iterrows():
            shortContract = self.broker.createContract(ticker=stk['Symbol'], instrument_type='STK')
            avgPrice = self.broker.getDataAtTime( type_data='MIDPOINT',
                                     contract = shortContract,
                                     data_time=data_time,
                                     bar_size='1 secs'
                                     )['close'].iloc[-1]
            shortExp = shortExp + stk['Number_of_Units']*avgPrice

        ''' Get long exposure '''
        for row, stk in longs.iterrows():
            longContract = self.broker.createContract(ticker=stk['Symbol'], instrument_type='STK')
            avgPrice = self.broker.getDataAtTime( type_data='MIDPOINT',
                                     contract = longContract,
                                     data_time=data_time,
                                     bar_size='1 secs'
                                     )['close'].iloc[-1]
            longExp = longExp + stk['Number_of_Units']*avgPrice

        ''' target exposure '''
        desiredFinalExposire = -( longExp + shortExp )
        hedgePosition = pos[ pos['Symbol']== self.hedgeInstrument  ]
        hedgeContract = self.broker.createContract(ticker=self.hedgeInstrument, instrument_type='STK')
        avgPrice = self.broker.getDataAtTime( type_data='MIDPOINT',
                                 contract = hedgeContract,
                                 data_time=data_time,
                                 bar_size='1 secs'
                                 )['close'].iloc[-1]
        currentHedgeExp = (hedgePosition['Number_of_Units']*avgPrice).values[0]
        delta_stkExposureReq = int( ( desiredFinalExposire - currentHedgeExp ) / avgPrice )  #units of stocks

        action = { 1: 'BUY', -1: 'SELL' }
        order_id = self.broker.nextOrderId()+1

        if (delta_stkExposureReq !=0):
            order_id = order_id + 1
            hedgeTrade = action[ np.sign(delta_stkExposureReq) ]
            hedge_order = self.broker.createOrder( trade_type=hedgeTrade, amount_units= int(abs(delta_stkExposureReq)), order_type='MARKET' )
            self.broker.placeOrder(order_id=order_id,
                                       contract=hedgeContract,
                                       order=hedge_order)

    def enterNewPositions(self):
        ''' This should be entered at the close '''
        order_id = self.broker.nextOrderId()+2

        for stk in self.decision_algorithm.bulls.keys():
            stk_ = stk.replace("."," ")
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

            order_id = order_id + 1

        for stk in self.decision_algorithm.bears.keys():
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

            order_id = order_id + 1
