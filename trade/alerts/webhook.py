from trade.models import *
import pyotp
import requests
import json
import threading
import time
from .getsymbols import get_symbol
from alerts.models import IndexTokens
SmartConnect = ''
try:
    from SmartApi import SmartConnect
except:
    from smartapi import SmartConnect

sessions = []
api_key = 'qy5tDMrp'
clientId = 'A400396'
pwd = '0786'
smartApi = SmartConnect(api_key)
token = "HPT2ZFLWDZMD77EAGVIEDQTQMI"
totp=pyotp.TOTP(token).now()
smartApi.generateSession(clientId, pwd, totp)
sessions.append(smartApi)
api_key = 'hVYSjEo2'
smartApi2 = SmartConnect(api_key)
smartApi2.generateSession(clientId, pwd, totp)
sessions.append(smartApi2)
api_key = '1IXBKk24'
smartApi3 = SmartConnect(api_key)
smartApi3.generateSession(clientId, pwd, totp)
sessions.append(smartApi3)

def get_price(segment,symbol,token,c=1):
    for x in sessions:
        try:
            get = x.ltpData(segment,symbol,token)
            return get['data']['ltp']
        except:
            continue
    co = c+1
    if co == 4:
        return 0.0
    return get_price(segment,symbol,token,c=co)


def place_tsl_alert(json_syntax):
    ur = webhookurl.objects.filter(use='smartorder').first()
    url = f'https://smart-algo.in/alert/{ur.url}'
    ttype = "SELL"
    if json_syntax["ttype"] == "SELL":
        ttype = "BUY"
    data = {
        "syntaxcount": 1,
        "syntax1": {
            "broker": json_syntax["broker"],
            "variety": json_syntax["variety"],
            "segment":json_syntax["segment"],
            "symbol": json_syntax["symbol"],
            "token": json_syntax["token"],
            "option": "False",
            "price":"0",
            "otype": "MARKET",
            "ptype": json_syntax["ptype"],
            "ttype": ttype,
            "extype": "C",
            "stoploss": "0",
            "position":"open",
            "users":json_syntax["users"]
        }}
    data = json.dumps(data)
    response = requests.post(url,data)


