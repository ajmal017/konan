"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api/system.py
Created on 2017-02-15T13:21:00Z
@author:Joshua Hu
"""
# imports from future
from __future__ import print_function

#imports from stdlib
import abc

import cPickle

import time
import datetime as dt

# internal/custom imports
import directory # FULL PATH: konan.api.directory

import broker # FULL PATH: konan.api.broker

class System(object):
    """docstring for System."""
    def __init__(self, path_system_state = '', strategies = {},
                    time_end = dt.datetime.now().time(), time_sleep = 0,
                    broker = None):
                    # TODO: may replace IBBrokerTotal with new class name
        super(System, self).__init__()
        self._path_system_state = path_system_state
        try:
            self._system_state = self.loadState(path_system_state = path_system_state)
        except:
            self._system_state = None
        # TODO: loadState + unpackState if there is an existing previous state;
        # if no valid previous state found OR path_system_state == ''
        # assume construction from null state

        self._broker = broker

        self._strategy_schedule = {}
        for strategy in strategies:
            strategies[strategy].broker = self.broker
            self.strategy_schedule[strategy] = (strategies[strategy].time_execution, strategies[strategy])
        self._time_end = time_end
        self._time_sleep = time_sleep

    def path_system_state():
        doc = "The path_system_state property."
        def fget(self):
            return self._path_system_state
        def fset(self, value):
            self._path_system_state = value
        def fdel(self):
            del self._path_system_state
        return locals()
    path_system_state = property(**path_system_state())

    def system_state():
        doc = "The system_state property."
        def fget(self):
            return self._system_state
        def fset(self, value):
            self._system_state = value
        def fdel(self):
            del self._system_state
        return locals()
    system_state = property(**system_state())

    def strategies():
        doc = "The strategies property."
        def fget(self):
            return self._strategies
        def fset(self, value):
            self._strategies = value
        def fdel(self):
            del self._strategies
        return locals()
    strategies = property(**strategies())

    def strategy_schedule():
        doc = "The strategy_schedule property."
        def fget(self):
            return self._strategy_schedule
        def fset(self, value):
            self._strategy_schedule = value
        def fdel(self):
            del self._strategy_schedule
        return locals()
    strategy_schedule = property(**strategy_schedule())

    def time_end():
        doc = "The time_end property."
        def fget(self):
            return self._time_end
        def fset(self, value):
            self._time_end = value
        def fdel(self):
            del self._time_end
        return locals()
    time_end = property(**time_end())

    def time_sleep():
        doc = "The time_sleep property."
        def fget(self):
            return self._time_sleep
        def fset(self, value):
            self._time_sleep = value
        def fdel(self):
            del self._time_sleep
        return locals()
    time_sleep = property(**time_sleep())

    def broker():
        doc = "The broker property."
        def fget(self):
            return self._broker
        def fset(self, value):
            self._broker = value
        def fdel(self):
            del self._broker
        return locals()
    broker = property(**broker())

    def loadState(self, path_system_state):
        if not directory.checkPath(path = path_system_state):
            with open(path_system_state, 'w+') as f:
                return cPickle.load(f)
        with open(path_system_state, 'rb') as f:
            return cPickle.load(f)

    def unpackState(self, state = None):
        #TODO
        pass

    def saveState(self):
        with open(self.path_system_state, 'rb') as f:
            cPickle.dump(self.system_state,f,2)

    def run(self):
        # TODO: check if connection actually passes to strategies
        self.broker.connect()
        # TODO: could possibly initiate multiple subprocesses; research
        while dt.datetime.now().time() <= self.time_end:
            for event in self.strategy_schedule:
                if dt.datetime.now().time() >= dt.datetime.strptime(str(self.strategy_schedule[event][0]), '%H:%M:%S.%f').time():
                    self.strategy_schedule[event][1].execute()
                    # TODO: need to implement multithreading for multiple strategies
            time.sleep(self.time_sleep)
        self.broker.disconnect()
