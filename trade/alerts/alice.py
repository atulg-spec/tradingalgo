import hashlib
import json
from django.utils import timezone
from trade.alerts.suscription_check import suscribed,present
from trade.models import *
import requests
from trade.notifications.notify_alert import api_notify
from trade.alerts.getsymbols import get_quantity

# ----------------ALICE BLUE API--------------------
# CHECKSUM
def checksum(input_string):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    checksum = sha256.hexdigest()
    return checksum

# GENERATE SESSION ID
def alice_session(userid,apikey):
    try:
        url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/getAPIEncpkey'
        payload = json.dumps({
          "userId": userid,
          "userData": apikey
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        a = response.json()
        enckey = a['encKey']
        # SESSION ID
        url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/getUserSID'
        ch = checksum(f"{userid}{apikey}{enckey}")
        payload = json.dumps({
          "userId": userid,
          "userData": ch
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        sessionID = response.json()['sessionID']
        return sessionID
    except Exception as e:
        return False


def alice_order(syntax,json_data):
    apiob = aliceapi.objects.all()
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
        qty = get_quantity(x.apiuser,json_data[syntax]["symbol"])
        try:
            print("-=-=-=-=-=-=-=-=-=-=-=-=")
            clientid = x.userid
            apitoken = x.apikey
            session_id = alice_session(clientid,apitoken)
            if not session_id:
                order = str({'s': 'error', 'code': -8, 'message': 'Unauthorised Access !'})
                trade = tradebook(apiid=x.apiname,response=order,apiuser=x.apiuser,broker='alice',status='failed',quantity=qty,symbol=json_data[syntax]["symbol"])
                api_notify(x.apiuser,x.apiname,'ALICE BLUE')
                trade.save()
                continue
            # ORDER PLACEMENT
            # VARIABLE ASSIGNMENT
            symbol = json_data[syntax]["symbol"]
            segment = json_data[syntax]["segment"]
            token = json_data[syntax]["token"]
            price = json_data[syntax]["price"]
            ttype = json_data[syntax]["ttype"]
            ptype = json_data[syntax]["ptype"]
            if ptype == 'INTRADAY':
                ptype = 'MIS'
            otype = 'MKT'
            if json_data[syntax]["otype"] == 'LIMIT':
                otype = 'L'
            # END VARIABLE ASSIGNMENT
            # ------------------POSITION------------------------
            try:
                if json_data[syntax]["position"].upper() == "CLOSE":
                    url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/positionAndHoldings/positionBook'
                    payload = json.dumps({
                      "ret": "DAY"
                    })
                    headers = {
                      'Authorization': f'Bearer {clientid} {session_id}',
                      'Content-Type': 'application/json'
                    }
                    response = requests.request("POST", url, headers=headers, data=payload)
                    dic = response.json()
                    print('---------------------------------------')
                    print('Position ALICE BLUE')
                    print(dic)
                    print('---------------------------------------')
                    for i in dic:
                        if int(i["Netqty"]) != 0:
                            # PLACE ORDER
                            url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/executePlaceOrder'
                            payload = json.dumps([
                              {
                                "complexty": "regular",
                                "discqty": "0",
                                "exch": i['Exchange'],
                                "pCode": ptype,
                                "prctyp": 'MKT',
                                "price": '0',
                                "qty": i["Netqty"],
                                "ret": "DAY",
                                "symbol_id": i['Token'],
                                "trading_symbol": i['Tsym'],
                                "transtype": 'SELL',
                                "trigPrice": "",
                                "orderTag": "smart-algo"
                              }
                            ])
                            headers = {
                              'Authorization': f'Bearer {clientid} {session_id}',
                              'Content-Type': 'application/json'
                            }
                            response = requests.request("POST", url, headers=headers, data=payload)
                            nordno = response.json()
                            order_id = nordno[0]['NOrdNo']
                            try:
                                orderbook = response.json()
                                for j in orderbook:
                                    if i['Nstordno'] == order_id:
                                        order = j
                                        hbuy = j['Price']
                                        hsell = j['Price']
                                        hsymbol = j['Tsym']
                                        hquantity = j['Qty']
                                        print(price)
                                        break
                                today = timezone.now().date()
                                old = tradebook.objects.filter(apiuser=x.apiuser,datetime__date=today,symbol=hsymbol).reverse().first()
                                old.response = order
                                old.sell=float(hsell)
                                old.p_l = (float(old.sell)*float(hquantity))-(float(old.buy)*float(hquantity))
                                old.save()
                            except Exception as e:
                                status = "failed"
            except:
                pass
            # END POSITION
            url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/executePlaceOrder'
            payload = json.dumps([
              {
                "complexty": "regular",
                "discqty": "0",
                "exch": segment,
                "pCode": ptype,
                "prctyp": otype,
                "price": price,
                "qty": qty,
                "ret": "DAY",
                "symbol_id": token,
                "trading_symbol": symbol,
                "transtype": ttype,
                "trigPrice": "",
                "orderTag": "smart-algo"
              }
            ])
            headers = {
              'Authorization': f'Bearer {clientid} {session_id}',
              'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            nordno = response.json()
            order_id = nordno[0]['NOrdNo']
            print(order_id)
            status="success"
            order = str({'s': 'error', 'code': -8, 'message': 'Order Failed !'})
            url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/fetchTradeBook'
            headers = {
            'Authorization': f'Bearer {clientid} {session_id}'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            order = str({'s': 'error', 'code': -2, 'message': 'Order Failed !'})
            orderbook = response.json()
            for i in orderbook:
                if i['Nstordno'] == order_id:
                  order = i
                  hbuy = i['Price']
                  hsell = i['Price']
                  print(price)
                  break
            hsymbol = symbol
            hquantity = qty
            if json_data[syntax]['ttype'].upper() == "BUY":
                hbuy=float(hbuy)
                trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='alice',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
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
            print(e)
            status="failed"
            order = order
            trade = tradebook(apiid=x.apiid,response=order,apiuser=x.apiuser,broker='alice',status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
            trade.save()
