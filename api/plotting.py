#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////

lib.plotting.py
Created on Thurs Nov 17 15:27 2016
@author: jsrhu

LIBRARY FILE

////////////////////////////////////////////////
------------------------------------
Packages
------------------------
STDLIB:

MAINTAINED:
pandas
matplotlib.pyplot

CUSTOM:

------------------------------------
Constants
------------------------
Integers: int
------------

------------------------
Long: long
------------

------------------------
Floats: float
------------

------------------------
Complex: complex
------------

------------------------
Strings: str
------------

------------------------
Arrays: list
------------

------------------------
Tuple: (x,y)
------------

------------------------
Sets: set
------------

------------------------
Frozen Set: frozenset
------------

------------------------
Dictionary: {'x':x,'y':y}
------------

------------------------------------
Functions
------------------------
Public
------------
plot

increaseYScaleRange

------------------------
Private
------------

////////////////////////////////////////////

TODO:
Implement plotting functions

////////////////////////////////////////////////
"""
import pandas as pd
import matplotlib.pyplot as plt

def plot(pandas_object, title = None, rot = 45, figsize = (11,8), y_label = None, x_label = None):
    pandas_object.plot(title=title, rot=rot, figsize=figsize, y = y_label, x = x_label)
    plt.show()

def increaseYScaleRange(plot, dataframe_min, dataframe_max, column, percentage):
    plot.ylim(dataframe_min[column].min()-abs(percentage*dataframe_min[column].min()),dataframe_max[column].max()+abs(percentage*dataframe_max[column].max()))
