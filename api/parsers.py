#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////

lib.parsers.py
Created on Thurs Nov 17 15:13 2016
@author: jsrhu

LIBRARY FILE

////////////////////////////////////////////////
------------------------------------
Packages
------------------------
STDLIB:
os
urlparse
datetime

MAINTAINED:
pandas

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
dateFormatParse
URLDomainParse
fileNameParse
fileExtensionParse
keywordParse

------------------------
Private
------------

////////////////////////////////////////////

TODO:

////////////////////////////////////////////////
"""
import os
import pandas as pd
from urlparse import urlparse
import datetime

def dateFormatParse(date_string):
    """
    Returns datetime date object
    """
    date_format="%Y-%m-%d %H:%M:%S %Z"
    date = pd.datetime.strptime(date_string, date_format)
    return date

def URLDomainParse(url_string = ''):
    """
    Returns domain from a given URL
    """
    domain = urlparse(url_string).netloc
    return domain

def fileNameParse(path_file = ''):
    """
    Return file name
    """
    file_name_ext = os.path.basename(path_file).split('.')
    return file_name_ext[0]

def fileExtensionParse(path_file = ''):
    """
    Returns file extension
    """

    file_name_ext = os.path.basename(path_file).split('.')
    extension = file_name_ext[1]

    #path, extension = os.path.splitext(path = path_file)
    return extension

def keywordParse(string, keyword):
    """
    Return keyword if found in a string
    """
    if keyword in string:
        return keyword
    else:
        return False
