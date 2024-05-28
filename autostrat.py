import requests

url = "https://smart-algo.in/automatedstratergy"

# Sending a GET request
response = requests.get(url)

# Checking if the request was successful (status code 200)
if response.status_code == 200:
    # Printing the response content
    print(response.text)
else:
    # If the request was unsuccessful, print the status code
    print("Failed to retrieve data, status code:", response.status_code)
