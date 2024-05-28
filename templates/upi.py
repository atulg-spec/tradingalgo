# import requests
# import json
# url = "https://upibuz.in/payment/create_order.php"
# params = {
#     "user_token": "83cc9cbe167cd77dc5328f87dbb7868f",
#     "amount":1,
#     "order_id":"smaata=goi",
#     "redirect_url":"https://smart-algo.in"
# }
# response = requests.get(url, params=params)
# print(response.url)
# if response.status_code == 200:
#     data = response.json()
#     print(data)
#     if data["status"]=="SUCCESS":
#         print(data["payment_link"])
#     else:
#         print("ohh")
# else:
#     print("Error: %s" % response.status_code)
# # response = requests.get("https://upibuz.in/payment/check_order.php?user_token=2771ccb32e6f4f72fa9b303e5c9de4e9&gateway_txn=64e3221be1767")
# # if response.content.decode('utf-8') == 'SUCCESS':
# #     print("Hello")
# # elif response.content.decode('utf-8') == 'PENDING':
# #     print("Error")
# # else:
# #     print("Unknown response")


api_token = "82e16b-54fd81-687682-f76ade-14d412"
your_upi_id = "paytmqr28100505010110sggy9gsszk@paytm"
your_unique_id = "OR=90S5845584"
import requests
import json
url = "https://apiqr.upibuz.in/order/process"
base_url = "https://apiqr.upibuz.in"
def make_post_request(endpoint, data):
    url = f"{base_url}{endpoint}"
    print("=============")
    print(url)
    print("=============")
    response = requests.post(url, data=data)
    return response.content
checkout_data = {
    "gateway_type":"Robotics",
    "upiuid": "paytmqr28100505010110sggy9gsszk@paytm",
    "token":'82e16b-54fd81-687682-f76ade-14d412',
    "orderId":"7d161217pf",
    "txnAmount":'10.0',
    "txnNote":"hello",
    "cust_Mobile":'9193660086',
    "cust_Email":'admGGin@demo.com',
    "callback_url":"http://127.0.0.1:8000",
    "checksum": "7UvRcIDFx2kR6h6F51FQUhkXv5M/hVTeg+Zpt6k2/kDVBPBMrZ2HJwdx3jLgxcJkUKiN4OgzOt226YBxUYWw4P7jnzIvIJMo4jZWQ1ohrZr1Brb/uMxV/Sn0ScYKQJLOLkNe4YvMUw9KOyVj77CnHSOAemKklTz7mcW72+dwXAbjJPQ/UzMcnYxKYEgXNCqck+Otq+r65468/gLIlgurtfIjYz6jwzRZBDh37edUi+U="
}
checkout_response = make_post_request("/order/process", checkout_data)

# Print the response from the checkout request
print("Gateway Check Out Page - REQUEST FORM DATA POST Response:")
print(checkout_response)

# if response.status_code == 200:
#     data = response.json()
#     print(data)
#     if data["status"]=="SUCCESS":
#         print(data["payment_link"])
#     else:
#         print("ohh")
# else:
#     print("Error: %s" % response.status_code)