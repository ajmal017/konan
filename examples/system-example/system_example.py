"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
system-example.py
Created on 2017-03-03T13:17:00Z
@author:Joshua Hu
"""
from __future__ import print_function

import abc

import time
import datetime as dt

import cPickle

import konan.api.system as system

import strategy_example

path_system_state = '/Users/jsrhu/Dropbox/'

def main():
    eSystem = system.System(path_system_state = '',
                            strategies = {'eStrategy': strategy_example.exampleStrategy()},
                            time_sleep = 10)
    # broker parameter passed default value of IBBrokerTotal() class
    # from broker module

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
