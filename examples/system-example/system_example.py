"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
system-example.py
Created on 2017-03-03T13:17:00Z
@author:Joshua Hu
"""
# imports from future
from __future__ import print_function

#imports from stdlib
import abc

import time
import datetime as dt

import cPickle

# internal/custom imports
import konan.api.system as system
import konan.api.broker as broker

import strategy_example

path_system_state = '/Users/jsrhu/Dropbox/'

def main():
    # initialize the broker resource
    eBroker = broker.IBBrokerTotal()

    # specify strategies associated with the system account
    dict_strategies = {'eStrategy': strategy_example.exampleStrategy()}

    # create
    eSystem = system.System(path_system_state = '',
                            strategies = dict_strategies,
                            time_end = dt.time(hour = 16, minute = 30),
                            time_sleep = 10, broker = eBroker)

    for event in eSystem.strategy_schedule:
        # TODO: modularize
        print('--------------------------------')
        print('FROM: ',__file__) # TODO: argument
        print('----------------')
        print(event,':', eSystem.strategy_schedule[event][0], ';', eSystem.strategy_schedule[event][1])
        # TODO: more arguments
        print('--------------------------------')
        # TODO: end modularize
    eSystem.run()

if __name__ == '__main__':
    main()
