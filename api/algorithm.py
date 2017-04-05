"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.algorithm.py
Created on 2017 -02-15T13:08:00Z
@author:Joshua Hu
"""
from __future__ import print_function

import abc

import datetime as dt

import position

class DecisionAlgorithm(object):
    """docstring for DecisionAlgorithm."""
    _metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def positions():
        doc = "The positions property."
        def fget(self):
            return self._positions
        def fset(self, value):
            self._positions = value
        def fdel(self):
            del self._positions
        return locals()

    @abc.abstractmethod
    def createPosition(time = dt.datetime.now(), ticker = '', amount_unit = 0, amount_value = 0.0):
        raise NotImplementedError("makePosition() is not implemented")

    @abc.abstractmethod
    def storePosition(position = position.Position()):
        raise NotImplementedError("storePosition() is not implemented")

    @abc.abstractmethod
    def calculatePositions():
        raise NotImplementedError("calculatePositions() is not implemented")

    @abc.abstractmethod
    def getData(data = '', trade_type = ''):
        raise NotImplementedError("getData() is not implemented")

"""
EXAMPLE USE CASE:
#this is written in an external script
import api.algortihm
class Deltix_algorithm(DecisionAlgorithm):
    ...
"""
