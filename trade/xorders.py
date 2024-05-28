from smartapi import SmartConnect
from trade.models import *
import yfinance as yf
import pyotp
from fyers_api import accessToken
from smartapi import SmartConnect
from fyers_api import fyersModel
from dhanhq import dhanhq
from django.utils import timezone
from py5paisa import FivePaisaClient
from py5paisa.order import Order, OrderType, Exchange
from fyers_api import accessToken
from pya3 import *
import requests
import json
import re
import threading


api_key = 'qy5tDMrp'
clientId = 'A400396'
pwd = '0786'
smartApi = SmartConnect(api_key)
token = "HPT2ZFLWDZMD77EAGVIEDQTQMI"
totp=pyotp.TOTP(token).now()
correlation_id = "abc123"
dataob = smartApi.generateSession(clientId, pwd, totp)

def get_price(segment,symbol,token):
    print("called")
    try:
        get = smartApi.ltpData(segment,symbol,token)
        return get['data']['ltp']
    except:
        return get_price(segment,symbol,token)
        
        

def palce_limit_order(price,stratob,symbol,symboltoken,transactiontype,segment,producttype,squareoff,stoploss,trailingstoploss):
    limit_order = Limitorder.objects.create(symbol=symbol,status='initiated',limit_price=price)
    limit_order.save()
    ordered = False
    while not ordered:
        if limit_order.status == 'completed':
            return True
        current_price = get_price(segment,symbol,token)
        limit_order.current_price = current_price
        limit_order.status = "processing"
        limit_order.save()
        if (
            (transactiontype == 'BUY' and current_price <= price) or
            (transactiontype == 'SELL' and current_price >= price)
        ):
            for x in stratob:
                if x.broker == "Angel ONE":
                    apiob = angelapi.objects.filter(apiid=x.apiid).first()
                    try:
                        clientid = apiob.clientid
                        rtoken = apiob.rtoken
                        apikey = apiob.apikey
                        authtoken = apiob.authtoken
                        obj=SmartConnect(api_key=apikey,
                                access_token = authtoken,
                                refresh_token = rtoken)
                        data =  {
                            "variety": 'NORMAL',
                            "tradingsymbol": symbol,
                            "symboltoken": symboltoken,
                            "transactiontype": transactiontype,
                            "exchange": segment,
                            "ordertype": 'Market',
                            "producttype": producttype,
                            "duration": "DAY",
                            "price": '0.0',
                            "squareoff": squareoff,
                            "stoploss": stoploss,
                            "quantity": x.quantity,
                        }
                        orderid=obj.placeOrder(data)
                        book = obj.orderBook()["data"]
                        for i in book:
                            if i["orderid"] == orderid:
                                order = str(i)
                                hbuy = str(i["averageprice"])
                                hsell= str(i["averageprice"])
                                if str(i["status"]) == "rejected":
                                    status="rejected"
                                else:
                                    status="success"
                        hquantity = x.quantity
                        hsymbol = symbol.upper()
                        if transactiontype.upper() == "BUY":
                            hbuy=float(hbuy)
                            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                            trade.save()
                        elif transactiontype.upper() == "SELL":
                            today = timezone.now().date()
                            old = tradebook.objects.filter(apiuser=x.user,datetime__date=today,symbol=hsymbol).order_by('datetime').reverse().first()
                            old.response = (order)
                            old.sell=float(hsell)
                            old.p_l = (float(old.sell)*float(x.quantity))-(float(old.buy)*float(x.quantity))
                            old.save()
                        status="success"
                    except Exception as e:
                        status="failed"
                    x.status = status
                    x.save()
                    ordered = True
                # ---------------------Dhan HQ-------------------
                elif x.broker == "Dhan HQ":
                    try:
                        apiob = dhanapi.objects.filter(apiid=x.apiid).first()
                        clientid = apiob.clientid
                        accesstoken = apiob.accesstoken
                        dhan = dhanhq(clientid,accesstoken)
                        transactiontype = f"dhan.{transactiontype.upper()}"
                        transactiontype = eval(transactiontype)
                        segm = f"dhan.{segment.upper()}"
                        segm = eval(segm)
                        protype = f"dhan.{producttype.upper()}"
                        protype = eval(protype)
                        ordtype = dhan.MARKET
                        order = dhan.place_order(
                            tag='smart-algo',
                            transaction_type=transactiontype,
                            exchange_segment=segm,
                            product_type=protype,
                            order_type=ordtype,
                            validity='DAY',
                            security_id=int(symboltoken),
                            quantity=int(x.quantity),
                            disclosed_quantity=0,
                            price=int(0),
                            after_market_order=False,
                            amo_time='OPEN',
                            bo_profit_value=0,
                            bo_stop_loss_Value=float(stoploss),
                            drv_expiry_date=None,
                            drv_options_type=None,
                            drv_strike_price=None    
                        )
                        try:
                            status = order["status"].lower()
                            order_id = order["data"]["orderId"]
                            book = dhan.get_trade_book(order_id)
                            hquantity = book["data"][0]["tradedQuantity"]
                            hsymbol = book["data"][0]["tradingSymbol"]
                            if transactiontype.upper() == "BUY":
                                hbuy = book["data"][0]["tradedPrice"]
                            else:
                                hsell = book["data"][0]["tradedPrice"]
                            order = book
                        except Exception as e:
                            status = "failed"
                        hquantity = x.quantity
                        hsymbol = symbol.upper()
                        if transactiontype.upper() == "BUY":
                            hbuy=float(hbuy)
                            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                            trade.save()
                        elif transactiontype.upper() == "SELL":
                            today = timezone.now().date()
                            old = tradebook.objects.filter(apiuser=x.user,datetime__date=today,symbol=hsymbol).order_by('datetime').reverse().first()
                            old.response = order
                            old.sell=float(hsell)
                            old.p_l = (float(old.sell)*float(x.quantity))-(float(old.buy)*float(x.quantity))
                            old.save()
                        else:
                            pass
                    except Exception as e:
                        status="failed"
                    x.status = status
                    x.save()
                    ordered = True
                        # --------------Alice Blue -----------------
                elif x.broker == "Alice Blue":
                    try:
                        apiob = aliceapi.objects.filter(apiid=x.apiid).first()
                        clientid = apiob.userid
                        apitoken = apiob.apikey
                        alice = Aliceblue(user_id=clientid,api_key=apitoken)
                        alice.get_session_id()
                        transactiontype = f"TransactionType.{transactiontype}"
                        transactiontype = eval(transactiontype)
                        ordtype = OrderType.Market
                        protype = f"ProductType.{producttype}"
                        protype = eval(protype)
                        exchange = segment
                        sym = symbol
                        order = alice.place_order(transaction_type = transactiontype,
                            instrument = alice.get_instrument_by_symbol(exchange, sym),
                            quantity = int(x.quantity),
                            order_type = ordtype,
                            product_type = protype,
                            price = float(0.0),
                            stop_loss = eval(stoploss),
                            square_off = eval(str(squareoff)),
                            trailing_sl = eval(str(trailingstoploss)),
                            is_amo = False,
                            order_tag='smart-algo')
                        status="success"
                        o = order["NOrdNo"]
                        ord = alice.get_order_history(o)
                        order = alice.get_order_history(ord["Nstordno"])
                        if transactiontype.upper() == "BUY":
                            hbuy = order["Avgprc"]
                        else:
                            hsell = order["Avgprc"]
                        hsymbol = order["Trsym"]
                        hsymbol = symbol
                        hquantity = x.quantity
                        if transactiontype.upper() == "BUY":
                            hbuy=float(hbuy)
                            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                            trade.save()
                        elif transactiontype.upper() == "SELL":
                            today = timezone.now().date()
                            old = tradebook.objects.filter(apiuser=x.user,datetime__date=today,symbol=hsymbol).order_by('datetime').reverse().first()
                            old.response = order
                            old.sell=float(hsell)
                            old.p_l = (float(old.sell)*float(x.quantity))-(float(old.buy)*float(x.quantity))
                            old.save()
                        else:
                            pass
                    except Exception as e:
                        status="failed"
                        order = e
                        trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
                        trade.save()
                    x.status = status
                    x.save()
                    ordered = True
                elif x.broker == "5 Paisa":
                    OrderType = ""
                    Exchange = ""
                    ExchangeType = ""
                    # ORDER TYPE
                    if transactiontype.upper() == "BUY":
                        OrderType = "B"
                    else:
                        OrderType = "S"
                    # EXCHANGE
                    if segment.upper() == "NSE":
                        Exchange = "N"
                    elif segment.upper() == "BSE":
                        Exchange = "B"
                    else:
                        Exchange = "M"
                    # EXCHANGE TYPE
                    if producttype.upper() == "CASH":
                        ExchangeType = "C"
                    elif producttype.upper() == "DERIVATIVE":
                        ExchangeType = "D"
                    else:
                        ExchangeType = "U"
                    try:
                        apiob = paisaapi.objects.filter(apiid=x.apiid).first()
                        cred={
                            "APP_NAME":apiob.apiname,
                            "APP_SOURCE":apiob.appsource,
                            "USER_ID":apiob.userid,
                            "PASSWORD":apiob.password,
                            "USER_KEY":apiob.userkey,
                            "ENCRYPTION_KEY":apiob.encryptionkey
                        }
                        client = FivePaisaClient(cred=cred)
                        totp = pyotp.TOTP(apiob.secretkey, interval=30)
                        tcode = totp.now()
                        client.get_totp_session(apiob.clientcode,tcode,apiob.mpin)
                        o = client.place_order(OrderType=OrderType,Exchange=Exchange,ExchangeType=ExchangeType,ScripCode = int(symboltoken), Qty=x.quantity, Price=int(0),StopLossPrice=int(stoploss))
                        status="success"
                        book = client.order_book()
                        for i in book:
                            if i["BrokerOrderId"] == o["BrokerOrderID"]:
                                order = client.get_trade_history(i["ExchOrderID"])
                        hquantity = x.quantity
                        if OrderType.upper() == "B":
                            hbuy = order["TradeHistoryData"][0]["TradePrice"]
                        else:
                            hsell = order["TradeHistoryData"][0]["TradePrice"]
                        if order == None:
                            order = "Invalid Credentials"
                            status="Failed"
                        hsymbol = order["TradeHistoryData"][0]["Symbol"]
                        hquantity = x.quantity
                        if OrderType.upper() == "B":
                            hbuy=float(hbuy)
                            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker="5 Paisa",status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                            trade.save()
                        elif OrderType.upper() == "S":
                            today = timezone.now().date()
                            old = tradebook.objects.filter(apiuser=x.user,datetime__date=today,symbol=hsymbol).order_by('datetime').reverse().first()
                            old.response = order
                            old.sell=float(hsell)
                            old.p_l = (float(old.sell)*float(x.quantity)-(float(old.buy)*float(x.quantity)))
                            old.save()
                        else:
                            pass
                    except Exception as e:
                        status="failed"
                        order = e
                        trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker="5 PAISA",status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
                        trade.save()
                    x.status = status
                    x.save()
                    ordered = True
                    # END 5 PAISA
                elif x.broker == "Fyers":
                    try:
                        apiob = fyersapi.objects.filter(apiid=x.apiid).first()
                        clientid = apiob.clientid
                        accesstoken = apiob.accesstoken
                        fyers = fyersModel.FyersModel(client_id=clientid, token=accesstoken)
                        fsymbol=f"{segment.upper()}:{symbol}"
                        side = 1
                        if transactiontype.upper() == "BUY":
                            side=1
                        else:
                            side=-1
                        data = {
                            "symbol":fsymbol,
                            "qty":x.quantity,
                            "type":2,
                            "side":side,
                            "productType":"BO",
                            "limitPrice":int(0),
                            "stopPrice":int(stoploss),
                            "validity":"DAY",
                            "takeProfit":int(stoploss)
                        }
                        order = fyers.place_order(data)
                        orderid = {"id":order["id"]}
                        order = fyers.get_orders(data=orderid)
                        status= "success"
                        hquantity = x.quantity
                        hsymbol = symbol.uppper()
                        if side == 1:
                            hbuy = order["data"][0]["tradedPrice"]
                        else:
                            hsell = order["data"][0]["tradedPrice"]
                        hsymbol = symbol
                        hquantity = x.quantity
                        if side == 1:
                            hbuy=float(hbuy)
                            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                            trade.save()
                        elif side == -1:
                            today = timezone.now().date()
                            old = tradebook.objects.filter(apiuser=x.apiuser,datetime__date=today,symbol=hsymbol).reverse().first()
                            old.response = order
                            old.sell=float(hsell)
                            old.p_l = (float(old.sell)*float(x.quantity))-(float(old.buy)*float(x.quantity))
                            old.save()
                        else:
                            pass
                    except Exception as e:
                        status="failed"
                    trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
                    trade.save()
                    x.status = status
                    x.save()
                    ordered = True
                else:
                    ordered = True
                    return None
            limit_order.status = "completed"
            limit_order.save()

