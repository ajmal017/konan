"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.strategy.py
Created on 2017-02-15T11:54:00Z
@author:Joshua Hu
"""
# imports from future
from __future__ import print_function

#imports from stdlib
import abc

import time
import datetime as dt

# internal/custom imports
import broker
import position

class Strategy(object):
    """docstring for Strategy."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, broker = None, decision_algorithm = None,
                    portfolio = None, time_execution = None, time_end = None,
                    time_sleep = 0, event_schedule = None):
        super(Strategy, self).__init__()

        self._broker = broker

        self._decision_algorithm = decision_algorithm

        self._portfolio = portfolio

        self._time_execution = time_execution
        self._time_end = time_end

        self._time_sleep = time_sleep

        self._event_schedule = event_schedule

    """
    CLASS PROPERTIES
    """
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

    def decision_algorithm():
        doc = "The decision_algorithm property."
        def fget(self):
            return self._decision_algorithm
        def fset(self, value):
            self._decision_algorithm = value
        def fdel(self):
            del self._decision_algorithm
        return locals()
    decision_algorithm = property(**decision_algorithm())

    def portfolio():
        doc = "The portfolio property."
        def fget(self):
            return self._portfolio
        def fset(self, value):
            self._portfolio = value
        def fdel(self):
            del self._portfolio
        return locals()
    portfolio = property(**portfolio())

    def time_execution():
        doc = "The time_execution property."
        def fget(self):
            return self._time_execution
        def fset(self, value):
            self._time_execution = value
        def fdel(self):
            del self._time_execution
        return locals()
    time_execution = property(**time_execution())

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

    def event_schedule():
        doc = "The event_schedule property."
        def fget(self):
            return self._event_schedule
        def fset(self, value):
            self._event_schedule = value
        def fdel(self):
            del self._event_schedule
        return locals()
    event_schedule = property(**event_schedule())

    def checkPortfolio():
        raise NotImplementedError("checkPortfolio() has not been implemented in the API")

    def checkDecision():
        raise NotImplementedError("checkDecision() has not been implemented in the API")

    def makeTrade(position = position.Position()):
        raise NotImplementedError("makeTrade() has not been implemented in the API")

    def updatePortfolio(position = position.Position()):
        raise NotImplementedError("updatePortfolio() has not been implemented in the API")

    def execute(self):
        print('EXECUTING: ', self.__class__.__name__)

        while dt.datetime.now().time() <= self.time_end:
            for event in self.event_schedule:
                if dt.datetime.now().time() >= dt.datetime.strptime(str(event), '%H:%M:%S.%f').time():
                    # TODO: implement method of parameter passing
                    print(event)
                    print(self.event_schedule[event][0],':',self.event_schedule[event][1])
                    self.event_schedule[event][0]()#(self.event_schedule[event][1])
            time.sleep(self.time_sleep)
