import json
from smartapi import SmartConnect

clientid = "A400396"
rtoken = "eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJpYXQiOjE2OTEzOTc2ODB9.o74XRoocpF-UpHrMwnezPxHuWR6AV-tIDVAs5v4aN87eSHY_ulZKk_ZhOXyUgHrF7rIywdW3jNxwE_arR115yg"
apikey = "GdLfUVBn"
authtoken = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE0MDAzOTYiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwiaWF0IjoxNjkxMzk3NjgwLCJleHAiOjE2OTE0ODQwODB9.FPx9QQ57Nl_9lTWyQLZOyBCD12Aoh-eBV63PPXeqlDQLycLYT8LroChn8IrPd8mVn_2RVYEWgtT4Kx5xWqGzLw"

try:
    obj = SmartConnect(api_key=apikey,
                       access_token=authtoken,
                       refresh_token=rtoken)
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045",
        "transactiontype": "SELL",
        "exchange": "NSE",
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": "19500",
        "squareoff": "0",
        "stoploss": "0",
        "quantity": "1"
        }

    # orderparams = {'variety': 'NORMAL', 'tradingsymbol': 'BANKNIFTY10AUG2344700CE', 'symboltoken': '43357',
    #                'transactiontype': 'BUY', 'exchange': 'NFO', 'ordertype': 'MARKET', 'producttype': 'INTRADAY',
    #                'duration': 'DAY', 'price': '0', 'squareoff': '0', 'stoploss': '0', 'quantity': '105'}
    orderId = obj.placeOrder(orderparams)
    print("The order id is: {}".format(orderId))
except Exception as e:
    print("Order placement failed: {}".format(str(e)))
