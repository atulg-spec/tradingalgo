import json
from smartapi import SmartConnect
clientid = "A400396"
rtoken = "eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJpYXQiOjE2OTE2Mzk3NTV9.9eFrO6ae7nEawHPkH0SWC5nketMyW5mgODcgsBboa8Fx7dgQCrPvH8hnbNANDNH-AG5pAa-IDQwIi3lm8GgkwA"
apikey = "GdLfUVBn"
authtoken = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE0MDAzOTYiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwiaWF0IjoxNjkxNjM5NzU1LCJleHAiOjE2OTE3MjYxNTV9.zECnyRskZayxmymadC8traRHwwUBW5jz68QH8VUS3wuSbprBRJlOTCZ4VJ5msQ8qLvZaoChFG0wxcDhsYYZ38Q"
try:
    obj=SmartConnect(api_key=apikey,
            access_token = authtoken,
            refresh_token = rtoken)
    print(obj.access_token)
    # orderparams = {'variety': 'NORMAL', 'tradingsymbol': 'BANKNIFTY10AUG2344700CE', 'symboltoken': '43357', 'transactiontype': 'BUY', 'exchange': 'NFO', 'ordertype': 'MARKET', 'producttype': 'INTRADAY', 'duration': 'DAY', 'price': '0', 'squareoff': '0', 'stoploss': '0', 'quantity': '105'}
    # orderId=obj.placeOrder(orderparams)
    # print("The order id is: {}".format(orderId))
    print("-------------------------------------")
    dic = obj.position()
    print("printing dic")
    print(dic)
    for i in dic["data"]:
        print("=================")
        print(i)
        print("=================")
        # print(i["exchange"])
        # print(i["sellavgprice"])
        # print(i["buyqty"])
        # if i["sellavgprice"] == '0.0':
        #     pass
except Exception as e:
    print("Order placement failed: {}".format(e.message))
# print("-----------------------")

# try:
#     obj=SmartConnect(api_key=apikey,
#              access_token = authtoken,
#              refresh_token = rtoken)
#     status=["FORALL"] #should be a list
#     page=1
#     count=10
#     lists=obj.gttLists(status,page,count)
#     print(lists)
# except Exception as e:
#     print("GTT Rule List failed: {}".format(e.message))