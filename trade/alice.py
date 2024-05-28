import requests
import json
url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/executePlaceOrder'
api = 'Bearer 880631 pgFarfLoXT35hZDfUjODY3m5bLyh04ylKxXHM6LSSup44pChRlPxp5Phi5YBXO36sggJ5AQix04FVqKuBKeWGrLUGfINcmvLes5pnOMGTXqh9Wo4hn5TmSnMq1V9Dliz'

payload = json.dumps([
  {
    "complexty": "regular",
    "discqty": "0",
    "exch": "NSE",
    "pCode": "MIS",
    "prctyp": "L",
    "price": "3550.00",
    "qty": 1,
    "ret": "DAY",
    "symbol_id": "212",
    "trading_symbol": "ASHOKLEY-EQ",
    "transtype": "BUY",
    "trigPrice": "",
    "orderTag": "order1"
  }
])
headers = {
  'Authorization': api,
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)


















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
