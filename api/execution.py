"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.template.py
Created on 2017-02-15T13:21:00Z
@author:Joshua Hu
"""
from __future__ import print_function

import abc

class Execution(object):
    """docstring for Execution."""

    __metaclass__ = abc.ABCMeta

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

    @abc.abstractmethod
    def run():
        raise NotImplementedError("run() is not implemented")
