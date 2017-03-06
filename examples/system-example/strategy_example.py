"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
strategy-example.py
Created on 2017-03-03T13:35:00Z
@author:Joshua Hu
"""
# imports from future
from __future__ import print_function

# internal/custom imports
import datetime as dt
import konan.api.strategy as strategy

class exampleStrategy(strategy.Strategy):
    """
    """
    def __init__(self, decision_algorithm = None, portfolio = None,
                    time_execution = dt.datetime.now().time()):
        super(exampleStrategy, self).__init__(decision_algorithm = decision_algorithm,
                                                portfolio = portfolio,
                                                time_execution = time_execution)

    def checkPortfolio():
        pass

    def checkDecision():
        pass

    def makeTrade(position = None):
        pass

    def updatePortfolio(position = None):
        pass

    def execute(self):
        print('EXECUTING: ', self.__class__.__name__)
