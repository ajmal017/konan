"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
strategy-example.py
Created on 2017-03-03T13:35:00Z
@author:Joshua Hu
"""
# imports from future
from __future__ import print_function

#imports from stdlib
import datetime as dt

# internal/custom imports
import konan.api.strategy as strategy

import konan.api.broker as broker

# Initialize values to be passed to class contstructor

# TODO: implement algorithm_example.py
# import and instantiate <decision_algorithm>
# import algorithm_example

# TODO: implement portfolio API
# import <portfolio>
# import portfolio_example

# Create a child class that inherits from the base <strategy> class
# and rename appropriately for system import purposes
class exampleStrategy(strategy.Strategy):
    """
    """
    def __init__(self, broker = broker.IBBrokerTotal(),
                    time_execution = dt.datetime.now().time(),
                    time_end = dt.time(hour = 16, minute = 30), time_sleep = 30):
                    # time_execution = dt.time(hour = 9, minute = 30

        decision_algorithm = None #algorithm_example.exampleAlgorithm()
        portfolio = None #portfolio_example.examplePortfolio()

        time_format = '%H:%M:%S.%f'

        time_stamp1 = '09:30:00.0'
        time_stamp2 = '12:00:00.0'
        time_stamp3 = '13:00:00.0'
        time_stamp4 = '15:30:00.0'
        # test time
        time_stamp_test = '13:16:30.0' #dt.datetime.now().time()

        # NOT SUPPORTED YET
        action1_arguments = 'thing'
        action2_arguments = 'not-thing'
        action3_arguments = None
        action4_arguments = None

        has_executed = False

        open_day = self.openDay
        hedge_one = self.hedgePositions
        guard = self.guardPositions
        end_day = self.endDay
        test_connection = self.testConnection

        # TODO: MAP & ZIP HERE
        event_schedule = {time_stamp1: [open_day, action1_arguments, has_executed],
                            time_stamp2: [hedge_one, action2_arguments, has_executed],
                            time_stamp3: [guard, action3_arguments, has_executed],
                            time_stamp4: [end_day, action4_arguments, has_executed],
                            time_stamp_test: [test_connection, None, has_executed]}
        # TODO: argument mapping is not finished

        super(exampleStrategy, self).__init__(broker = broker,
                                                decision_algorithm = decision_algorithm,
                                                portfolio = portfolio,
                                                time_execution = time_execution,
                                                time_end = time_end,
                                                time_sleep = time_sleep,
                                                event_schedule = event_schedule)

    #create specific actions groups below contstructor in function form
    def openDay(self, thing = None):
        pass
    def hedgePositions(self, thing = None):
        pass

    def guardPositions(self):
        pass

    def endDay(self):
        pass

    def testConnection(self):
        if self.broker.connected():
            print('IS CONNECTED')
            self.broker.disconnect()
            print('DISCONNECTED')
        self.broker.connect()
        print('CONNECTED')
