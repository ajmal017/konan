"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
deltix_algorithm_example.py
Created on 2017-03-08T14:35:00Z
@author:Joshua Hu
"""
# imports from future
#from __future__ import print_function

#imports from stdlib
import os
import sys
import warnings

import datetime as dt

import cPickle as pickle

import pandas as pd
import numpy as np

# NOT USED
# import utils.files as utf
# from dateutil.parser import parse

# internal/custom imports
import konan.api.algorithm as algo
import konan.api.broker as br

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





class deltixAlgorithm(algo.DecisionAlgorithm):

    def __init__(self):

        self.earningsCalendar = {}
        self.actualCutoff = {}
        self.bears = {}
        self.bulls = {}
        self.params = ( 0, 45, 30, 120 )


    def getScrubDate(self,nextED=None, TOD="", calendar=None):
        idx = utils.find_date_in_list(calendar=calendar, target_date=nextED, move=0 )

        if( (TOD=='After Market') ):
            try:
                return calendar[idx+1]
            except:
                print nextED, " not in trading Calendar "

        elif(  TOD!='nan' ):
            return nextED

        elif ( TOD=='nan' ):
            print "We should not even be attempting to update"


    def getEnterDate(self,nextED=None, TOD="", calendar=None, stk=""):

        ''' Establish Enter Date '''
        enterDate = None
        if ( TOD in ['Before Market', 'During Market'] ):


            ''' Back shift enter date if necessary '''
            idx = utils.find_date_in_list(calendar=calendar, target_date=nextED, move=0 )

            if(idx ==np.nan):
                last_idx = utils.find_date_in_list(calendar=calendar, target_date=nextED, move=1 )
            else:
                last_idx = idx -1
            try:
                enterDate = calendar[last_idx]
                return enterDate

            except:
                print stk, ": Couldn't locate earnings date"
        else:
            return nextED

    def positions():
        pass

    def createPosition():
        pass

    def storePosition():
        pass

    def calculatePositions():
        pass

    def getData(self, dirName='', fileName='', dataType='', date=None):  #
        ''' Specify
        date: datetime object

        dataType: str: 'WSH', 'WSHearnings'
        '''

        data = pd.DataFrame()
        #today = str(dt.date.today()).replace("-","_")
        today = str(date).replace("-","_")

        ''' =================================
            LOAD WSH EARNINGS ANNOUNCEMENT
         ================================= '''
        if( dataType=='WSH' ):

            ''' WSH Data '''
            dirName = dropbox+"QTS\\QTSServer\\Data\\WSH\\Earnings\\"  # folder of WSH data
            file_ = 'WSH_Daily_Snapshot_ED_'+today+'.csv' # default name
            if len(fileName)!=0:  # override
                file_ = fileName
            fileName = os.path.join(dirName, file_)

            WSHDataPath = fileName

            ''' check if file exists '''
            if( not os.path.exists(WSHDataPath) ):
                warnings.warn( WSHDataPath+' not found')
                return data
            data = pd.read_csv( WSHDataPath, index_col='stock_symbol', parse_dates = ['fiscal_year', 'timestamp', 'next_ed'] )
            data['date'] = date

            return data


        ''' =================================
            LOAD WSH EARNINGS CALENDAR
        ================================= '''

        if( dataType=='WSHEarningsCalendar' ):

            dirName = dropbox+"QTS\\QTSServer\\Data\\WSH\\EarningsCalendar\\"  # folder of WSH data

            #file_ = 'WSH_earnings_calendar_'+today+'.p'  # use this file format
            file_ = 'WSH_earnings_calendar.p'  # use this file format

            fileName =  os.path.join(dirName,file_)

            if(os.path.exists)(fileName):
                self.earningsCalendar = pickle.load( open(fileName, "rb") )

            return self.earningsCalendar


        ''' =================================
            LOAD CUTOFF FILE
        ================================= '''
        if( dataType=='WSHCutoffCalendar' ):
            dirName = dropbox+"QTS\\QTSServer\\Data\\WSH\\EarningsCalendar\\"  # folder of WSH data
            #file_ = 'WSH_earnings_calendar_'+today+'.p'  # use this file format
            file_ = 'WSH_cutoff_calendar.p'  # use this file format

            fileName =  os.path.join(dirName,file_)

            if(os.path.exists)(fileName):
                self.actualCutoff = pickle.load( open(fileName, "rb") )
            return self.actualCutoff

        else:
            return "dataType  not found!"

    def returnSeriesSlice(self, WSHlocalStk, date, stk):
        # Today's values
        Q = WSHlocalStk['next_ed_quarter']
        year = WSHlocalStk['fiscal_year'].year
        TOD = str(WSHlocalStk['time_of_day'])
        nextED =  WSHlocalStk['next_ed'].date()
        timeStamp =  WSHlocalStk['timestamp']

        # Can I add timestamp?
        enterDate =  self.getEnterDate( nextED=nextED,
                                       TOD=TOD,
                                       calendar=nysecal,
                                       stk=stk )

        # quarterly infromation embedded in here
        stkSeries = pd.Series( index=['next_ed_quarter', 'fiscal_year','time_of_day', 'next_ed', 'enterDate', 'timestamp'],
                                      data= [Q, year, TOD, nextED, enterDate, timeStamp] )

        return stkSeries


    ''' # ========================================================= # '''

    def constructEarningsCalendar(self, WSHlocal, date=None ):
        ''' Updates earnings calendar or constructs one if it is empty '''

        ''' # ========================================================= # '''

        for stk in WSHlocal.index:

            WSHlocalStk = WSHlocal.loc[stk]

            if stk not in self.earningsCalendar.keys():
                self.earningsCalendar[stk] = pd.DataFrame( index=[date], columns=['next_ed_quarter', 'fiscal_year','time_of_day', 'next_ed', 'enterDate', 'timestamp'] )

            # Today's values
            Q = WSHlocalStk['next_ed_quarter']
            TOD = str(WSHlocalStk['time_of_day'])
            year = WSHlocalStk['fiscal_year'].year
            nextED =  WSHlocalStk['next_ed'].date()
            timeStamp =  WSHlocalStk['timestamp']

            # Can I add timestamp?
            enterDate =  self.getEnterDate( nextED=nextED,
                                       TOD=TOD,
                                       calendar=nysecal,
                                       stk=stk )

            # quarterly infromation embedded in here
            stkSeries = pd.Series( index=['next_ed_quarter', 'fiscal_year','time_of_day', 'next_ed', 'enterDate', 'timestamp'],
                                      data= [Q, year, TOD, nextED, enterDate, timeStamp] )

            #stkSeries = self.returnSeriesSlice(WSHlocalStk, date, stk)


            if( stkSeries['time_of_day'] != 'nan' ):
                self.actualCutoff[stk] = self.getScrubDate( nextED=stkSeries['next_ed'],
                                                  TOD=stkSeries['time_of_day'],
                                                  calendar=nysecal
                                                  )
            ''' ADD IF COMPLETELY EMPTY '''
            if( (self.earningsCalendar[stk].shape[0]==1) and (self.earningsCalendar[stk].iloc[0].isnull().all() ) ):
                self.earningsCalendar[stk].loc[date] = stkSeries

            else:

                dfForQ = self.earningsCalendar[stk][ self.earningsCalendar[stk]['next_ed_quarter']==stkSeries['next_ed_quarter']  ]

                if (dfForQ.empty): # Add if quarter is empty
                    self.earningsCalendar[stk].loc[date] = stkSeries

                else:
                    lastSeriesForQ = dfForQ.iloc[-1].drop('timestamp')  # ignoring timestamp

                    if ( not lastSeriesForQ.equals( stkSeries.drop('timestamp') ) ) :
                        self.earningsCalendar[stk].loc[date] = stkSeries


    ''' # ========================================================= # '''
    def calcTradingSignals(self, earningsCal=None, tday=None):
        ''' # ========================================================= # '''
        '''
        earningsCal = earningsCalendar[stk][Q] in the old scheme
        private method
        returns dictionary of dU and dD
        '''

        found = False
        l2 = -2
        ''' Change in earnings date '''
        lastnextED = earningsCal.iloc[-1]['next_ed']
        lastYear = earningsCal.iloc[-1]['fiscal_year']

        deltaD, deltaU = np.nan, np.nan

        try:
            while( not found ):
                #print l2
                lastChangeDate = earningsCal.iloc[l2]['next_ed']
                lastChangeYear = earningsCal.iloc[l2]['fiscal_year']

                if( (lastnextED  != lastChangeDate) & (lastYear==lastChangeYear) ):
                    found=True
                else:
                    l2 = l2 -1
                if(l2==-20): #cutoff
                    print "Cannot find last changed date"
                    break

            if( found ):
                deltaD = ( earningsCal.iloc[-1]['next_ed'] - earningsCal.iloc[l2]['next_ed'] ).days
                deltaU = ( tday - earningsCal.index[l2+1] ).days                          # time since last announcement

            else:
                deltaD, deltaU = np.nan, np.nan

        except:
             deltaD, deltaU = np.nan, np.nan

        return {'dD': deltaD, 'dU': deltaU}


    ''' # ========================================================= # '''

    def generatePositionsForClose(self, WSHlocal, date=None):

        ''' # ========================================================= # '''

        ''' ------------------------------------------------------- '''
        ''' FIND SIGNALS EVERY DAY ONLY IN THE APPROPRIATE QUARTERS '''
        ''' ------------------------------------------------------- '''

#        todayBulls, todayBears = pd.Series(), pd.Series()
        if(WSHlocal.empty):
            self.bears = {}
            self.bulls = {}

        else:
            for stk in WSHlocal.index:

                WSHlocalStk = WSHlocal.loc[stk]
                Q = WSHlocalStk['next_ed_quarter']

               # Get the approrpiate quarterly earnings announcements
                dfForQ = self.earningsCalendar[stk][ self.earningsCalendar[stk]['next_ed_quarter'] == Q ]

                lastSeriesForQ = dfForQ.iloc[-1]

                # Check if we should enter
                if ( (date==lastSeriesForQ['enterDate']) and (lastSeriesForQ['time_of_day'] in ['After Market', 'Before Market', 'During Market'] ) ):

                    signals = self.calcTradingSignals( earningsCal=dfForQ, tday=date )

                    deltaD = signals['dD']
                    deltaU = signals['dU']
                    
                    print stk, deltaD, deltaU  # check if we are calculating the right metrics

                    #print 'Trying to open: ', stk, deltaD, deltaU
                    if ( (deltaD < self.params[0]) & (deltaU < self.params[1]) ):
                        try:
#                            todayBulls[stk] = priceData[stk]['CloseRtns'].loc[tday] # reset everyday                            
                            # Get close-close returns                            
                            self.bulls[stk] = (deltaD, deltaU)
                            
                        except:
                            print stk, "price data not found. Cannot long"
                            pass


                    if ( (deltaD > self.params[0]) & (deltaU >= self.params[1]) & (deltaU<=self.params[3])):  #& (abs(deltaD) <80) ): # note additional cut off.
                        try:
                            #todayBears[stk] = priceData[stk]['CloseRtns'].loc[tday]
                            self.bears[stk] = (deltaD, deltaU)
                        except:
                            print stk, "price data not found. Cannot short"
                            pass
                        
      


    ''' # ========================================================= # '''

    def scrubEarningsCalendar(self, date=None ):

        ''' # ========================================================= # '''
        for stk in self.earningsCalendar.keys():

            if ( (date==self.actualCutoff[stk]) and len(self.actualCutoff)>0 ) :
                
                print "SCRUBBING: ", stk, " on ", date
                self.earningsCalendar[stk].drop( self.earningsCalendar[stk].loc[:date].index, inplace=True )


    ''' # ========================================================= # '''
    def pickleCalendars(self):
        ''' Pickle earningsCalendar
            Pickle actual cutoff Calendar
        ''' # ========================================================= # '''

        pickle.dump( self.earningsCalendar,
                open( os.path.join(dropbox+"QTS\\QTSServer\\Data\\WSH\\EarningsCalendar\\", 'WSH_earnings_calendar.p'), "wb" ) )

        ''' write to actual cut off to file '''
        pickle.dump( self.actualCutoff,
                open( os.path.join(dropbox+"QTS\\QTSServer\\Data\\WSH\\EarningsCalendar\\", 'WSH_cutoff_calendar.p'), "wb" ) )


''' Generate earnings Calendar '''
create=False
if (create):
    deltixStrat = deltixAlgorithm()

    for _date in pd.date_range( dt.date(2017,1,19), dt.date(2017,3,2) ):

        date = _date.date()

        print date

        WSHData = deltixStrat.getData(dataType='WSH', date=date)

        deltixStrat.getData(dataType='WSHEarningsCalendar', date=date)

        deltixStrat.getData(dataType='WSHCutoffCalendar', date=date)

        deltixStrat.constructEarningsCalendar(WSHData, date=date)

        deltixStrat.generatePositionsForClose(WSHData, date=date)

        A = deltixStrat.earningsCalendar
        B = deltixStrat.actualCutoff

        deltixStrat.pickleCalendars()

#    pickle.dump( deltixStrat.earningsCalendar,
#                open( os.path.join(dropbox+"QTS\\QTSServer\\Data\\WSH\\EarningsCalendar\\", 'WSH_earnings_calendar.p'), "wb" ) )
#
#    ''' write to actual cut off to file '''
#    pickle.dump( deltixStrat.actualCutoff,
#                open( os.path.join(dropbox+"QTS\\QTSServer\\Data\\WSH\\EarningsCalendar\\", 'WSH_cutoff_calendar.p'), "wb" ) )
#
