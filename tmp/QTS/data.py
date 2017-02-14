#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
data.py
Created on Fri Nov 18 13:35 2016
@author: Michael Halls Moore
@author: Joshua Hu

///////////
Constants**
///////////
None

/////////
Classes**
/////////
Parent:

Children:

"""
from __future__ import print_function

from abc import ABCMeta, abstractmethod

import sys
import datetime
import os, os.path
import datetime as dt
import operator as op

import numpy as np
import pandas as pd
from tqdm import tqdm

import lib.readWriteData as rwd

from event import MarketEvent

class DataHandler(object):
    """
    DataHandler is an abstract base class providing an interface for all subsequent (inherited) data handlers (both live and historic).
    The goal of a (derived) DataHandler object is to output a generated set of bars (OHLCVI) for each symbol requested.
    This will replicate how a live strategy would function as current market data would be sent "down the pipe".
    Thus a historic and live system will be treated identically by the rest of the backtesting suite.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_bar(self, symbol):
        """
        Returns the last bar updated.
        """
        raise NotImplementedError("Should implement get_latest_bar()")

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars updated.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def get_latest_bar_datetime(self, symbol):
        """
        Returns a Python datetime object for the last bar.
        """
        raise NotImplementedError("Should implement get_latest_bar_datetime()")

    @abstractmethod
    def get_latest_bar_value(self, symbol, val_type):
        """
        Returns one of the Open, High, Low, Close, Volume or OI from the last bar.
        """
        raise NotImplementedError("Should implement get_latest_bar_value()")

    @abstractmethod
    def get_latest_bars_values(self, symbol, val_type, N=1):
        """
        Returns the last N bar values from the
        latest_symbol list, or N-k if less available.
        """
        raise NotImplementedError("Should implement get_latest_bars_values()")

    @abstractmethod
    def update_bars(self):
        """
        Pushes the latest bars to the bars_queue for each symbol
        in a tuple OHLCVI format: (datetime, open, high, low,
        close, volume, open interest).
        """
        raise NotImplementedError("Should implement update_bars()")

class HistoricCSVDataHandler(DataHandler):
    """
    HistoricCSVDataHandler is designed to read CSV files for each requested symbol from disk and provide an interface to obtain the "latest" bar in a manner identical to a live trading interface.
    """
    def __init__(self, events, csv_dir, symbol_list):
        """
        Initialises the historic data handler by requesting the location of the CSV files and a list of symbols. It will be assumed that all files are of the form ’symbol.csv’, where symbol is a string in the list.

        Parameters:
        events - The Event Queue.
        csv_dir - Absolute directory path to the CSV files.
        symbol_list - A list of symbol strings.

        Return:
        None
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting them into pandas DataFrames within a symbol dictionary. For this handler it will be assumed that the data is taken from Yahoo. Thus its format will be respected.
        """
        comb_index = None
        for s in self.symbol_list:
        # Load the CSV file with no header information, indexed on date
            self.symbol_data[s] = pd.io.parsers.read_csv(os.path.join(self.csv_dir, ’%s.csv’ % s),
            header=0, index_col=0, parse_dates=True,
            names=['datetime', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
            ).sort()

        # Combine the index to pad forward values
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index.union(self.symbol_data[s].index)
                # Set the latest symbol_data to None
                self.latest_symbol_data[s] = []
        # Reindex the dataframes
        for s in self.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].\
            reindex(index=comb_index, method=’pad’).iterrows()

    def _get_new_bar(self, symbol):
        """
        Returns the latest bar from the data feed.
        """
        for b in self.symbol_data[symbol]:
            yield b

    def get_latest_bar(self, symbol):
        """
        Returns the last bar from the latest_symbol list.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1]

    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list, or N-k if less available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol] except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol):
        """
        Returns a Python datetime object for the last bar.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1][0]

    def get_latest_bar_value(self, symbol, val_type):
        """
        Returns one of the Open, High, Low, Close, Volume or OI
        values from the pandas Bar series object.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return getattr(bars_list[-1][1], val_type)

    def get_latest_bars_values(self, symbol, val_type, N=1):
        """
        Returns the last N bar values from the latest_symbol list, or N-k if less available.
        """
        try:
            bars_list = self.get_latest_bars(symbol, N)
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return np.array([getattr(b[1], val_type) for b in bars_list])

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure for all symbols in the symbol list.
        """
        for s in self.symbol_list:
            try:
                bar = next(self._get_new_bar(s))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                        self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())

