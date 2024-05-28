import requests
import hashlib

# Define the base URL for the Paytm Business Robotics API
base_url = "https://apiqr.upibuz.in"

# Define your API credentials
api_token = "82e16b-54fd81-687682-f76ade-14d412"
your_upi_id = "paytmqr28100505010110sggy9gsszk@paytm"
your_unique_id = "ORDS5845584"

# Function to calculate checksum
def calculate_checksum(data, api_secret):
    # Concatenate all key-value pairs in the data and sort them
    concatenated_data = ''.join([f'{key}{value}' for key, value in sorted(data.items())])

    # Append your API secret
    concatenated_data += api_secret

    # Calculate the checksum using SHA-256
    checksum = hashlib.sha256(concatenated_data.encode()).hexdigest()
    return checksum

# Function to make a POST request to the API
def make_post_request(endpoint, data):
    url = f"{base_url}{endpoint}"
    response = requests.post(url, data=data)
    return response.text

# Gateway Check Out Page - REQUEST FORM DATA POST
checkout_data = {
    "upiuid": your_upi_id,
    "token": api_token,
    "orderId": your_unique_id,
    "txnAmount": "100",
    "txnNote": "Test",
    "callback_url": "http://localhost/txnResult",
}

# Calculate the checksum for the request
checkout_data["checksum"] = calculate_checksum(checkout_data, api_token)

checkout_response = make_post_request("/order/process", checkout_data)

# Print the response from the checkout request
print("Gateway Check Out Page - REQUEST FORM DATA POST Response:")
print(checkout_response)
