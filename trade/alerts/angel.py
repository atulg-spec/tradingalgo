from trade.alerts.suscription_check import suscribed,present
from trade.models import *
from django.utils import timezone
try:
    from SmartApi import SmartConnect
except:
    from smartapi import smartConnect
from trade.notifications.notify_alert import api_notify
from trade.alerts.getsymbols import get_quantity


# --------------------ANGEL ONE API---------------------
def angel_order(syntax,json_data):
    apiob = angelapi.objects.all()
    order = ""
    status= ""
    hquantity="0"
    hsymbol="s"
    hbuy = 0
    hsell= 0
    qty=0
    for x in apiob:
        if not present(x.apiuser,json_data[syntax]):
            continue
        if not suscribed(x.apiuser):
            continue
        if not x.is_trading:
            continue
        try:
            print("angel one ")
            qty = get_quantity(x.apiuser,json_data[syntax]["symbol"])
            print(qty)
            qty = int(qty)
            orderid = ""
            clientid = x.clientid
            rtoken = x.rtoken
            apikey = x.apikey
            authtoken = x.authtoken
            obj=SmartConnect(api_key=apikey,
                    access_token = authtoken,
                    refresh_token = rtoken)
            pos = obj.position()
            print(pos)
            if str(pos) == "{'success': False, 'message': 'Invalid Token', 'errorCode': 'AG8001', 'data': ''}":
                api_notify(x.apiuser,x.apiname,'ANGEL ONE')
                order = str({'s': 'error', 'code': -8, 'message': 'Unauthorised Access !'})
                ob = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='angel',status='failed',quantity=hquantity,symbol=hsymbol,buy=hbuy)
                ob.save()
                continue
            # ------------------POSITION------------------------
            try:
                print(1)
                if json_data[syntax]["position"].upper() == "CLOSE":
                    dic = obj.position()
                    print('----------------------------')
                    print('ANGEL ONE Position')
                    print(dic)
                    print('----------------------------')
                    for i in dic["data"]:
                        if int(i["netqty"]) != 0:
                            param = {
                                "variety": "NORMAL",
                                "tradingsymbol": i["tradingsymbol"],
                                "symboltoken": i["symboltoken"],
                                "transactiontype": "SELL",
                                "exchange": i["exchange"],
                                "ordertype": "MARKET",
                                "producttype": "INTRADAY",
                                "duration": "DAY",
                                "price": "0",
                                "squareoff": "0",
                                "stoploss": "0",
                                "quantity": i["netqty"]
                                }
                            orderid=obj.placeOrder(param)
                            book = obj.orderBook()["data"]
                            for j in book:
                                if j["orderid"] == orderid:
                                    order = str(j)
                                    hbuy = str(j["averageprice"])
                                    hsell= str(j["averageprice"])
                                    hsymbol= str(j["tradingsymbol"])
                                    if str(j["status"]) == "rejected":
                                        status="rejected"
                                    else:
                                        status="success"
                            today = timezone.now().date()
                            old = tradebook.objects.filter(apiuser=x.apiuser,datetime__date=today,symbol=hsymbol).reverse().first()
                            old.response = order
                            old.sell=float(hsell)
                            old.p_l = (float(old.sell)*float(i["buyqty"]))-(float(old.buy)*float(i["buyqty"]))
                            old.save()
            except:
                pass
            # ----------------END POSITION-------------------
            print(2)
            ptype = json_data[syntax]['ptype']
            if ptype == 'CNC':
                ptype = 'DELIVERY'
            elif ptype == 'NRML':
                ptype = 'CARRYFORWARD'
            data = {
                "variety":json_data[syntax]['variety'],
                "tradingsymbol": json_data[syntax]['symbol'],
                "symboltoken": json_data[syntax]['token'],
                "transactiontype": json_data[syntax]['ttype'],
                "exchange": json_data[syntax]['segment'],
                "ordertype": json_data[syntax]['otype'],
                "producttype": ptype,
                "duration": "DAY",
                "price": json_data[syntax]['price'],
                "stoploss": json_data[syntax]['stoploss'],
                "quantity": qty
            }
            print(data)
            print(3)
            orderid=obj.placeOrder(data)
            print(6)
            book = obj.orderBook()["data"]
            print(5)
            for i in book:
                if i["orderid"] == orderid:
                    order = str(i)
                    hbuy = str(i["averageprice"])
                    hsell= str(i["averageprice"])
                    if str(i["status"]) == "rejected":
                        status="rejected"
                    else:
                        status="success"
            hquantity = qty
            hsymbol = json_data[syntax]['symbol'].upper()
            print(order)
            print(4)
            if json_data[syntax]['ttype'].upper() == "BUY":
                hbuy=float(hbuy)
                trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='angel',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                trade.save()
            
            elif json_data[syntax]['ttype'].upper() == "SELL":
                today = timezone.now().date()
                old = tradebook.objects.filter(apiuser=x.apiuser,datetime__date=today,symbol=hsymbol).reverse().first()
                old.response = order
                old.sell=float(hsell)
                old.p_l = (float(old.sell)-float(old.buy))*float(qty)
                old.save()
            else:
                pass
            allplan.objects.filter(user=x.apiuser,active=True).update(placed_order = models.F('placed_order') + 1)
        except Exception as e:
            status="failed"
            order = order + f" MESSAGE ERROR: Error: {e}"
            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='angel',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
            trade.save()
    #-----------------END ANGEL ONE API------------------------------