class repository(object):
    def __init__(self, dir_root = '/', project = 'test/', data_file = 'test.txt'):
        self._root = dir_root #find users Dropbox folder
        self._projects = os.listdir(self.root)
        self._current_project = self.selectProject(project = project)
        self._current_file = data_file

    def selectProject(self, project = ''):
        if project not in self.projects:
            try:
                os.mkdir(self.root + project) # try for mkdirs
            except:
                print(traceback.format_exc()+'\n')
                return ''
        return project

    def checkData(self, path = ''):
        if not os.path.exists(path):
            # decide which to use
            return False
            '''raise IOError('The file: ' + path +
                        ' does not exist or could not be found.')'''
        else:
            return True

    def root():
        doc = "The root property."
        def fget(self):
            return self._root
        def fset(self, value):
            self._root = value
        def fdel(self):
            del self._root
        return locals()
    root = property(**root())

    def projects():
        doc = "The projects property."
        def fget(self):
            return self._projects
        def fset(self, value):
            self._projects = value
        def fdel(self):
            del self._projects
        return locals()
    projects = property(**projects())

    def current_project():
        doc = "The current_project property."
        def fget(self):
            return self._current_project
        def fset(self, value):
            self._current_project = value
        def fdel(self):
            del self._current_project
        return locals()
    current_project = property(**current_project())

    def current_file():
        doc = "The current_file property."
        def fget(self):
            if self.checkData(self._current_file):
                return self._current_file
            else:
                return self.checkData(self._current_file)
        def fset(self, value):
            self._current_file = value
        def fdel(self):
            del self._current_file
        return locals()
    current_file = property(**current_file())

    def project_path():
        doc = "The project_path property."
        def fget(self):
            return self._root + self._current_project
        return locals()
    project_path = property(**project_path())

    def file_path():
        doc = "The file_path property."
        def fget(self):
            return self._root + self._current_project + self._current_file
        return locals()
    file_path = property(**file_path())

