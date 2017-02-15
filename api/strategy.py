"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.strategy.py
Created on 2017-02-15T11:54:00Z
@author:Joshua Hu
"""
from __future__ import print_function

import abc

import position

class Strategy(object):
    """docstring for Strategy."""
    __metaclass__ = abc.ABCMeta

    """
    CLASS PROPERTIES
    """
    @abc.abstractproperty
    def decision_algorithm():
        doc = "The decision_algorithm property."
        def fget(self):
            return self._decision_algorithm
        def fset(self, value):
            self._decision_algorithm = value
        def fdel(self):
            del self._decision_algorithm
        return locals()

    @abc.abstractproperty
    def portfolio():
        doc = "The portfolio property."
        def fget(self):
            return self._portfolio
        def fset(self, value):
            self._portfolio = value
        def fdel(self):
            del self._portfolio
        return locals()

    @abc.abstractproperty
    def time_execution():
        doc = "The time_execution property."
        def fget(self):
            return self._time_execution
        def fset(self, value):
            self._time_execution = value
        def fdel(self):
            del self._time_execution
        return locals()

    @abc.abstractmethod
    def checkPortfolio():
        raise NotImplementedError("checkPortfolio() has not been implemented")

    @abc.abstractmethod
    def checkDecision():
        raise NotImplementedError("checkDecision() has not been implemented")

    @abc.abstractmethod
    def makeTrade(position = position.Position()):
        raise NotImplementedError("makeTrade() has not been implemented")

    @abc.abstractmethod
    def updatePortfolio(position = position.Position()):
        raise NotImplementedError("updatePortfolio() has not been implemented")

    @abc.abstractmethod
    def execute():
        raise NotImplementedError("execute() has not been implemented")
