from dhanhq import dhanhq

clientid = "1100617939"
accesstoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzAxMjc2MzkzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDYxNzkzOSJ9.oFDmW_GKxuD_kxctiur4FJEbBWRP0qVgyxTE7w40iW4B2uO5H82RPlY6oVV-6lSeFgewOckIOPJhMgj265GKOA"
dhan = dhanhq(clientid,accesstoken)
# order = dhan.place_order(
#     tag='',
#     transaction_type=dhan.BUY,
#     exchange_segment=NSE_EQ,
#     product_type=dhan.INTRA,
#     order_type=dhan.MARKET,
#     validity='DAY',
#     security_id='1333',
#     quantity=2,
#     disclosed_quantity=0,
#     price=0,
#     trigger_price=0,
#     after_market_order=False,
#     amo_time='OPEN',
#     bo_profit_value=0,
#     bo_stop_loss_Value=0,
#     drv_expiry_date=None,
#     drv_options_type=None,
#     drv_strike_price=None    
# )
# print(order)
# print(dhan.NSE)
# a = "hello"
# print(type(a))

print("=============")
dic = dhan.get_positions()
print(dic)
if dic['status'] == 'failure':
    print("down")
print("============")
for i in dic["data"]:
    print(i["positionType"])
    print(i["netQty"])
    print(i["exchangeSegment"])