class filter(object):
    """
    Base Class for data filters. Historical Filter for Backtest sub-system and Live Filter for Live Trading sub-system
    """
    def __init__(self, filter_lifespan = 1, filter_update_period = 1, hist_data_sources = [], live_data_sources = [], **kwds):
        """
        Constructor for dataFilter class

        Parameters:
        self -
        filter_lifespan -
        filter_update_period -
        hist_data_sources -
        live_data_sources -

        Return:
        None
        """

        self._lifespan = dt.timedelta(days=filter_lifespan)
        self._update_period = dt.timedelta(days=filter_update_period)
        self._hist_data_sources = hist_data_sources
        self._live_data_sources = live_data_sources

    @property
    def lifespan(self):
        return self._lifespan

    @lifespan.setter
    def lifespan(self, value):
        if value < 1:
            raise ValueError("Filter Lifespan must be at least 1 day long, i.e. Lifespan must be non-zero and positive")
        if not isinstance(value,(int,long)):
            raise TypeError("Filter Lifespan must be set in whole days, i.e. Lifespan value must be an integer")
        self._lifespan = dt.timedelta(days=value)

    @property
    def update_period(self):
        return self._update_period

    @update_period.setter
    def update_period(self, value):
        if value < 1:
            raise ValueError("Filter Update Period must be at least 1 day long, i.e. Update Period must be non-zero and positive")
        if not isinstance(value,(int,long)):
            raise TypeError("Filter Update Period must be set in whole days, i.e. Update Period value must be an integer")
        self._update_period = dt.timedelta(days=value)

    @property
    def hist_data_sources(self):
        return self._hist_data_sources

    @hist_data_sources.setter
    def hist_data_sources(self, sources):
        #raise error on object types in list?
        if sources == None:
            raise ValueError("Source list cannot be empty")
        self._hist_data_sources = sources

    @property
    def live_data_sources(self):
        return self._live_data_sources

    @live_data_sources.setter
    def live_data_sources(self, sources):
            #raise error on object types in list?
        if sources == None:
            raise ValueError("Source list cannot be empty")
        self._live_data_sources = sources

    def rawFilter(self, data = pd.DataFrame(), columns = [], black = False):
        """
        Filter raw data to create a pandas DataFrame

        Parameters:
        data -
        columns -
        black -

        Return:
        function - returns pandas DataFrame
        """
        if black == True:
            return self._rawBlacklist(data = data, columns = columns)
        else:
            return self._rawWhitelist(data = data, columns = columns)

    def _rawBlacklist(self, data = pd.DataFrame(), columns = []):
        """
        Private function for filter class that returns a subsection of a pandas DataFrame using a blacklist of DataFrame columns.

        Parameters:
        columns -

        Return:
        df - pandas DataFrame
        """
        df = rwd.readToDF(path_data = data)
        filtered = df.drop(labels = columns, axis = 1)
        return filtered

    def _rawWhitelist(self, data = pd.DataFrame(), columns = []):
        """
        Private function for filter class that returns a subsection of a pandas DataFrame using a whitelist of DataFrame columns.

        Parameters:
        columns -

        Return:
        df - pandas DataFrame
        """
        df = rwd.readToDF(path_data = data)
        filtered = df[columns]
        return filtered

    def rawValueFilter(self, data = pd.DataFrame(), columns = [], values = {}, comparators = {}):
        """
        Filter raw data to create a pandas DataFrame

        Parameters:
        data - pandas DataFrame
        columns - columns to filter
        values - dictionary with column names as strings and values being the values to filter by
        comparator - comparison operator

        Return:
        function - returns pandas DataFrame
        """
        dict_comparator = {'!=':op.ne,
                           '==':op.eq,
                           '<':op.lt,
                           '>':op.gt,
                           '<=':op.le,
                           '>=':op.ge}
        #try catch for not comparators
        df = data
        for key in columns:
            df_new = df[dict_comparator[comparators[key]]( df[key] , values[key] )]
            df = df_new
        return df

    def rawSetFilter(self, data = pd.DataFrame(), set_ = [], columns = [], black = False):
        """
        PARAMETERS:
        self -
        data -
        set_ -
        columns -
        black -

        RETURN:
        df - filteres pandas DataFrame
        """
        df = data
        for key in columns:
            df_new = df[df[key].isin(set_)]
            df = df_new
        return df

    def calcFilter(self, data = pd.DataFrame(), columns = [], functions = [], black = False):
        """
        Filter raw data through the use of a calculated function from the data properties

        Parameters:
        data -
        columns -
        functions -
        black -

        Return:
        function - returns pandas DataFrame
        """
        if black == True:
            return self._calcBlacklist(data = data, columns = columns, functions = functions)
        else:
            return self._calcWhitelist(data = data, columns = columns, functions = functions)

    def _calcBlacklist(self, data = pd.DataFrame(), columns = [], functions = []):
        """
        Private function for filter class that returns a subsection of a pandas DataFrame using functions to create a blacklist of DataFrame columns.

        Parameters:
        data -
        columns -
        functions -

        Return:
        df - pandas DataFrame
        """
        for function in functions:
            df = function(data,inplace=True)
        return df

    def _calcWhitelist(self, data = pd.DataFrame(), columns = [], functions = []):
        """
        Private function for filter class that returns a subsection of a pandas DataFrame using functions to create a blacklist of DataFrame columns.

        Parameters:
        data -
        columns -
        functions -

        Return:
        df - pandas DataFrame
        """
        for function in functions:
            df = function(data,inplace=True)
        return df

