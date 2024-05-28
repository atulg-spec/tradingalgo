from trade.alerts.suscription_check import suscribed,present
from django.utils import timezone
from trade.models import *
from py5paisa import FivePaisaClient
import pyotp
from trade.alerts.getsymbols import get_quantity

#---------------------5 PAISA API------------------------------

def paisa_order(syntax,json_data):
    apiob = paisaapi.objects.all()
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
            cred={
                "APP_NAME":x.apiname,
                "APP_SOURCE":x.appsource,
                "USER_ID":x.userid,
                "PASSWORD":x.password,
                "USER_KEY":x.userkey,
                "ENCRYPTION_KEY":x.encryptionkey
            }
            client = FivePaisaClient(cred=cred)
            totp = pyotp.TOTP(x.secretkey, interval=30)
            tcode = totp.now()
            client.get_totp_session(x.clientcode,tcode,x.mpin)
            # ASSIGNMENT
            if json_data[syntax]["otype"].upper == "BUY":
                otype = 'B'
            else:
                otype = 'S'
            if json_data[syntax]["segment"].upper() == 'NSE':
                segment = 'N'
            elif json_data[syntax]["segment"].upper() == 'BSE':
                segment = 'B'
            else:
                segment = 'M'
            if json_data[syntax]["ptype"].upper() == 'INTRADAY':
                intraday = True
            else:
                intraday = False
            # END ASSIGNMENT
            o = client.place_order(
                OrderType=otype,
                Exchange=segment,
                ExchangeType=json_data[syntax]["extype"],
                ScripCode = int(json_data[syntax]["token"]),
                Qty=int(qty),
                Price=int(json_data[syntax]["price"]),
                StopLossPrice = int(json_data[syntax]["stoploss"]),
                IsIntraday=intraday
                )
            status="success"
            book = client.order_book()
            for i in book:
                if i["BrokerOrderId"] == o["BrokerOrderID"]:
                    order = client.get_trade_history(i["ExchOrderID"])
            hquantity = qty
            if json_data[syntax]['otype'].upper() == "BUY":
                hbuy = order["TradeHistoryData"][0]["TradePrice"]
            else:
                hsell = order["TradeHistoryData"][0]["TradePrice"]
            if order == None:
                order = "Invalid Credentials"
                status="Failed"
            hsymbol = order["TradeHistoryData"][0]["Symbol"]
            hquantity = qty
            if json_data[syntax]['otype'].upper() == "BUY":
                hbuy=float(hbuy)
                trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='5paisa',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                trade.save()
            elif json_data[syntax]['otype'].upper() == "SELL":
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
            order = e
            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='5paisa',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
            trade.save()
    # ------------END 5 PAISA API--------------------