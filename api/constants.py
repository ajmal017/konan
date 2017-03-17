import sys
import datetime as dt

# INTERACTIVE BROKERS INFORMATION
CLIENT_ID = 100
PORT = 7497

# INTERACTIVE BROKERS ACCOUNT INFORMATION
ACCOUNT_NAMES = {'PAPAR_252': 'DU603835', 'PAPAR_896': 'DU550479'}

# DATETIME FORMATS
TIME_FORMAT = '%H:%M:%S.%f'
DATE_FORMAT = ''

MINUTE_INT = 60
HOUR_INT = 3600

STRING_MARKET_OPEN = '9:30:00.0'
STRING_MARKET_CLOSE = '16:00:00.0'

TIME_MARKET_OPEN = dt.time(hour = 9, minute = 30, second = 00, microsecond = 00)
TIME_MARKET_CLOSE = dt.time(hour = 16, minute = 00, second = 00, microsecond = 00)

STRING_SYSTEM_START = '9:00:00.0'
STRING_SYSTEM_END = '16:30:00.0'

TIME_SYSTEM_START = dt.time(hour = 9, minute = 00, second = 00, microsecond = 00)
TIME_SYSTEM_END = dt.time(hour = 16, minute = 30, second = 00, microsecond = 00)

# SETS AND LISTS (?)
# PANDAS COLUMNS AND INDICIES (?)

# FILE EXTENSIONS
FILE_EXTENSION_CSV = '.csv'
FILE_EXTENSION_JSON = '.json'
FILE_EXTENSION_XLS = '.xls'

# SPECIFIC FILE NAMES
FILE_NAME_WSH_DAILY_DATA = 'WSH_Daily_Snapshot_ED_'

# SPECIFIC DIRECTORY PATHS
PATH_DAILY_PNL = ''
PATH_AGGREGATE_PNL = ''

# USER SPECIFIC
if sys.platform == 'win32':
    RAY = {'MODULES': utils,
        'nyse_calendar_path': "myPythonprojects\\konan\\rd\\mcal_test.p",
        'WSH_data_path': "QTS\\QTSServer\\Data\\WSH\\Earnings\\"}

MARKET_DATA_DICT_TICK_TYPE = {0 : "BID SIZE",
                1 : "BID PRICE",
                2 : "ASK PRICE",
                3 : "ASK SIZE",
                4 : "LAST PRICE",
                5 : "LAST SIZE",
                6 : "HIGH",
                7 : "LOW",
                8 : "VOLUME",
                9 : "CLOSE PRICE",
                10 : "BID OPTION COMPUTATION",
                11 : "ASK OPTION COMPUTATION",
                12 : "LAST OPTION COMPUTATION",
                13 : "MODEL OPTION COMPUTATION",
                14 : "OPEN_TICK",
                15 : "LOW 13 WEEK",
                16 : "HIGH 13 WEEK",
                17 : "LOW 26 WEEK",
                18 : "HIGH 26 WEEK",
                19 : "LOW 52 WEEK",
                20 : "HIGH 52 WEEK",
                21 : "AVG VOLUME",
                22 : "OPEN INTEREST",
                23 : "OPTION HISTORICAL VOL",
                24 : "OPTION IMPLIED VOL",
                27 : "OPTION CALL OPEN INTEREST",
                28 : "OPTION PUT OPEN INTEREST",
                29 : "OPTION CALL VOLUME"}
