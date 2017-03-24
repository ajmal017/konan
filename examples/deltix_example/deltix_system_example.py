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

import deltix_strategy_example

path_system_state = '/Users/jsrhu/Dropbox/'

def main():
    # initialize the broker resource
    broker_252 = broker.IBBrokerTotal()

    # specify strategies associated with the system account
    dict_strategies = {'Deltix': deltix_strategy_example.deltixStrategy()}

    # create
    system_papar252 = system.System(path_system_state = path_system_state,
                            strategies = dict_strategies,
                            time_end = dt.time(hour = 16, minute = 30),
                            time_sleep = 30, broker = broker_252)

    for event in system_papar252.strategy_schedule:
        # TODO: modularize
        print('--------------------------------')
        print('FROM: ',__file__) # TODO: argument
        print('----------------')
        print(event,':', system_papar252.strategy_schedule[event][0], ';', system_papar252.strategy_schedule[event][1])
        # TODO: more arguments
        print('--------------------------------')
        # TODO: end modularize
    system_papar252.run()

if __name__ == '__main__':
    main()
