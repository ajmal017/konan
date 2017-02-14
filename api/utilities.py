#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////

lib.utils.py
Created on Tue Nov 22 12:31 2016
@author: jsrhu

LIBRARY FILE

////////////////////////////////////////////////
------------------------------------
Packages
------------------------
STDLIB:

MAINTAINED:
pandas

CUSTOM:
readWriteData
directory
parsers

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

------------------------
Private
------------

////////////////////////////////////////////

TODO:
Implement function filters

////////////////////////////////////////////////
"""
import datetime as dt
from dateutil.parser import parse

import pandas as pd
from tqdm import tqdm

import readWriteData as rwd
import directory as dr
import parsers as prs

"""
ANALYSIS FUNCTIONS
"""

def max(data = pd.DataFrame(), columns = []):
    return df

def min(data = pd.DataFrame(), columns = []):
    return df

def getDomain(series = pd.Series()):
    def domainParse(x):
        try:
            return prs.URLDomainParse(x)
        except:
            return 'empty.domain'

    tqdm.pandas(desc='Getting domains')
    domains = series.progress_apply(lambda x: domainParse(x))
    return domains

def getDate(series = pd.Series()):
    tqdm.pandas(desc='Getting days')
    dates = series.progress_apply(lambda x: parse(str(x)).date())
    return dates

def accernDomainFrequency(data = pd.DataFrame(), last_date = dt.date.today()):
    df_data = data.loc[:,['article_url','harvested_at','overall_author_rank']]
    df_data['domain'] = getDomain(df_data['article_url'])
    df_data['date'] = getDate(df_data['harvested_at'])
    df_group = df_data.groupby('domain')
    df_day_avg = pd.DataFrame({'day_avg':None, 'total':df_group.size() , 'dofm':df_group['date'].min(), 'dolm':df_group['date'].max(), 'age_days':None, 'days_inactive':None, 'max_author_rank':df_group['overall_author_rank'].max(),'mean_author_rank':df_group['overall_author_rank'].mean()})
    df_day_avg['days_inactive'] = df_day_avg['dolm'].rsub(last_date).dt.days
    df_day_avg['age_days'] = df_day_avg['dolm'].sub(df_day_avg['dofm']).dt.days+1
    df_day_avg['day_avg'] = df_day_avg['total'].div(df_day_avg['dofm'].rsub(last_date).dt.days+1)
    return df_day_avg

def accernEventImpact(data = pd.DataFrame()):
    return df