def eval_order(json_syntax):
    in_token = IndexTokens.objects.first()
    BANKNIFTY = in_token.BANKNIFTY
    CRUDEOIL = in_token.CRUDEOIL
    SENSEX = in_token.BANKNIFTY
    NIFTY = in_token.NIFTY
    FININFTY = in_token.FIN_NIFTY
    BANKEX = in_token.BANKNIFTY
    ttype = json_syntax['ttype']
    symbol = json_syntax['symbol']
    last_price = 0.0
    ordered_price = get_price(json_syntax['segment'],symbol,json_syntax['token'])
    index_list = {'BANKNIFTY':{'segment': 'NSE', 'symbol': 'BANKNIFTY', 'token': BANKNIFTY},'CRUDEOIL':{'segment': 'MCX', 'symbol': 'CRUDEOIL', 'token': CRUDEOIL},'SENSEX':{'segment': 'NSE', 'symbol': 'SENSEX', 'token': SENSEX},'NIFTY':{'segment': 'NSE', 'symbol': 'NIFTY', 'token': NIFTY},'BANKEX':{'segment': 'NSE', 'symbol': 'BANKEX', 'token': BANKEX},'FINNIFTY':{'segment': 'NSE', 'symbol': 'FINNIFTY', 'token': FININFTY}}
    opseg = ''
    opsymbol = ''
    optoken = ''
    start_time = time.time()
    end_time = start_time + 180
    if json_syntax['option'] == 'True':
        opsymbol = get_symbol(json_syntax['symbol'])
        print('opsymbol')
        print(opsymbol)
        detail = index_list.get(opsymbol)
        optoken = detail['token']
        opseg = detail['segment']
        ordered_price = get_price(opseg,opsymbol,optoken)
    if ordered_price == 0.0:
        return False
    # BANKNIFTY PUT TRAILING LOGIC
    if json_syntax['option'] == 'True' and get_symbol(json_syntax['symbol']) == opsymbol and (json_syntax['symbol'].endswith('PE') or json_syntax['symbol'].endswith('P')):
        tsl_rate = 2
        stoploss = ordered_price + float(json_syntax['stoploss'])
        target = ordered_price - float(json_syntax['target'])
        minimum = ordered_price
        last_price = ordered_price
        trail = trailing_stoploss.objects.create(symbol=symbol,status='initiated',ordered_price=ordered_price,stoploss=stoploss,target=target,transaction_type=ttype)
        trail.save()
        ordered = False
        trail.status = 'processing'
        trail.save()
        while not ordered :
            current_price = get_price(opseg,opsymbol,optoken)
            # current_price = get_price(json_syntax['segment'],symbol,json_syntax['token'])
            change = last_price - current_price
            tsl = change/tsl_rate
            trail.current_price = current_price
            trail.save()
            if tsl >= 0 and current_price < minimum and time.time() > end_time:
                stoploss = stoploss - tsl
                trail.stoploss = round(stoploss,2)
                trail.save()
                minimum = current_price
            # STOP LOSS
            if current_price >= stoploss:
                thread = threading.Thread(target=place_tsl_alert,args = (json_syntax,))
                thread.start()
                trail.status = 'completed'
                trail.exit_avg = round(current_price,2)
                trail.message = 'Stoploss Hits !'
                trail.save()
                ordered = True
                return True
            # TARGET
            if current_price <= target:
                tsl_rate = 1.4
                stoploss = target
                target = stoploss - float(json_syntax['target'])
                trail.target = target
                trail.stoploss = stoploss
                trail.message = "Target Reached Still Trading !"
                trail.save()
            if trail.status == 'completed' or trail.status == 'cancelled':
                ordered = True
                return True
            last_price = current_price
            time.sleep(2)
    # BUY TRAILING LOGIC
    elif ttype == 'BUY':
        tsl_rate = 2
        stoploss = ordered_price - float(json_syntax['stoploss'])
        target = ordered_price + float(json_syntax['target'])
        maximum = ordered_price
        trail = trailing_stoploss.objects.create(symbol=symbol,status='initiated',ordered_price=ordered_price,stoploss=stoploss,target=target,transaction_type=ttype)
        trail.save()
        ordered = False
        trail.status = 'processing'
        trail.save()
        last_price = ordered_price
        while not ordered :
            if json_syntax['option'] == 'True' and get_symbol(json_syntax['symbol']) == opsymbol:
                current_price = get_price(opseg,opsymbol,optoken)
            else:
                current_price = get_price(json_syntax['segment'],symbol,json_syntax['token'])
            change = current_price - last_price
            tsl = change/tsl_rate
            if tsl >= 0 and current_price > maximum and time.time() > end_time:
                stoploss = stoploss + tsl
                trail.stoploss = round(stoploss,2)
                trail.save()
                maximum = current_price
            trail.current_price = current_price
            trail.save()
            # STOP LOSS
            if current_price <= stoploss:
                thread = threading.Thread(target=place_tsl_alert,args = (json_syntax,))
                thread.start()
                trail.status = 'completed'
                trail.exit_avg = round(current_price,2)
                trail.message = 'Stoploss Hits !'
                trail.save()
                ordered = True
                return True
            # TARGET
            if current_price >= target:
                tsl_rate = 1.4
                stoploss = target
                target = stoploss + float(json_syntax['target'])
                trail.target = target
                trail.stoploss = stoploss
                trail.message = "Target Reached Still Trading !"
                trail.save()
            if trail.status == 'completed' or trail.status == 'cancelled':
                ordered = True
                return True
            last_price = current_price
            time.sleep(1)
    # SELL TRAILING LOGIC
    else :
        tsl_rate = 2
        stoploss = ordered_price + float(json_syntax['stoploss'])
        target = ordered_price - float(json_syntax['target'])
        minimum = ordered_price
        last_price = ordered_price
        trail = trailing_stoploss.objects.create(symbol=symbol,status='initiated',ordered_price=ordered_price,stoploss=stoploss,target=target,transaction_type=ttype)
        trail.save()
        ordered = False
        trail.status = 'processing'
        trail.save()
        while not ordered :
            if json_syntax['option'] == 'True' and get_symbol(json_syntax['symbol']) == opsymbol:
                current_price = get_price(opseg,opsymbol,optoken)
            else:
                current_price = get_price(json_syntax['segment'],symbol,json_syntax['token'])
            # current_price = get_price(json_syntax['segment'],symbol,json_syntax['token'])
            change = last_price - current_price
            tsl = change/tsl_rate
            trail.current_price = current_price
            trail.save()
            if tsl >= 0 and current_price < minimum and time.time() > end_time:
                stoploss = stoploss - tsl
                trail.stoploss = round(stoploss,2)
                trail.save()
                minimum = current_price
            # STOP LOSS
            if current_price >= stoploss:
                thread = threading.Thread(target=place_tsl_alert,args = (json_syntax,))
                thread.start()
                trail.status = 'completed'
                trail.exit_avg = round(current_price,2)
                trail.message = 'Stoploss Hits !'
                trail.save()
                ordered = True
                return True
            # TARGET
            if current_price <= target:
                tsl_rate = 1.4
                stoploss = target
                target = stoploss - float(json_syntax['target'])
                trail.target = target
                trail.stoploss = stoploss
                trail.message = "Target Reached Still Trading !"
                trail.save()
            if trail.status == 'completed' or trail.status == 'cancelled':
                ordered = True
                return True
            last_price = current_price
            time.sleep(2)
