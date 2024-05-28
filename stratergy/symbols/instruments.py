import pandas as pd
import csv 

def get_instrument(exchange_token):
    if str(exchange_token).strip() == '':
        return None
    exchange_token = float(exchange_token)
    df = pd.read_csv('complete.csv')
    instrument = df[df['exchange_token'] == exchange_token]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['instrument_key']
    
def get_instrument_type(exchange_token):
    if str(exchange_token).strip() == '':
        return None
    exchange_token = float(exchange_token)
    df = pd.read_csv('complete.csv')
    instrument = df[df['exchange_token'] == exchange_token]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['instrument_type']


def get_exchange(exchange_token):
    if str(exchange_token).strip() == '':
        return None
    exchange_token = float(exchange_token)
    df = pd.read_csv('complete.csv')
    instrument = df[df['exchange_token'] == exchange_token]
    if instrument.empty:
        return None
    else:
        return instrument.iloc[0]['exchange']



def get_symbol(exchange_token):
    if str(exchange_token).strip() == '':
        return None
    exchange_token = float(exchange_token)
    df = pd.read_csv('complete.csv')
    instrument = df[df['exchange_token'] == exchange_token]
    if instrument.empty:
        return None
    else:
        if str(instrument.iloc[0]["tradingsymbol"]).strip() == 'nan':
            return instrument.iloc[0]["instrument_key"]
        else:
            return instrument.iloc[0]["tradingsymbol"]

import csv

def get_dhan_symbol(exchange_token, instrument_type):
    if not exchange_token or str(exchange_token).strip() == '' or not instrument_type or str(instrument_type).strip() == '':
        return None
    file_path = 'dhan_syb.csv'
    exchange_token = float(exchange_token)
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if float(row['SEM_SMST_SECURITY_ID']) == exchange_token and row['SEM_EXCH_INSTRUMENT_TYPE'] == instrument_type:
                return row['SEM_TRADING_SYMBOL']
    return None

# Example usage:
# token = '35545'
# token = float(token)
# result = get_symbol(token)
# print('-=-=-=-=-=-Instrument-=-=-===-=--=--')
# print(result)

# df = pd.read_csv('complete.csv')
# # for x in df['exchange_token']:
# #     print(x)
# print(df['exchange_token'])
# if 'USDINR2421680.1CE' in df['exchange_token']:
#     print('Hello World')
