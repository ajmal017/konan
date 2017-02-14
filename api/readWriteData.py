#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////

lib.readWriteData.py
Created on Thurs Nov 17 13:05 2016
@author: jsrhu

LIBRARY FILE

////////////////////////////////////////////////
------------------------------------
Packages
------------------------
STDLIB:
os
cPickle

MAINTAINED:
numpy
pandas
dropbox

CUSTOM:
directory
parsers

------------------------------------
Constants
------------------------
Integers: int
------------
sample_lines

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
dir_data
dir_pickle
dir_csv
dir_json
acess_token - need to change to filepath pointing to file storing token

------------------------
Arrays: list
------------
csv_keys
json_keys
xls_keys

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
readToDF
readCSV
readJSON
readXLS

pickleDF
returnPickle
serialize

dropboxUpload
dropboxDownload

------------------------
Private
------------
_generalReaderFunction
_checkKeywords

_CSVReaderFunction
_readAccernCSV
_readIWMETF
_readGeneralCSV
_readGeneralJSON
_readSPDRETF

_dropboxConnect

////////////////////////////////////////////

TODO:
Change data directories
Implement try-catch for input variables
Clean documentation and ensure consistency in description
Read chunk by chunk

////////////////////////////////////////////////
"""
import os
import traceback

import numpy as np
import cPickle
import pandas as pd
from tqdm import tqdm

import dropbox

import directory as dr
import parsers as prs

dir_data = '/Users/jsrhu/Code/Git/pandasProjects/data/'
dir_pickle = dir_data+'pickle/'
dir_csv = dir_data+'csv/'
dir_json = dir_data+'json/'

csv_keys = ['accern','IWM']
json_keys = []
xls_keys = ['SPY','MDY']

sample_lines = 10000

#global access_token
access_token_path = '/Users/jsrhu/Code/customPackages/proprietary/QTS/assets/keys/dropbox_api.txt'
with open(access_token_path,'rb') as t:
    global access_token
    access_token = t.read()
#access_token = 'r9-vzHrIPPAAAAAAAAANj9Rdt_OIBEEBgiFhTdvI6UZ4jiFQMSZp0ABd0HHS5j3c'

def readToDF(path_data = '', read_full = True, n_lines = sample_lines):
    """
    Generalized read to df function.

    PARAMETERS:
    path_data - string representation of the data file path
    read_full - boolean value designated if the file is to be read in full or in part
    n_lines - integer value indicating the number of lines to read from the top of the file

    RETURN:
    None - if the file cannot be found
    df - a pandas DataFrame

    TODO:
    extend JSON functionality
    extend directory reading capability
    """

    if dr.checkPath(path = path_data, is_file = True):
        df = readFromFile(path_data = path_data, read_full = read_full, n_lines = n_lines)
        return df

    else:
        df = readFromDirectory(path_data = path_data, read_full = read_full, n_lines = n_lines)
        return df

def readFromFile(path_data = '', read_full = True, n_lines = sample_lines):
    file_extension = prs.fileExtensionParse(path_data)
    function = _generalReaderFunction(file_extension)

    if read_full:
        df = function(path_data = path_data)
    else:
        df = function(path_data = path_data, read_full = read_full, n_lines = n_lines)
    return df

def readFromDirectory(path_data = '', read_full = True, n_lines = sample_lines):
    df = pd.DataFrame()
    list_files = dr.listFilesInDir(path_dir = path_data)
    for f in tqdm(iterable = list_files, desc = 'Reading files in directory'):
        path_file = path_data+f
        if not dr.checkPath(path = path_file, is_file = True):
            pass
        else:
            try:
                df_temp = readFromFile(path_data = path_file)
                df = df.append(df_temp)
            except Exception:
                pass
    return df

def _generalReaderFunction(extension):
    """
    Returns function based on matching extension key.

    PARAMETERS:
    extension - string representation of a file extension

    RETURN:
    dict_type[extension] - function from the function dictionary
    """
    dict_type = {'csv':readCSV,
                 'json':readJSON,
                 'xls':readXLS}

    try:
        return dict_type[extension]
    except KeyError:
        return doNothing

def doNothing():
    pass

def _checkKeywords(keys, string):
    """
    Returns first keyword in a list that appears in a string.

    PARAMETERS:
    keys - list of keys to check for
    string - the string to be checked for keywords

    RETURN:
    key - the first keyword from the list keys to be found in string
    """
    for keyword in keys:
        if not prs.keywordParse(string,keyword):
            pass
        else:
            key = prs.keywordParse(string,keyword)
            return key

def readCSV(path_data, read_full = True, n_lines = sample_lines):
    """
    General CSV file reader function.

    PARAMETERS:
    path_data - string representation of the data file path
    read_full - boolean value designated if the file is to be read in full or in part
    n_lines - integer value indicating the number of lines to read from the top of the file

    RETURN:
    df - a pandas DataFrame
    """
    file_name = prs.fileNameParse(path_data)
    key = _checkKeywords(csv_keys,file_name)
    function = _CSVReaderFunction(key)

    if read_full:
        df = function(path_data = path_data)
    else:
        df = function(path_data = path_data, read_full = read_full, n_lines = n_lines)
    return df

def _CSVReaderFunction(key):
    """
    Returns function based on keyword from a path string.

    PARAMETERS:
    key - key indicating which function to return

    RETURN:
    dict_type[key] - function from the Dictionary
    _readGeneralCSV - general CSV reader function
    """
    dict_type = {'accern':_readAccernCSV,
                 'IWM':_readIWMETF}

    try:
        return dict_type[key]
    except KeyError:
        return _readGeneralCSV

def _readAccernCSV(path_data, read_full = True, n_lines = sample_lines):
    """
    Returns a pandas DataFrame from an Accern csv file.

    PARAMETERS:
    path_data - string representation of the data file path
    read_full - boolean value designated if the file is to be read in full or in part
    n_lines - integer value indicating the number of lines to read from the top of the file

    RETURN:
    df - a pandas DataFrame
    """
    Accern_header = 0
    if read_full:
        df = pd.read_csv(filepath_or_buffer = path_data, header = Accern_header, dtype = {'overall_source_rank': np.float64, 'event_impact_score_entity_1': np.float64}, na_values = ['na'], date_parser = prs.dateFormatParse, parse_dates = ['harvested_at'])
    else:
        df = pd.read_csv(filepath_or_buffer = path_data, header = Accern_header, dtype = {'overall_source_rank': np.float64, 'event_impact_score_entity_1': np.float64}, na_values = ['na'], date_parser = prs.dateFormatParse, parse_dates = ['harvested_at'], nrows = n_lines)
    return df

def _readIWMETF(path_data, read_full = True, n_lines = sample_lines):
    """
    Based on ETF CSV files from Blackrock iShares. Includes IWM. Up to date as of Nov 21 2016.

    PARAMETERS:
    path_data - string representation of the data file path
    read_full - boolean value designated if the file is to be read in full or in part
    n_lines - integer value indicating the number of lines to read from the top of the file

    RETURN:
    df - a pandas DataFrame
    """
    Blackrock_iShares_header = 10
    if read_full:
        df = pd.read_csv(filepath_or_buffer = path_data, skiprows = Blackrock_iShares_header)
    else:
        df = pd.read_csv(filepath_or_buffer = path_data, skiprows = Blackrock_iShares_header, nrows = n_lines)
    return df

def _readGeneralCSV(path_data, read_full = True, n_lines = sample_lines):
    """
    Read any CSV file into a pandas DataFrame.

    PARAMETERS:
    path_data - string representation of the data file path
    read_full - boolean value designated if the file is to be read in full or in part
    n_lines - integer value indicating the number of lines to read from the top of the file

    RETURN:
    df - a pandas DataFrame
    """
    if read_full:
        df = pd.read_csv(filepath_or_buffer = path_data)
    else:
        df = pd.read_csv(filepath_or_buffer = path_data, nrows = n_lines)
    return df

def readJSON(path_data = '', read_full = True, n_lines = sample_lines):
    """
    Read JSON to pandas DataFrame

    PARAMETERS:
    path_data - string representation of the data file path
    read_full - boolean value designated if the file is to be read in full or in part
    n_lines - integer value indicating the number of lines to read from the top of the file

    RETURN:
    df - a pandas DataFrame
    """
    # turn to parse function
    # without parse function assumes proper JSON format
    '''
    with open(path_data, 'r') as myfile:
        data = "["+myfile.read().replace('}\r\n{', '},{')+"]"   # using this hack for non-formatted accern json files
    '''
    df = pd.read_json(path_or_buf = path_data)#data)
    return df

def _readGeneralJSON(path_data, read_full = True, n_lines = sample_lines):
    """

    PARAMETERS:
    path_data - string representation of the data file path
    read_full - boolean value designated if the file is to be read in full or in part
    n_lines - integer value indicating the number of lines to read from the top of the file

    RETURN:
    df - a pandas DataFrame
    """
    df = pd.read_json(path_or_buf=str(path_data))
    return df

def readXLS(path_data, read_full = True, n_lines = sample_lines):
    """

    PARAMETERS:
    path_data - string representation of the data file path
    read_full - boolean value designated if the file is to be read in full or in part
    n_lines - integer value indicating the number of lines to read from the top of the file

    RETURN:
    df - a pandas DataFrame
    """
    SPDR_ETF_header = 3
    df = pd.read_excel(io = str(path_data), skiprows = SPDR_ETF_header)
    return df

def _readSPDRETF(path_data):
    """
    Based on ETF XLS files from SPDR. Includes SPY & MDY. Up to date as of Nov 21 2016.

    PARAMETERS:
    path_data - string representation of path to file

    RETURN:
    df = a pandas DataFrame
    """
    SPDR_ETF_header = 3
    df = pd.read_excel(io = str(path_data), skiprows = SPDR_ETF_header)
    return df

#################################
def writeDF():
    pass

#################################
# TODO change the approach to files/incorporate new library functions

def pickleDF(df = pd.DataFrame(), name = '', overwrite = False):
    """
    Pickles a pandas DataFrame witha specified name in the pickle directory.

    PARAMETERS:
    df - a pandas DataFrame
    name - name of file
    path_file - directory to save file

    RETURN:
    returnPickle(name) - serialized pickle object
    cPickle.dump(df, f) - serialized pickle object
    """
    name = str(name)
    file_name = 'df_'+name+'.pickle'
    try:
        os.mkdir(dir_pickle)
    except:
        pass
    if os.path.exists(dir_pickle+file_name) and not overwrite:
        # update pickle or retrieve old pickle?
        print 'Pickle exists: retrieving pickle'
        return returnPickle(name)
    else:
        print '\n\nCreating pickle:',dir_pickle+file_name,'\n'
        with open(dir_pickle+file_name, 'w+') as f:
            return cPickle.dump(df, f)

def returnPickle(name = ''):
    """
    Finds a pickle file based on the initial pandas DataFrame used to create the pickle.

    PARAMETERS:
    name - the name the serialized object is saved as

    RETURN:
    cPickle.load(f) - unserialized data
    """
    name = str(name)
    file_name = dir_pickle+'df_'+name+'.p'
    print file_name
    with open(file_name,'rb') as f:
        try:
            return cPickle.load(f)
        except:
            print 'Error'

def serialize(data = pd.DataFrame(), path = '', form = ''):
    """
    Generalized object serialization.

    PARAMETERS:
    data - object to be serialized
    path - destination for serialized object
    form - serialization form for data

    RETURN:
    None
    """
    pass

def uploadDropbox(path_file = ''):
    """
    Upload file to Dropbox.

    PARAMETERS:
    path_file - taget file for upload

    RETURN:
    True - upload is successful
    False - upload failed
    """
    with _connectDropbox() as dbx:
        with open(path_file,'rb') as f:
            try:
                dbx.files_upload(f, path_file)
            except:
                print "Error uploading file"
                return False
            else:
                return True

def downloadDropbox(path_dropbox = '', path_file = None):
    """
    Upload file to Dropbox.

    PARAMETERS:
    path_dropbox - taget file for upload
    path_file - path to save downloaded file to

    RETURN:
    data - Dropbox file data
    None - file does not exist

    TODO:
    open files properly
    """
    with _connectDropbox() as dbx:
        if path_file == None:
            try:
                meta_data, response = dbx.files_download(path_dropbox)
            except dropbox.exceptions.HttpError as err:
                print('*** HTTP error', err)
                return None
            data = response.content
            print(len(data), 'bytes; md:', meta_data)
            return data
        else:
            try:
                meta_data, response = dbx.files_download_to_file(path_dropbox)#where does path_file come into play?
            except dropbox.exceptions.HttpError as err:
                print('*** HTTP error', err)
                return None
            data = response.content
            print(len(data), 'bytes; md:', meta_data)
            return data

def _connectDropbox():
    """
    Connect to Dropbox with API access token.

    PARAMETERS:
    None

    RETURN:
    dbx - Dropbox connection
    """
    dbx =  dropbox.Dropbox(access_token)
    return dbx
