# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 17:31:39 2017

@author: Ray
"""


# ------------------------------
# Position container
# ------------------------------
class position_(object):
    
    def __init__ (self, expiry=0, ID="", age=-1, wealth=1, entry_price=1, open_date=None, trade_type=1, num_units=0):

        self.open_date =open_date
        self.wealth = wealth
        self.trade_type = trade_type  # long/ short
        self.entry_price = entry_price
        self.age = -1 # When this reaches 5 it is a signal to close all positions.
        self.expiration = expiry
        self.ID = ID

        self.today_price = 0
        self.prev_price = 0
        self.today_PL = 0


        if( num_units == 0 and self.wealth!=0):
            self.num_units = self.trade_type * self.wealth /  self.entry_price

        if( num_units !=0 and self.wealth==0 ):
            self.wealth  = self.trade_type * self.num_units* self.entry_price

        if( num_units !=0 and self.wealth!=0 ):
            raise "Specify either the number of units or investment value"


    def updatePosition( self, wealth=1, entry_price=1, open_date=None, trade_type=1, num_units=np.nan ):

        self.open_date =open_date
        self.wealth = wealth
        self.trade_type = trade_type  # long/ short
        self.entry_price = entry_price

        if(num_units!= np.nan):
            self.num_units = num_units


    def setExpiration(self, T):
        self.expiration=T


    def setTodayPrice(self, today_price):
        self.today_price = today_price

    def setTodayPL(self, today_PL):
        self.today_PL = today_PL


# ------------------------------
# Position container for stock
# ------------------------------
class positionStk(position_):

    def __init__(self, expiry=0, ID="", age=-1, wealth=1, entry_price=1, open_date=None, trade_type=1, num_units=np.nan):

        position_.__init__ (self,
                            expiry=expiry,
                            age=age,
                            wealth=wealth,
                            entry_price=entry_price,
                            open_date=open_date,
                            trade_type=trade_type,
                            ID = ID
                            )


# ------------------------------
# Position container for futures
# ------------------------------
class positionFutures(position_):

    def __init__(self, expiry=0, ID="", age=-1, wealth=1, entry_price=1, open_date=None, trade_type=1, num_units=np.nan, mult=1 ):

        position_.__init__ (self,
                            expiry=expiry,
                            age=age,
                            wealth=wealth,
                            entry_price=entry_price,
                            open_date=open_date,
                            trade_type=trade_type,
                            ID = ID,
                            num_units=num_units
                            )

        self.cont_multiplier = mult


    def setMultiplier(self, mult):
        self.cont_multiplier = mult




#    def getPositionPL(self, today_price):
#        # self.exit price should be set
#        #self.setTodayPrice(today_price)
#
#        return self.trade_type*(self.today_price - self.prev_price)


# ------------------------------
# performance object
# ------------------------------

class performance(object):

    def __init__(self, portfolio=None, start_date=None, end_date=None, precision=6):

#        self.maxDD = 0
#        self.maxDDD = 0
#        self.calmar = 0
#        self.sharpe = 0
#        self.annualizedVol = 0
#        self.annualizedRets = 0

        self.start_date = start_date
        self.end_date = end_date
        self.precision = precision

        self.performance = {'maxDD': 0,
                                'maxDDD': 0,
                                'maxDDstart': 0,
                                'maxDDend': 0,
                                'Sharpe': 0,
                                'Calmar': 0,
                                'annualizedVol': 0,
                                'annualizedRets': 0,
                                'finalRets' : 0
                                }
        if (portfolio==None):
            pass
        else: # it's a portfolio object
            portfolio.calcRets()
            portfolio.calcCumRets()
            portfolio.calcRets()


            if( start_date ==None ):
                self.start_date = portfolio.rets.index[0]
            else:
                self.start_date = start_date

            if( end_date == None ):
                self.end_date = portfolio.rets.index[-1]
            else:
                self.end_date = end_date


#            self.calcSharpe(portfolio)   # Sharpe
#            self.calcDrawDown(portfolio) # Drawdown
#            self.calcCalmar(portfolio) # Drawdown

            self.customAnalytics(portfolio)

            self.performance['finalRets'] = portfolio.cum_rets[-1]

            # round to 6 digits
            # --------------------------
            def myRound(x, precision=1):
            # --------------------------
                try:
                    return [ round(x, precision) ]
                except:
                    return [x]

            self.performance.update( (x, myRound(y,self.precision)  )  for x, y in self.performance.items()  )



    # Abstract class?
    def customAnalytics(self, portfolio):
        self.calcSharpe(portfolio)   # Sharpe
        self.calcDrawDown(portfolio) # Drawdown
        self.calcCalmar(portfolio) # Drawdown
        self.calcWinLossPct(portfolio)



    def calcSharpe(self, portfolio, frequency="daily", rf_rate=0.):
        fac=252
        if(frequency=="daily"):
            fac=252


        rets = portfolio.rets.loc[self.start_date:self.end_date]

        meanexcess = rets.mean()*fac - rf_rate
        volatility= np.sqrt(fac)*rets.std()

        self.performance['annualizedRets'] = rets.mean()*fac
        self.performance['annualizedVol'] = rets.std()*np.sqrt(fac)

        self.performance['Sharpe'] =  meanexcess/volatility


    def calcDrawDown(self,portfolio):
        #import generate_trading_days

        cum_rets = portfolio.cum_rets.loc[self.start_date:self.end_date]

        dates = cum_rets.index.values

        highwatermark = pd.Series(data=0, index=dates)
        drawdown = pd.Series(data=0, index=dates)
        drawdownduration = pd.Series(data=0, index=dates)

        for i in np.arange( 1, cum_rets.size ):
            highwatermark.iloc[i]= max( highwatermark.iloc[i-1], cum_rets.iloc[i] )
            drawdown.iloc[i] = (1.+ cum_rets.iloc[i])/ ( 1+highwatermark.iloc[i] ) - 1.

            if ( drawdown.iloc[i]==0 ):
                drawdownduration.iloc[i]=0.
            else:
                drawdownduration.iloc[i] = drawdownduration.iloc[i-1]+1


        self.performance['maxDD'] =  drawdown.min(0)
        self.performance['maxDDD'] = int(drawdownduration.max())


        oneday = datetime.timedelta(days=1)

        self.performance['maxDDend'] = drawdownduration.argmax()
        self.performance['maxDDstart'] = self.performance['maxDDend'] - int(self.performance['maxDDD'])*oneday

        self.performance['maxDDstart'] = str( self.performance['maxDDstart'] )
        self.performance['maxDDend'] = str( self.performance['maxDDend'] )



    # ----------------------------------
    # Calculate  Calmar
    # ----------------------------------
    def calcCalmar( self, portfolio, fac=252 ):

        # anualized returns using all data
        nDays = portfolio.cum_rets.size

        #if (nDays < fac*3):
        maxAnnualizedRets = (1.+ portfolio.cum_rets.iloc[-1] )**(float(fac)/ nDays) - 1.


        print maxAnnualizedRets

        #self.performance['Calmar'] = maxAnnualizedRets / max( abs(self.performance['maxDD']), 1.)
        try:
            self.performance['Calmar'] = maxAnnualizedRets / abs(self.performance['maxDD'] )
        except:
            raise
            print "maxDD is", self.performance['maxDD']


    def calcWinLossPct(self, portfolio):
        nDays = float( portfolio.rets.size  )
        self.performance['win%'] = portfolio.rets[ portfolio.rets>0 ].size /  nDays
        self.performance['loss%'] = 1. - self.performance['win%']


''' ==============================================================
#
# PORTFOLIO OBJECT
#
 ================================================================= '''

class portfolio(object):

    ''' ==================== '''
    def __init__(self, date=None, init_wealth = 0):
        ''' ==================== '''



        self.time = { 'Close': '1600', 'Open': '0930'  }


        self.position_list = []  # should be a list of positionStk objects
        self.position_dict = {}  # should be a list of positionStk objects
        self.NAV = pd.Series()
        self.rets = pd.Series()
        self.Wo = init_wealth
        self.open_date = date
        self.NAV[self.open_date] = self.Wo
        self.transaction_cost = 0.0005
        self.fixedTcost = 0.0

        self.bulls = []
        self.bears = []
        self.tickers = []
        self.exit_positions = []

        self.net_exposure = 0
        self.cum_rets = pd.Series()
        self.rets = pd.Series()
        self.dailyPL = pd.Series()

        self.dailyPositions = pd.DataFrame(columns=['numPositions', 'bears', 'bulls', 'positionRets', 'netExposure'])
        self.performance = {}

    ''' ==================== '''
    def setWealth(self, Po):
        ''' ==================== '''
        self.Wo = Po

    ''' ==================== '''
    def markPosToMarket(self,  mark_date=None, PL=0): # assuming a positionStk object
        ''' ==================== '''

        #print self.NAV.index.get_loc(date)
        #positionPL = position.getPositionPL( price )
        self.NAV[mark_date] = self.NAV[mark_date] + PL

    ''' ==================== '''
    def openPosition(self, position, open_date):
        ''' ==================== '''
        ''' % Open position
            % Take transaction cost into consideration '''

        self.position_list.append(position)
        try:
            self.NAV[open_date] = self.NAV[open_date] - abs(position.wealth) * self.transaction_cost
        except:
            print "No key in NAV on: ", open_date
            pass

    ''' ==================== '''
    def openPositionD(self, position, open_date):
        ''' ==================== '''
        ''' % Open position
            % Take transaction cost into consideration '''

        self.position_dict[position.ID] = position

        try:
            self.NAV[open_date] = self.NAV[open_date] - abs(position.wealth) * self.transaction_cost
        except:
            print "No key in NAV on: ", open_date
            pass

    ''' ==================== '''
    def closePosition(self, position, close_date):
        ''' ==================== '''
        ''' % Close position
            % Take transaction cost into consideration '''

        self.NAV[close_date] = self.NAV[close_date] - abs(position.wealth) * self.transaction_cost
        try:
            self.position_list.remove(position)
        except:
            print "No key in NAV on: ", close_date
            pass

    ''' ==================== '''
    def closePositionD(self, position, close_date):
        ''' ==================== '''
        ''' % Close position
            % Take transaction cost into consideration '''

        self.NAV[close_date] = self.NAV[close_date] - abs(position.wealth) * self.transaction_cost
        try:
            #self.position_list.remove(position)
            #self.position_dict.pop( position.ID )

            del self.position_dict[ position.ID ]

        except:
            print "No key in NAV on: ", close_date
            pass



    ''' ==================== '''
    def openMultiplePositions( self, position_dict=None, trade_type=1, priceData=None, open_date=None, expiry=0, OHLC='Open', execs=True, fp=None ):
         # homogenous expiry
        # Note that we do not open a position if it already exists
        # all longs or all shorts
        ''' ==================== '''
        a = { 1: 'Buy', -1: 'Sell' }

        counterPF = { 1: self.bulls, -1: self.bears }

        for stk in position_dict.keys():
            if stk not in self.tickers:
                # Create new position
                try:
                    entryprice = priceData[stk][OHLC].loc[open_date]

                    try:
                        wealth = position_dict[stk][0]
                    except:
                        wealth = position_dict[stk]

                    new_position = positionStk( expiry=expiry,
                                                ID=stk,
                                                wealth=wealth,
                                                entry_price=entryprice,
                                                open_date=open_date,
                                                trade_type=trade_type )

                    self.openPosition( new_position, open_date )
                    if(execs):
                        try:
                            utf.writeLine( filePointer=fp, fields=(str(open_date), self.time[OHLC], stk, position_dict[stk][0] , a[trade_type], position_dict[stk][1], position_dict[stk][2]) )
                        except:
                            utf.writeLine( filePointer=fp, fields=(str(open_date), self.time[OHLC], stk, position_dict[stk] , a[trade_type]) )
                except:
                   # raise
                    print open_date, stk, "price not found"


            ''' Reverse positions '''
            if stk in counterPF[-trade_type]:
                for position in self.position_list:
                    if ( position.ID == stk ):
                        try:
                           entryprice = priceData[stk][OHLC].loc[open_date] # Ticker may be accounced before price exists?

                           position.updatePosition( wealth = -position.wealth,
                                                   entry_price = entryprice,
                                                   num_units = -position.num_units,
                                                   trade_type = -position.trade_type,
                                                   open_date = open_date
                                                   )
                           self.NAV[open_date] = self.NAV[open_date] - 2*position.wealth*self.transaction_cost

                           if(execs):
                               utf.writeLine( filePointer=fp, fields=(str(open_date), self.time[OHLC], stk, 2*position_dict[stk][1] , a[-trade_type], position_dict[stk][1], position_dict[stk][2], "reposition") )


                           print "Reposition occured on ", open_date
                        except:
                           pass


    ''' ==================== '''
    def openMultiplePositionsD( self, position_dict=None, trade_type=1, priceData=None, open_date=None, expiry=0, OHLC='Open', execs=True, fp=None ):
         # homogenous expiry
        # Note that we do not open a position if it already exists
        # all longs or all shorts
        ''' ==================== '''
        a = { 1: 'Buy', -1: 'Sell' }

        counterPF = { 1: self.bulls, -1: self.bears }

        for stk in position_dict.keys():
            if stk not in self.tickers:
                # Create new position
                try:
                    entryprice = priceData[stk][OHLC].loc[open_date]

                    try:
                        wealth = position_dict[stk][0]
                    except:
                        wealth = position_dict[stk]

                    new_position = positionStk( expiry=expiry,
                                                ID=stk,
                                                wealth=wealth,
                                                entry_price=entryprice,
                                                open_date=open_date,
                                                trade_type=trade_type )

                    self.openPosition( new_position, open_date )
                    if(execs):
                        try:
                            utf.writeLine( filePointer=fp, fields=(str(open_date), self.time[OHLC], stk, position_dict[stk][0] , a[trade_type], position_dict[stk][1], position_dict[stk][2]) )
                        except:
                            utf.writeLine( filePointer=fp, fields=(str(open_date), self.time[OHLC], stk, position_dict[stk] , a[trade_type]) )
                except:
                    print open_date, stk, "price not found"
                    # raise

            ''' Reverse positions '''
            if stk in counterPF[-trade_type]:
                try:
                    self.position_dict[stk]
                except:
                    print stk, "not in position_dict"
                    break

                try:
                    entryprice = priceData[stk]['Close'].loc[open_date] # Ticker may be accounced before price exists?
                except:
                    print stk, "price not found"
                    break
                self.position_dict[stk].updatePosition( wealth = -position.wealth,
                                                       entry_price = entryprice,
                                                       num_units = -position.num_units,
                                                       trade_type = -position.trade_type,
                                                       open_date = open_date
                                                       )
                self.NAV[open_date] = self.NAV[open_date] - 2*position.wealth*self.transaction_cost

                if(execs):
                    utf.writeLine( filePointer=fp, fields=(str(open_date), stk, 2*position_dict[stk][1] , a[-trade_type], position_dict[stk][1], position_dict[stk][2], "reposition") )

                print "Reposition occured on ", open_date





    # !!! Not universal because of Ernie's imprecise hedging mechanism
    ''' ==================== '''
    def resizePosition( self, priceData=None, ticker="", open_date=None, new_wealth=1, OHLC='Close', trade_type=0., fp=None, execs=True, adjustment=np.nan) :
        ''' ==================== '''

        action = {1: 'Buy' , -1: 'Sell'}
        #revAction = {'Buy': 1 , 'Sell': -1 }

        entry_price = priceData[ticker][OHLC].loc[open_date]

        found = False
        for position in self.position_list:

            if( position.ID == ticker ): # reposition this ticker

                found = True

                #old_wealth = self.dailyPositions['netExposure'].iloc[-2] # has sign
                #old_wealth = self.dailyPositions['netExposure'].iloc[-2] # has sign

                #print open_date, adjustment

                if ( np.isnan(adjustment) ):

                    deltaPositionWealth = (self.dailyPositions['netExposure'].iloc[-1] - self.dailyPositions['netExposure'].iloc[-2] )
                    adjustment = -deltaPositionWealth

                if( adjustment==0 ):
                    break

                #action_sign = np.sign(delta_wealth) # For exec writing
                action_sign = np.sign(adjustment) # For exec writing

#                shares_purchased = (delta_wealth) / entry_price   # For exec writing

                position.updatePosition( wealth = new_wealth,
                         entry_price = entry_price,
                         open_date = open_date,
                         trade_type = trade_type,
                         num_units = position.trade_type * position.wealth / entry_price
                        )

                #self.NAV[open_date] = self.NAV[open_date] - abs(delta_wealth)*self.transaction_cost
                self.NAV[open_date] = self.NAV[open_date] - abs(adjustment)*self.transaction_cost

                if(execs):
                    #utf.writeLine( filePointer=fp, fields=(str(open_date), ticker, abs(delta_wealth), action[ int(action_sign) ], "RESIZE HEDGE") )
                    utf.writeLine( filePointer=fp, fields=(str(open_date), self.time[OHLC],  ticker, int(abs(adjustment)), action[ int(action_sign) ], "RESIZE HEDGE") )

                break

        if (not found):
            print open_date, self.time[OHLC], "Position does not exist. Creating one now"
            if( abs(new_wealth) > 0.001):
                new_position = positionStk( expiry=0,
                                            ID=ticker,
                                            wealth=abs(new_wealth),
                                            entry_price=entry_price,
                                            open_date=open_date,
                                            trade_type = trade_type,
                                            )
                new_position.setTodayPrice( entry_price )
                self.openPosition( new_position, open_date )

                if(execs):
                    utf.writeLine( filePointer=fp, fields=(str(open_date),  self.time[OHLC],  ticker, new_wealth, action[trade_type], "CREATE HEDGE") )



    ''' ==================== '''
    def resizePositionD( self, priceData=None, ticker="", open_date=None, new_wealth=1, OHLC='Close', trade_type=0., fp=None, execs=True) :
        # Resize current position based on ticker
        # Also create a new position if it doesn't already exist
        ''' ==================== '''

        action = {1: 'Buy' , -1: 'Sell'}
        #revAction = {'Buy': 1 , 'Sell': -1 }

        entry_price = priceData[ticker][OHLC].loc[open_date]

        found = False

        try:
            self.position_dict[ticker]
            found = True
        except:

            if( abs(new_wealth) > 0.001):

                print "Position does not exist. Creating one now"

                new_position = positionStk( expiry = 0,
                                            ID = ticker,
                                            wealth = abs(new_wealth),
                                            entry_price = entry_price,
                                            open_date = open_date,
                                            trade_type = trade_type,
                                            )

                new_position.setTodayPrice( entry_price )

                self.openPosition( new_position, open_date )

                if(execs):
                    utf.writeLine( filePointer=fp, fields=(str(open_date), self.time[OHLC], ticker, new_wealth, action[trade_type], "CREATE HEDGE") )


        if( found ):
            old_wealth = self.dailyPositions['netExposure'].iloc[-2] # has sign

            self.position_dict[ticker].setTodayPrice(entry_price)

            # Wf - Wi
            delta_wealth =  int( trade_type*new_wealth - old_wealth ) # For exec writing and commission fee
            #print open_date, new_wealth, trade_type,  old_wealth, delta_wealth

            if( delta_wealth != 0 ):

                action_sign = np.sign(delta_wealth) # For exec writing
#                shares_purchased = (delta_wealth) / entry_price   # For exec writing

                position.updatePosition( wealth = new_wealth,
                         entry_price = entry_price,
                         open_date = open_date,
                         trade_type = trade_type,
                         num_units = position.trade_type * position.wealth / entry_price
                        )

                self.NAV[open_date] = self.NAV[open_date] - abs(delta_wealth)*self.transaction_cost

                if(execs):
                    utf.writeLine( filePointer=fp, fields=(str(open_date), self.time[OHLC], ticker, abs(delta_wealth), action[ int(action_sign) ], "RESIZE HEDGE") )





    ''' ==================== '''
    def markExistingPositionsInterCC(self, priceData=None, mark_date=None, prev_date=None, ignore_tickers=[]):
        ''' ==================== '''

        self.exit_positions = [] # auto reset

        for position in self.position_list:
            ''' interday position marking '''
            if(position.ID not in ignore_tickers): # don't age anything in the ignore list
                position.age = position.age +1

            ''' Extension of life '''
            if( (position.ID in self.dailyPositions['bears'].loc[mark_date] ) or (position.ID in self.dailyPositions['bulls'].loc[mark_date] ) and (position.ID not in ignore_tickers)  ):
            #if( (position.ID in self.dailyPositions['bears'].loc[mark_date] ) or (position.ID in self.dailyPositions['bulls'].loc[mark_date] )  ):
                position.expiration = position.expiration + 1


            try:
                position_PL = position.trade_type*( priceData[position.ID]['Close'].loc[mark_date] - priceData[position.ID]['Close'].loc[prev_date] )*abs(position.num_units)
            except:
                position_PL = 0

#
#            if( position.ID =='SPY'):
#                try:
#                    position_PL = position.trade_type*( priceData[position.ID]['Close'].loc[mark_date] - priceData[position.ID]['Open'].loc[mark_date] )*abs(position.num_units)
#                except:
#                    position_PL = 0


            #cumPL = cumPL + position_PL
            self.markPosToMarket( mark_date=mark_date, PL=position_PL  )

            #print position.ID, position.age, position.expiration

            position.wealth = position.wealth + position_PL # update position wealth
            # Close out expiring positions that are not in the new bulls and bears
            #if( (position.age == position.expiration) and (position.ID not in ignore_tickers) ) :
            if( (position.age == position.expiration) ) :
                self.exit_positions.append(position)



        ''' ==================== '''
    def markExistingPositionsInterCO(self, priceData=None, mark_date=None, prev_date=None, ignore_tickers=[]):
        ''' These should take a function that determines if we want to exit or not '''
        ''' The function acts on a position object  and returns true or false '''
        ''' % Do not age position '''
        ''' ==================== '''


        self.exit_positions = [] # auto reset
        for position in self.position_list:
            ''' interday position marking '''

            if(position.ID not in ignore_tickers): # don't age anything in the ignore list
                position.age = position.age +1

            ''' Extension of life '''
#            if( (position.ID in self.dailyPositions['bears'].loc[mark_date] ) or (position.ID in self.dailyPositions['bulls'].loc[mark_date] ) and (position.ID not in ignore_tickers)  ):
#            #if( (position.ID in self.dailyPositions['bears'].loc[mark_date] ) or (position.ID in self.dailyPositions['bulls'].loc[mark_date] )  ):
#                position.expiration = position.expiration + 1
            try:
                position_PL = position.trade_type*( priceData[position.ID]['Open'].loc[mark_date] - priceData[position.ID]['Close'].loc[prev_date] )*abs(position.num_units)
            except:
                position_PL = 0

#            if( position.ID =='SPY'):
#                try:
#                    position_PL = position.trade_type*( priceData[position.ID]['Close'].loc[mark_date] - priceData[position.ID]['Open'].loc[mark_date] )*abs(position.num_units)
#                except:
#                    position_PL = 0

            #cumPL = cumPL + position_PL
            self.markPosToMarket( mark_date=mark_date, PL=position_PL  )
            #print position.ID, position.age, position.expiration

            position.wealth = position.wealth + position_PL # update position wealth
            # Close out expiring positions that are not in the new bulls and bears
            #if( (position.age == position.expiration) and (position.ID not in ignore_tickers) ) :
            if ( position.age == position.expiration ) :
                self.exit_positions.append(position)


            ''' ==================== '''
    def markExistingPositionsInterOC(self, priceData=None, mark_date=None, prev_date=None, ignore_tickers=[]):
        ''' These should take a function that determines if we want to exit or not '''
        ''' The function acts on a position object  and returns true or false '''
        ''' % Do not age position '''
        ''' ==================== '''

        self.exit_positions = [] # auto reset
        for position in self.position_list:
            ''' interday position marking '''
            if(position.ID not in ignore_tickers): # don't age anything in the ignore list
                position.age = position.age +1

            ''' Extension of life '''

            try:
                position_PL = position.trade_type*( priceData[position.ID]['Close'].loc[mark_date] - priceData[position.ID]['Open'].loc[mark_date] )*abs(position.num_units)
            except:
                position_PL = 0

            #cumPL = cumPL + position_PL
            self.markPosToMarket( mark_date=mark_date, PL=position_PL  )

            position.wealth = position.wealth + position_PL # update position wealth


            if( (position.age == position.expiration) ) :
                self.exit_positions.append(position)






    ''' ==================== '''
    def markExistingPositionsDInterCC(self, priceData=None, mark_date=None, prev_date=None, ignore_tickers=[]):
        ''' ==================== '''

        self.exit_positions = [] # auto reset

        for key, position in self.position_dict.items():
            ''' interday position marking '''
            if( position.ID not in ignore_tickers): # don't age anything in the ignore list
                position.age = position.age +1

            ''' Extension of life '''
            if( (position.ID in self.dailyPositions['bears'].loc[mark_date] ) or (position.ID in self.dailyPositions['bulls'].loc[mark_date] ) and (position.ID not in ignore_tickers)  ):
                position.expiration = position.expiration + 1


            try:
                position_PL = position.trade_type*( priceData[position.ID]['Close'].loc[mark_date] - priceData[position.ID]['Close'].loc[prev_date] )*abs(position.num_units)
            except:
                position_PL = 0

            #cumPL = cumPL + position_PL
            self.markPosToMarket( mark_date=mark_date, PL=position_PL  )

            #print position.ID, position.age, position.expiration

            position.wealth = position.wealth + position_PL # update position wealth
            # Close out expiring positions that are not in the new bulls and bears
            #if( (position.age == position.expiration) and (position.ID not in ignore_tickers) ) :
            if( (position.age == position.expiration) ) :
                self.exit_positions.append(position)


#        ''' ==================== '''
#    def getPositionPL(self, priceData=None, mark_date=None, prev_date=None, ignore_tickers=[]):
#        ''' ==================== '''
#
#        self.exit_positions = [] # auto reset
#
#        for position in self.position_list:
#            ''' interday position marking '''
#            if(position.ID not in ignore_tickers): # don't age anything in the ignore list
#                position.age = position.age +1
#
#
#            try:
#                position_PL = position.trade_type*( priceData[position.ID]['Close'].loc[mark_date] - priceData[position.ID]['Close'].loc[prev_date] )*abs(position.num_units)
#            except:
#                position_PL = 0
#
#            #cumPL = cumPL + position_PL
#            self.markPosToMarket( mark_date=mark_date, PL=position_PL  )
#
#            #print position.ID, position.age, position.expiration
#
#            position.wealth = position.wealth + position_PL # update position wealth
#
#            # Close out expiring positions that are not in the new bulls and bears
#            #if( (position.age == position.expiration) and (position.ID not in ignore_tickers) ) :
#            if( (position.age == position.expiration) ) :
#                self.exit_positions.append(position)





    ''' ==================== '''
    def setTickers(self):
        ''' ==================== '''
        self.tickers = [ position.ID for position in self.position_list]


    ''' ==================== '''
    def getTickers(self):
        ''' ==================== '''
        return self.tickers


    ''' ==================== '''
    def setBulls(self, ignore=[]):
        ''' ==================== '''
        self.bulls = [ position.ID for position in self.position_list if (position.trade_type==1) and (position.ID not in ignore) ]


    ''' ==================== '''
    def getBulls(self):
        ''' ==================== '''
        return self.bulls


    ''' ==================== '''
    def setBears(self, ignore=[]):
        ''' ==================== '''
        self.bears = [ position.ID for position in self.position_list if (position.trade_type==-1) and (position.ID not in ignore) ]


    ''' ==================== '''
    def getBears(self):
        ''' ==================== '''
        return self.bears


    ''' ==================== '''
    def getNetExposure(self, exclude=[]):
        ''' ==================== '''
        net_exposure = 0

        for position in self.position_list:
            if(position.ID not in exclude):
                net_exposure = net_exposure + position.wealth*position.trade_type

        self.net_exposure = net_exposure
        return net_exposure



    ''' ----------------------------------------------------- #
    # Analytics library
    # ----------------------------------------------------- '''
    def calcRets(self,lag=1):
        self.rets = self.NAV.diff(lag)/ self.NAV

    def getRets(self):
        return self.rets

    def calcCumRets(self):
        self.cum_rets = (self.NAV-self.NAV.iloc[0]) / self.NAV.iloc[0]

    def getCumRets(self):
        return self.cum_rets

    def calcPL(self, lag=1):
        self.dailyPL = self.NAV.diff(lag)

    def getPL(self):
        return self.dailyPL
