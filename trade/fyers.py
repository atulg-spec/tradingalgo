from fyers_api import fyersModel

clientid = "KT4BY2P2PM-100"
accesstoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTY0OTMwMzIsImV4cCI6MTY5NjU1MjI1MiwibmJmIjoxNjk2NDkzMDMyLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbEhtM29FcGpxOENUT19EV0JmbzB2UkxpRnFHckhnQkdLMF9hMVBGNDFiRHFyZk5paG5fOGNUMjItQ0hVVE9ITlBwYmxvQWthVU9JaGQ2N01vVjNvTGMtOU1xLUkzZ0Y1VWNicVBFbzlPVV9HVnBHOD0iLCJkaXNwbGF5X25hbWUiOiJBU0lGIEFMSSIsIm9tcyI6IksxIiwiaHNtX2tleSI6bnVsbCwiZnlfaWQiOiJYQTYxMDg1IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.2evi1nRNbwU3LBP1D8NXxCe7iNuSAcKu3o_dKnDeTFE"
fyers = fyersModel.FyersModel(client_id=clientid, token=accesstoken)
print(fyers)
data = {
                "symbol":f"NSE:SBIN-EQ",
                "qty":1,
                "type":'2',
                "side":1,
                "productType":'INTRADAY',
                "limitPrice":0,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":"False",
            }
print(data)
order = fyers.place_order(data)
print("=-=-=-=-=-=-=-=-=-=")
print(order)
# data={
#      "symbol":"NSE:SBIN-EQ",
#      "qty":1,
#      "type":2,
#      "side":1,
#      "productType":"INTRADAY",
#      "limitPrice":0,
#      "stopPrice":0,
#      "validity":"DAY",
#      "disclosedQty":0,
#      "offlineOrder":"False",
#  }
# order = fyers.place_order(data)
# print(order)
# a = {'s': 'ok', 'code': 1101, 'message': 'Order Submitted Successfully. Your Order Ref. No. 23080400366855', 'id': '23080400366855'}
# print(a["id"])
# data = {"id":a["id"]}
# print(fyers.orderbook())
# print("===========================")
# print("===========================")
# order = fyers.get_orders(data=data)
# print(order)
# print("===========================")
# print(order["data"][0]["tradedPrice"])
# print(order["data"][0]["symbol"])