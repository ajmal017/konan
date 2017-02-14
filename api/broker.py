"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
api.broker.py
Created on 2017-02-14T16:36:00Z
@author:Joshua Hu
"""

class broker(object):
    """docstring for broker."""
    def __init__(self, arg):
        super(broker, self).__init__()
        self.arg = arg

class IBBroker(broker):
    """docstring for IBBroker."""
    def __init__(self, arg):
        super(IBBroker, self).__init__()
        self.arg = arg


class DataBroker(broker):
    """docstring for DataBroker."""
    def __init__(self, arg):
        super(DataBroker, self).__init__()
        self.arg = arg

class IBDataBroker(IBBroker, DataBroker):
    """docstring for IBDataBroker."""
    def __init__(self, arg):
        super(IBDataBroker, self).__init__()
        self.arg = arg

class ExecutionBroker(broker):
    """docstring for ExecutionBroker."""
    def __init__(self, arg):
        super(ExecutionBroker, self).__init__()
        self.arg = arg

class IBExecutionBroker(IBBroker, ExecutionBroker):
    """docstring for IBExecutionBroker."""
    def __init__(self, arg):
        super(IBExecutionBroker, self).__init__()
        self.arg = arg