def place_tsl_alert(json_syntax,current_price):
    url = 'https://smart-algo.in/alert/newmatch'
    print("yoooooooooooooooooo")
    print(json_syntax)
    data = {
        "syntaxcount": 1,
        "syntax1": {
            "broker": json_syntax["broker"],
            "variety": json_syntax["variety"],
            "segment":json_syntax["segment"],
            "symbol": json_syntax["symbol"],
            "token": json_syntax["token"],
            "option": json_syntax["option"],
            "price":"0",
            "otype": "MARKET",
            "ptype": json_syntax["ptype"],
            "ttype": "SELL",
            "stoploss": "0",
            "position":"clse"
        }}
    data = json.dumps(data)
    response = requests.post(url,data)
    print("kr$na")
    print(response.content)


def get_symbol(symbol):
    match = re.match(r'(.*?)(\d{2}[A-Z]{3}\d+)', symbol)
    if match:
        result = match.group(1)
        return result
    else:
        return symbol



def trailing_stop_loss(json_syntax):
    trailing_sl = json_syntax['trailing_sl']
    symbol = json_syntax['symbol']
    last_price = 0.0
    ordered_price = get_price(json_syntax['segment'],symbol,json_syntax['token'])
    max = ordered_price
    price = ordered_price - trailing_sl
    trail = trailing_stoploss.objects.create(symbol=symbol,status='initiated',trailing=price)
    trail.save()
    ordered = False
    trail.status = 'processing'
    trail.save()
    while not ordered :
        current_price = get_price(json_syntax['segment'],symbol,json_syntax['token'])
        print(current_price)
        print("trailing : ",price)
        if max < current_price:
            max = current_price
            price = current_price - trailing_sl
            trail.trailing = price
            trail.save()
        if current_price <= price:
            thread = threading.Thread(target=place_tsl_alert,args = (json_syntax,current_price))
            thread.start()
            trail.status = 'completed'
            trail.save()
            ordered = True
            break
            return True
        if trail.status == 'completed':
            ordered = True
            return True
        
# print(get_price(segment='MCX',symbol='CRUDEOIL23OCT8000CE',token='259284'))