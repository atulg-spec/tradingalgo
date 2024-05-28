# ----------------FYERS API--------------------
from trade.alerts.suscription_check import suscribed,present
from fyers_api import fyersModel
from django.utils import timezone
from trade.models import *
from trade.alerts.getsymbols import get_quantity

def fyers_order(syntax,json_data):
    apiob = fyersapi.objects.all()
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
            qty = get_quantity(x.apiuser,json_data[syntax]["symbol"])
            json_data[syntax]['quantity']=qty
            clientid = x.clientid
            accesstoken = x.accesstoken
            fyers = fyersModel.FyersModel(client_id=clientid, token=accesstoken)
            # POSITIONS
            try:
                if json_data[syntax]["position"].upper() == "CLOSE":
                    dic = fyers.positions()
                    for i in dic["netPositions"]:
                        if int(i["netQty"]) != 0:
                            data = {
                                    "symbol":i['symbol'],
                                    "qty":i['netQty'],
                                    "type":2,
                                    "side":-1,
                                    "productType":"INTRADAY",
                                    "limitPrice":0,
                                    "stopPrice":0,
                                    "validity":"DAY",
                                    "disclosedQty":0,
                                    "offlineOrder":"False",
                                }
                            order = fyers.place_order(data=data)
                            orderid = {"id":order["id"]}
                            order = fyers.get_orders(data=orderid)
                            status= "success"
                            hsell = order["data"][0]["tradedPrice"]
                            hquantity = i['netQty']
                            hsymbol = order["data"][0]["symbol"]
                            today = timezone.now().date()
                            old = tradebook.objects.filter(apiuser=x.apiuser,datetime__date=today,symbol=hsymbol).reverse().first()
                            old.response = order
                            old.sell=float(order["data"][0]["tradedPrice"])
                            old.p_l = (float(old.sell)*float(i['netQty']))-(float(old.buy)*float(i['netQty']))
                            old.save()
            except:
                pass
            # END POSITION
            # ASSIGNMENT
            if json_data[syntax]["otype"].upper() == "LIMIT":
                otype = 1
            elif json_data[syntax]["otype"].upper() == "MARKET":
                otype = 2
            elif json_data[syntax]["otype"].upper() == "STOP":
                otype = 3
            else:
                otype = 4
            if json_data[syntax]["ttype"].upper() == "BUY":
                ttype = 1
            else:
                ttype = -1
            # END ASSIGNMENT
            data = {
                "symbol":f"{json_data[syntax]['segment']}:{json_data[syntax]['symbol']}",
                "qty":qty,
                "type":otype,
                "side":ttype,
                "productType":json_data[syntax]['ptype'],
                "limitPrice":json_data[syntax]['price'],
                "stopPrice":json_data[syntax]['stoploss'],
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":"False",
            }
            order = fyers.place_order(data)
            orderid = {"id":order["id"]}
            order = fyers.get_orders(data=orderid)
            status= "success"
            hbuy = order["data"][0]["tradedPrice"]
            hsell = order["data"][0]["tradedPrice"]
            hquantity = qty
            hsymbol = order["data"][0]["symbol"]
            if json_data[syntax]["ttype"].upper() == "BUY":
                hbuy=float(order["data"][0]["tradedPrice"])
                trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='fyers',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                trade.save()
            elif json_data[syntax]["ttype"].upper() == "SELL":
                today = timezone.now().date()
                old = tradebook.objects.filter(apiuser=x.apiuser,datetime__date=today,symbol=hsymbol).reverse().first()
                old.response = order
                old.sell=float(order["data"][0]["tradedPrice"])
                old.p_l = (float(old.sell)-float(old.buy))*float(qty)
                old.save()
            else:
                pass
            allplan.objects.filter(user=x.apiuser,active=True).update(placed_order = models.F('placed_order') + 1)
        except Exception as e:
            status="failed"
            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='fyers',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
            trade.save()
# ---------END FYERS API