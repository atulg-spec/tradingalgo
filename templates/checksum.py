import hashlib
import json
import paytmchecksum


# # Your data
# data = {
#     "gateway_type":"Robotics",
#     "upiuid": "paytmqr28100505010110sggy9gsszk@paytm",
#     "token":'82e16b-54fd81-687682-f76ade-14d412',
#     "orderId":"7d161217pf",
#     "txnAmount":10.0,
#     "txnNote":"hello",
#     "cust_Mobile":'9193660086',
#     "cust_Email":'admGGin@demo.com',
#     "callback_url":"http://127.0.0.1:8000",
# }
# # Convert the data to a JSON string
# data_json = json.dumps(data, separators=(',', ':'), sort_keys=True)


# key = "4xGhRSabz1"
# checksum = paytmchecksum.PaytmChecksum.generateSignature(data,key)

# # checksum = hashlib.sha256(data_json.encode()).hexdigest()

# print("Checksum:", checksum)



import requests
url = "https://apiqr.upibuz.in/order/process"
params = {
    "gateway_type":"Robotics",
    "upiuid": "paytmqr28100505010110sggy9gsszk@paytm",
    "token":'82e16b-54fd81-687682-f76ade-14d412',
    "orderId":"SPINFOTECH1694076455",
    "txnAmount":'1',
    "txnNote":"Test Payment",
    "cust_Mobile":'0930248930',
    "cust_Email":'atul@gmail.com',
    "callback_url":"/payment/txn-result/",
    "checksum":'z6svxFUbkYqDZbqy1zB4RyXtUWkgiUZMVA1JBGU2IMO7McsrmIli9Q7jK0bGhF5PYF5oBA7bqofsWcOuPU+sslRZZoapL0ugmNcA3Ebul2g='
}
response = requests.post(url, data=params)
print(response.url)
print(response.text)
