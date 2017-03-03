# -*- coding: utf-8 -*-


import konan.api.position as position
import konan.api.strategy as strategy
import testAlgorithm
import datetime
import time
import random
import numpy as np
import utils
import pickle


nyse = pickle.load( open('C:\\Users\\Ray\\Google Drive\\myPythonProjects\\konan\\rd\\mcal_test.p', 'rb') )

nysecal = list(nyse.index.date)



class deltixStrategy(strategy.Strategy):
    
    """
    CLASS PROPERTIES
    """
    
    def __init__ (self, execBroker, dataBroker):
        
        self.decision_algorithm = testAlgorithm.deltix()
        self.portfolio = None
        self.time_execution = None
        self.execBroker = execBroker
        self.dataBroker = dataBroker
        self.dW = 1000 # position size
        self.hedgeInstrument = 'SPY'
                
    
    def checkPortfolio(self):
        pass

    def checkDecision(self):
        pass

    def makeTrade(self,position = position.Position()):
        pass
    
    def updatePortfolio(self,position = position.Position()):
        pass

    def execute(self):
        
        date = datetime.date.today()
        
       
        ''' Get today's WSH data '''
        
        ''' ----------------- '''
        ''' Market OPEN EVENT '''
        ''' ----------------- '''
        
        # LOAD DATA
        WSHdata = self.decision_algorithm.getData(dataType='WSH', date=date)        
        earningsCal = self.decision_algorithm.getData(dataType='WSHEarningsCalendar', date=date)        
        cutoffCal = self.decision_algorithm.getData(dataType='WSHCutoffCalendar', date=date)
        
        # UPDATE DATA
        self.decision_algorithm.constructEarningsCalendar(WSHdata, date)        
        self.decision_algorithm.generatePositionsForClose(WSHdata, date)        
        self.decision_algorithm.pickleCalendars()
        
        self.momentumGuard()
        self.hedgePositions()
                
        ''' ------------------ '''
        ''' Market CLOSE EVENT '''
        ''' ------------------ '''
        closeDT = datetime.datetime.combine( date, datetime.time(15,55) ) 
        self.closeAllPositions()
        self.enterNewPositions()
        self.hedgePositions( data_time=closeDT )
        
        self.decision_algorithm.scrubEarningsCalendar(date=date)
        
        self.decision_algorithm.pickleCalendars()
        
        
    ''' # ========================================================= # '''    
        
    def momentumGuard(self):
        
        
        ''' # ========================================================= # '''    
        
        pos = self.execBroker.getPositions()

        for key, position_ in pos.iterrows():
            
            if (position_['Symbol'] == self.hedgeInstrument):
                continue
            
            sgn = np.sign( position_['Number_of_Units'] )
            ticker = ( position_['Symbol'] )
            
            if(sgn!=0):
                
                ''' Check if returns have moved against us '''           
                contract = self.execBroker.createContract(ticker=ticker, instrument_type=position_['Financial_Instrument'])
                
                todayOpen = datetime.datetime.now().replace( hour=9, minute=30 )                
                
                idx = utils.find_date_in_list(calendar=nysecal, 
                                              target_date=datetime.date.today(), 
                                              move=0)
                
                prevClose = datetime.datetime.combine( nysecal[idx-1], datetime.time(16,00) )
                        
                prevClosePrice = self.execBroker.getDataAtTime( type_data='MIDPOINT', 
                                             contract = contract,
                                             data_time = prevClose,
                                             bar_size='1 secs'
                                             )['close'].iloc[-1]
                
                
                todayOpenPrice = self.execBroker.getDataAtTime( type_data='MIDPOINT', 
                                             contract = contract,
                                             data_time = todayOpen,
                                             bar_size='1 secs'
                                             )['close'].iloc[-1]
                
                interDayRtns = sgn*( todayOpenPrice -  prevClosePrice ) / prevClosePrice
                
                print ticker, interDayRtns
                
                if ( interDayRtns <= 0 ):            
                    self.execBroker.closePosition(symbol=ticker, order_type='MARKET')
                

    
    ''' # ========================================================= # '''    
    
    def hedgePositions(self, data_time):
        ''' data_time would be the time we intend to hedge '''
        
        ''' # ========================================================= # '''    
        
        
        
        pos = self.execBroker.getPositions()
        
        shorts = pos[ (pos['Number_of_Units']<0) & (pos['Symbol']!= self.hedgeInstrument) ]        
        longs = pos[ (pos['Number_of_Units']>0) & (pos['Symbol']!= self.hedgeInstrument) ]
                
        shortExp, longExp = 0, 0
        
        ''' Get short exposure '''
        for row, stk in shorts.iterrows():    
            shortContract = self.execBroker.createContract(ticker=stk['Symbol'], instrument_type='STK')    
            
            avgPrice = self.execBroker.getDataAtTime( type_data='MIDPOINT', 
                                     contract = shortContract, 
                                     data_time=data_time,
                                     bar_size='1 secs'
                                     )['close'].iloc[-1]
            shortExp = shortExp + stk['Number_of_Units']*avgPrice
            
        ''' Get long exposure '''
        for row, stk in longs.iterrows():    
            longContract = self.execBroker.createContract(ticker=stk['Symbol'], instrument_type='STK')    
            
            avgPrice = self.execBroker.getDataAtTime( type_data='MIDPOINT', 
                                     contract = longContract, 
                                     data_time=data_time,
                                     bar_size='1 secs'
                                     )['close'].iloc[-1]
            
            longExp = longExp + stk['Number_of_Units']*avgPrice
        
        
        ''' target exposure '''
        desiredFinalExposire = -( longExp + shortExp )
        hedgePosition = pos[ pos['Symbol']== self.hedgeInstrument  ]
        hedgeContract = self.execBroker.createContract(ticker=self.hedgeInstrument, instrument_type='STK')
        
        
        avgPrice = self.execBroker.getDataAtTime( type_data='MIDPOINT', 
                                 contract = hedgeContract, 
                                 data_time=data_time,
                                 bar_size='1 secs'
                                 )['close'].iloc[-1]

            
        currentHedgeExp = (hedgePosition['Number_of_Units']*avgPrice).values[0]
        delta_stkExposureReq = int( ( desiredFinalExposire - currentHedgeExp ) / avgPrice )  #units of stocks
        
        action = { 1: 'BUY', -1: 'SELL' }
        
        order_id = self.execBroker.nextOrderId()+1 
        
        if (delta_stkExposureReq !=0):           
            order_id = order_id + 1    
            hedgeTrade = action[ np.sign(delta_stkExposureReq) ]    
            hedge_order = self.execBroker.createOrder( trade_type=hedgeTrade, amount_units= int(abs(delta_stkExposureReq)), order_type='MARKET' )    
            self.execBroker.placeOrder(order_id=order_id, 
                                       contract=hedgeContract, 
                                       order=hedge_order)

        
    
    ''' # ========================================================= # '''    
    
    def enterNewPositions(self):
        ''' This should be entered at the close '''
        
        ''' # ========================================================= # '''            
        
            
        order_id = self.execBroker.nextOrderId()+2
        
        for stk in self.decision_algorithm.bulls.keys():                    
            
            stk_ = stk.replace("."," ")                        
            print 'Long: ', stk, order_id            
            c = self.execBroker.createContract(ticker=stk_, 
                                               instrument_type="STK", 
                                               primary_exchange ='NYSE')
            
            buy_order = self.execBroker.createDollarOrder(trade_type = 'BUY',
                                                         contract = c,
                                                         amount_dollars = self.dW, 
                                                         order_type='MARKET' )  # default is market order                                

            self.execBroker.placeOrder(order_id, c, buy_order )                                      

            time.sleep(1)            
            self.execBroker.callback.order_Status            
            time.sleep(1)
            
            order_id = order_id + 1
            
                
        for stk in self.decision_algorithm.bears.keys():  
                      
            stk_ = stk.replace("."," ")              
            print 'Short: ', stk, order_id                        
            c = self.execBroker.createContract(ticker=stk_, 
                                               instrument_type="STK", 
                                               primary_exchange ='NYSE')

            sell_order = self.execBroker.createDollarOrder( trade_type = 'SELL', 
                                                           amount_dollars = self.dW,
                                                           contract = c,
                                                           order_type='MARKET')  # default is market order            
            
            time.sleep(1)                       
            self.execBroker.placeOrder( order_id, 
                                        c, 
                                        sell_order )                             
            time.sleep(1)
            
            order_id = order_id + 1


''' Testing if I can access the decision algorithm '''

##import pandas as pd
#deltixStrat = deltixStrategy()
#
#for _date in pd.date_range( datetime.date(2017,1,19), datetime.date(2017,3,3) ):
#   
#    date = _date.date()    
#    
#    print date
#    
#    WSHData = deltixStrat.decision_algorithm.getData(dataType='WSH', date=date)
#
#    deltixStrategy.decision_algorithm().constructEarningsCalendar(WSHData, date=date)    
#    deltixStrat.generatePositionsForClose(WSHData, date=date)
#    
#    #deltixStrat

    