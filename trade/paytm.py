import requests
import json
url = "pytm.upibuz.in/order/process"
params = {
    "user_token": "83cc9cbe167cd77dc5328f87dbb7868f",
    "amount":1,
    "order_id":"smaata=goi",
    "redirect_url":"https://smart-algo.in"
}
response = requests.get(url, params=params)
print(response.url)
# if response.status_code == 200:
#     data = response.json()
#     print(data)
#     if data["status"]=="SUCCESS":
#         print(data["payment_link"])
#     else:
#         print("ohh")
# else:
#     print("Error: %s" % response.status_code)