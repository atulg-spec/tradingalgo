import requests
import json
import hashlib

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
        print(response.json())
        sessionID = response.json()['sessionID']
        return sessionID
    except Exception as e:
        return False


print(alice_session('880631','pgFarfLoXT35hZDfUjODY3m5bLyh04ylKxXHM6LSSup44pChRlPxp5Phi5YBXO36sggJ5AQix04FVqKuBKeWGrLUGfINcmvLes5pnOMGTXqh9Wo4hn5TmSnMq1V9Dliz'))
















# from pya3 import *

# alice = Aliceblue(user_id='880631',api_key=api)
# print(alice.get_session_id()) # Get Session ID
# print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
# print(
#    alice.place_order(transaction_type = TransactionType.Buy,
#                     instrument = alice.get_instrument_by_symbol('NSE', 'INFY'),
#                     quantity = 1,
#                     order_type = OrderType.Market,
#                     product_type = ProductType.Delivery,
#                     price = 0.0,
#                     trigger_price = None,
#                     stop_loss = None,
#                     square_off = None,
#                     trailing_sl = None,
#                     is_amo = False,
#                     order_tag='order1')
#    )
# # Net_position = alice.get_netwise_positions()
# # print(alice.get_daywise_positions())
# # close_position = Alice_Wrapper.close_net_poition(Net_position)
# # print("Close position :",close_position)
# # print("=============================")
# # print("=============================")
# # print("=============================")
# # print("=============================")
# # dic = alice.get_daywise_positions()
# # for i in dic:
# #     print(i['Netqty'])
# #     print(i['Exchange'])
# #     print(i['Symbol'])
