import requests
url = "https://test.payu.in/_payment"
payload = "key=JP***g&txnid=Dnh8wYimuCRIdv&amount=10.00&firstname=PayU User&email=test@gmail.com&phone=9876543210&productinfo=iPhone&pg=&bankcode=&surl=https://apiplayground-response.herokuapp.com/&furl=https://apiplayground-response.herokuapp.com/&hash=cb4b8bda5677dbe80f53735b1d0ec5d48164c3654627369268cf6bf266db994db39108ce2e0868c953e66c172f6b2d78836b253d3463d0cc40d9b6a93118ed56"
headers = { "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded" }
response = requests.request("POST", url, data=payload, headers=headers, params="")
print(response.text)