class histFilter(dataFilter):
    """
    Historical Filter for Backtest sub-system
    """
    def __init__(self, filter_lifespan = 1, filter_update_period = 1, **kwds):
        """
        Constructor for histFilter class

        Parameters:
        self -
        filter_lifespan -
        filter_update_period -

        Return:
        None
        """
        base = dataFilter(filter_lifespan = filter_lifespan, filter_update_period = filter_update_period, hist_data_sources = [])
        self._lifespan = base.lifespan
        self._update_period = base.update_period
        self._hist_data_sources = base.hist_data_sources

    def spawnLiveFilter(self):
        return liveFilter(filter_lifespan = self.lifespan, filter_update_period = self.filter_update_period)

class liveFilter(dataFilter):
    """
    Live Filter for Live trading sub-system
    """
    def __init__(self, filter_lifespan = 1, filter_update_period = 1, update_hour = 16, update_minute = 00, dict_candidate = {'candidate_columns':[],'candidate_values':{}, 'candidate_comparators':{}}, dict_whitelist = {'whitelist_columns':[],'whitelist_values':{}, 'whitelist_comparators':{}}, columns = [], candidate_values = {}, whitelist_values ={}, comparators = {}, **kwds):
        """
        Constructor for liveFilter class

        Parameters:
        self -
        filter_lifespan -
        filter_update_period -

        Return:
        None
        """
        base = dataFilter(filter_lifespan = filter_lifespan, filter_update_period = filter_update_period, live_data_sources = [])
        self._lifespan = base.lifespan
        self._update_period = base.update_period
        self._live_data_sources = base.live_data_sources
        self._birthdate = dt.date.today()
        self._update_time = dt.time(hour = update_hour, minute = update_minute)

        self._candidate_columns = dict_candidate['candidate_columns']
        self._candidate_values = dict_candidate['candidate_values']
        self._candidate_comparators = dict_candidate['candidate_comparators']

        self._whitelist_columns = dict_whitelist['whitelist_columns']
        self._whitelist_values = dict_whitelist['whitelist_values']
        self._whitelist_comparators = dict_whitelist['whitelist_comparators']

    @property
    def birthdate(self):
        return self._birthdate

    @property
    def update_time(self):
        return self._update_time

    @property
    def candidate_columns(self):
        return self._candidate_columns

    @property
    def candidate_values(self):
        return self._candidate_values

    @property
    def candidate_comparators(self):
        return self._candidate_comparators

    @property
    def whitelist_columns(self):
        return self._whitelist_columns

    @property
    def whitelist_values(self):
        return self._whitelist_values

    @property
    def whitelist_comparators(self):
        return self._whitelist_comparators

    def _check(self):
        time_now = dt.datetime.now().time()
        if time_now >= self.update_time:
            return True
        else:
            return False

    def updateCandidateList(self, data = pd.DataFrame(), columns = []):
        """
        Parameters:
        self
        data

        Return:
        df_candidate_update
        """
        if not self._check():
            pass
        else:
            df_candidate_update = self.rawValueFilter(data = data, columns = self.candidate_columns, values = self.candidate_values, comparators = self.candidate_comparators)
            return df_candidate_update

    def updateWhitelist(self, data = pd.DataFrame(), columns = []):
        """
        Parameters:
        self
        data

        Return:
        df_whitelist_update
        """
        if not self._check(): # causing errors if day parameters of _check() are not specified
            pass
        else:
            df_whitelist_update = self.rawValueFilter(data = data, columns = self.whitelist_columns, values = self.whitelist_values, comparators = self.whitelist_comparators)
            return df_whitelist_update

    def connect(self, source):
        """
        Connect to a given data source.

        Parameters:
        source

        Return:
        connection
        """
        connection = source
        return connection

    def readConnection(self, connection):
        """
        Read information form a connection to a data source.

        Parameters:
        connection

        Return:
        data
        """
        data = connection
        return data
