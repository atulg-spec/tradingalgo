from trade.alerts.suscription_check import suscribed,present
from trade.models import *
from django.utils import timezone
from dhanhq import dhanhq
from trade.notifications.notify_alert import api_notify
from trade.alerts.getsymbols import get_quantity


# ----------------DHAN HQ API--------------------
def dhan_order(syntax,json_data):
    apiob = dhanapi.objects.all()
    order = ""
    status= ""
    hquantity="0"
    hsymbol="s"
    hbuy = 0
    hsell= 0
    qty=0
    f = open("apierr.txt", "a")
    f.write(f'Order dhan me bhi \n')
    f.close()
    for x in apiob:
        if not present(x.apiuser,json_data[syntax]):
            continue
        if not suscribed(x.apiuser):
            continue
        if not x.is_trading:
            continue
        f = open("apierr.txt", "a")
        f.write(f'User mila \n')
        f.close()
        try:
            qty = get_quantity(x.apiuser,json_data[syntax]["symbol"])
            clientid = x.clientid
            price=int(json_data[syntax]["price"])
            quantity=int(qty)
            if json_data[syntax]['segment'] == 'NFO':
                json_data[syntax]['segment'] = 'FNO'
            if json_data[syntax]['segment'] == 'BFO':
                json_data[syntax]['segment'] = 'BSE_FNO'
            accesstoken = x.accesstoken
            dhan = dhanhq(clientid,accesstoken)
            dic = dhan.get_positions()
            if dic['status'] == 'failure':
                api_notify(x.apiuser,x.apiname,'DHAN HQ')
                order = str({'s': 'error', 'code': -8, 'message': 'Unauthorised Access !'})
                ob = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='dhan',status='failed',quantity=hquantity,symbol=hsymbol,buy=hbuy)
                ob.save()
                continue
            transactiontype = f"dhan.{json_data[syntax]['ttype'].upper()}"
            transactiontype = eval(transactiontype)
            segment = f"dhan.{json_data[syntax]['segment'].upper()}"
            segment = eval(segment)
            if json_data[syntax]['ptype'].upper() == 'INTRADAY':
                json_data[syntax]['ptype'] = 'INTRA'
            producttype = f"dhan.{json_data[syntax]['ptype'].upper()}"
            producttype = eval(producttype)
            if json_data[syntax]['ptype'].upper() == 'INTRA':
                json_data[syntax]['ptype'] = 'INTRADAY'
            if json_data[syntax]['segment'] == 'FNO':
                json_data[syntax]['segment'] = 'NFO'
            if json_data[syntax]['segment'] == 'BFO':
                json_data[syntax]['segment'] = 'BSE_FNO'
            # ------------------POSITION------------------------
            try:
                if json_data[syntax]["position"].upper() == "CLOSE":
                    dic = dhan.get_positions()
                    print('----------------------------')
                    print('DHAN HQ Positions')
                    print(dic)
                    print('----------------------------')
                    for i in dic["data"]:
                        if i["positionType"].upper() != "CLOSED":
                            print('DONE')
                            print('----------')
                            # segmentvar =f"dhan.{i['exchangeSegment']}"
                            # segmentvar = eval(segmentvar)
                            order = dhan.place_order(
                                    transaction_type=dhan.SELL,
                                    exchange_segment=i['exchangeSegment'],
                                    product_type=dhan.INTRA,
                                    order_type=dhan.MARKET,
                                    price=0,
                                    quantity=i['netQty'],
                                    security_id=i['securityId'],
                                )
                            print('FINAL DONE')
                            try:
                                status = order["status"].lower()
                                order_id = order["data"]["orderId"]
                                book = dhan.get_trade_book(order_id)
                                hquantity = book["data"][0]["tradedQuantity"]
                                hsymbol = book["data"][0]["tradingSymbol"]
                                hsell = book["data"][0]["tradedPrice"]
                                order = book
                                today = timezone.now().date()
                                old = tradebook.objects.filter(apiuser=x.apiuser,datetime__date=today,symbol=hsymbol).reverse().first()
                                old.response = order
                                old.sell=float(hsell)
                                old.p_l = (float(old.sell)*float(i['netQty']))-(float(old.buy)*float(i['netQty']))
                                old.save()
                            except Exception as e:
                                status = "failed"
            except Exception as e:
                print(e)
            # END POSITION
            f = open("apierr.txt", "a")
            f.write(f'Position ke baad bhi \n')
            f.close()
            otype = json_data[syntax]['otype'].upper()
            ordertype = eval(f"dhan.{json_data[syntax]['otype']}")
            order = dhan.place_order(
                                transaction_type=transactiontype,
                                exchange_segment=segment,
                                product_type=producttype,
                                order_type=ordertype,
                                price=price,
                                quantity=qty,
                                security_id=json_data[syntax]["token"],
                            )
            f = open("apierr.txt", "a")
            f.write(f'Order {order} \n')
            f.close()
            print(f'Order, {order}')
            try:
                status = order["status"].lower()
                order_id = order["data"]["orderId"]
                book = dhan.get_trade_book(order_id)
                hquantity = book["data"][0]["tradedQuantity"]
                hsymbol = book["data"][0]["tradingSymbol"]
                if json_data[syntax]['ttype'].upper() == "BUY":
                    hbuy = book["data"][0]["tradedPrice"]
                else:
                    hsell = book["data"][0]["tradedPrice"]
                order = book
            except Exception as e:
                status = "failed"
                hsymbol = json_data[syntax]['segment'].upper()
            hquantity = qty
            if json_data[syntax]['ttype'].upper() == "BUY":
                hbuy=float(hbuy)
                trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker="dhan",status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
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
            f = open("apierr.txt", "a")
            f.write(f'Final error, {e} \n')
            f.close()
            status="failed"
            order = f"Error: {e}"
            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='dhan',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
            trade.save()
    # ----------------END DHAN HQ API---------------------
