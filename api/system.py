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
    """
    <System> class.

    Each <System> instantiation is unique to an Interactive Brokers account.

    The <System> class is responsible for setting up global resources such as
    brokers or portfolios and handling the execution of trading strategies
    associated with its account through threading at a predetermined time.
    The <System> saves critical and important values in order to preserve its
    current state in the case of system failure or interruption
    as a <SystemState> object.
    """
    def __init__(self, path_system_state = '', strategies = {},
                    time_end = dt.datetime.now().time(), time_sleep = 0,
                    broker = None):
                    # TODO: may replace IBBrokerTotal with new class name
        """
        <System> class constructor.

        PARAMETERS:
        path_system_state - string representing path to the serialized
                            <SystemState>
        strategies - dictionary containing imported strategies
        time_end - <datetime.time> object representing the time the system should
                    stop running
        time_sleep - float number representing the number of seconds the system
                        should be inactive between time checks
        broker - <Broker> object

        RETURNS:
        None

        RESULTS:
        Creates <System> object.
        """
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

    """
    CLASS PROPERTIES
    """
    def path_system_state():
        doc = """
                The <<path_system_state>> property provides a string representation
                of the path to the serialized <SystemState> object where the
                <<system_state>> is to be stored and read from.
            """
        def fget(self):
            return self._path_system_state
        def fset(self, value):
            self._path_system_state = value
        def fdel(self):
            del self._path_system_state
        return locals()
    path_system_state = property(**path_system_state())

    def system_state():
        doc = """
                The <<system_state>> property is the <SystemState> object in
                which the system's state values are stored for reference
                and storage.
            """
        def fget(self):
            return self._system_state
        def fset(self, value):
            self._system_state = value
        def fdel(self):
            del self._system_state
        return locals()
    system_state = property(**system_state())

    def strategy_schedule():
        doc = """
                The <<strategy_schedule>> property is a <dictionary> containing
                a <string> key representation of the strategy
                (typically a human readable name) associated with an imported
                child of the <Strategy> class created for a particular strategy.
            """
        def fget(self):
            return self._strategy_schedule
        def fset(self, value):
            self._strategy_schedule = value
        def fdel(self):
            del self._strategy_schedule
        return locals()
    strategy_schedule = property(**strategy_schedule())

    def time_end():
        doc = """
                The <<time_end>> property is a <datetime.time> object which
                represents the time when the system should shutdown.
            """
        def fget(self):
            return self._time_end
        def fset(self, value):
            self._time_end = value
        def fdel(self):
            del self._time_end
        return locals()
    time_end = property(**time_end())

    def time_sleep():
        doc = """
                The <<time_sleep>> property is a <float> which represents the
                time, in granularity of seconds, which the system should sleep
                between execution cycles.
            """
        def fget(self):
            return self._time_sleep
        def fset(self, value):
            self._time_sleep = value
        def fdel(self):
            del self._time_sleep
        return locals()
    time_sleep = property(**time_sleep())

    def broker():
        doc = """
                The broker property is a <Broker> class instance and
                a global resource used by all strategies to request
                external or local data and execute trades with a broker.
            """
        def fget(self):
            return self._broker
        def fset(self, value):
            self._broker = value
        def fdel(self):
            del self._broker
        return locals()
    broker = property(**broker())

    """
    CLASS PUBLIC METHODS
    """
    def loadState(self, path_system_state):
        """
        Function loads a serialized object from a given path.
        Function tries to find and read a path.

        PARAMETERS:
        path_system_state - string representing path to the serialized
                            <SystemState> object

        RETURNS:
        Serialized Python2 object

        RESULTS:
        None
        """
        #TODO: implement catch for errors
        if not directory.checkPath(path = path_system_state):
            with open(path_system_state, 'w+') as f:
                return cPickle.load(f)
        with open(path_system_state, 'rb') as f:
            return cPickle.load(f)

    def unpackState(self, state = None):
        """
        Assigns values found in an object to the appropriate values in the
        system.

        PARAMETERS:
        state - loaded serialized Python2 object

        RETURNS:
        None

        RESULTS:
        Loads values saved in the <SystemState> object into the system.
        """
        #TODO
        pass

    def saveState(self):
        """
        Creates a serialized copy of key system attributes to continue from.
        METHOD DESCRIPTION

        PARAMETERS:
        None

        RETURNS:
        None

        RESULTS:
        Serialized properties object stored in system state directory.

        """
        with open(self.path_system_state, 'rb') as f:
            cPickle.dump(self.system_state,f,2)

    def run(self):
        """
        Main system method.
        Executes all the strategies associated with this system.

        PARAMETERS:
        None

        RETURNS:
        None

        RESULTS:
        Main method of each <Strategy> associated with the <System> instantiation
        is executed.
        """
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

class SystemState(object):
    """
    <SystemState> class.

    Each <SystemState> instantiation is unique to a <System> in one point in
    time.

    The <SystemState> class is responsible for storing serialized
    [trading system state values] for reliable reads in case of system failure.
    """
    def __init__(self):
        super(SystemState, self).__init__()
