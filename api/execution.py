"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.template.py
Created on 2017-02-15T13:21:00Z
@author:Joshua Hu
"""
from __future__ import print_function

import abc

import broker

class Execution(object):
    """docstring for Execution."""
    __metaclass__ = abc.ABCMeta
    def __init__(self, strategies):
        self._strategies = strategies

        #TODO: decide on the sharing of the connection resource between brokers
        self._broker = broker.Broker()

    @abc.abstractproperty
    def strategies():
        doc = "The strategies property."
        def fget(self):
            return self._strategies
        def fset(self, value):
            self._strategies = value
        def fdel(self):
            del self._strategies
        return locals()

    @abc.abstractproperty
    def data_broker():
        doc = "The data_broker property."
        def fget(self):
            return self._data_broker
        def fset(self, value):
            self._data_broker = value
        def fdel(self):
            del self._data_broker
        return locals()

    @abc.abstractproperty
    def execution_broker():
        doc = "The execution_broker property."
        def fget(self):
            return self._execution_broker
        def fset(self, value):
            self._execution_broker = value
        def fdel(self):
            del self._execution_broker
        return locals()

    @abc.abstractmethod
    def run():
        raise NotImplementedError("run() is not implemented")
