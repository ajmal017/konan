"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api/system.py
Created on 2017-02-15T13:21:00Z
@author:Joshua Hu
"""
from __future__ import print_function

import abc

class System(object):
    """docstring for System."""
    def __init__(self, system_state = None, strategies = None, broker = None):
        super(System, self).__init__()
        self._system_state = system_state
        self._strategies = strategies
        self._broker = broker

    def system_state():
        doc = "The system_state property."
        def fget(self):
            return self._system_state
        def fset(self, value):
            self._system_state = value
        def fdel(self):
            del self._system_state
        return locals()
    system_state = property(**system_state())

    def strategies():
        doc = "The strategies property."
        def fget(self):
            return self._strategies
        def fset(self, value):
            self._strategies = value
        def fdel(self):
            del self._strategies
        return locals()
    strategies = property(**strategies())

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

    @abc.abstractmethod
    def run():
        raise NotImplementedError("run() is not implemented")
