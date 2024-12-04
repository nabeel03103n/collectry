import requests
from requests.auth import HTTPBasicAuth

def query_transaction_status(merchant_id, order_id, username, password, bank_reference_id=None):

    base_url = "https://pilot.surepay.ndml.in/SurePayPayment/v1/queryPaymentStatus"  # UAT URL
    base_url_refund = "https://pilot.surepay.ndml.in/SurePayPayment/v1/refundTransaciton"  # UAT URL

    # Construct the request message
    if bank_reference_id:
        request_msg = f"{bank_reference_id}|{merchant_id}|{order_id}"
    else:
        request_msg = f"|{merchant_id}|{order_id}"

    payload = {'requestMsg': request_msg}

    try:
        # Send the POST request
        response = requests.post(
            base_url,
            data=payload,
            auth=HTTPBasicAuth(username.strip(), password.strip())
        )

        # Debugging output for troubleshooting
        print(f"Request sent to {base_url}")
        print(f"Payload: {payload}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        # Check if response is plain text
        if response.status_code == 200:
            # Return raw text response for further processing
            return {"status": "success", "response": response.text}
        else:
            # Handle unsuccessful status codes
            return {"error": f"HTTP {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": "Exception occurred", "details": str(e)}

# Example Usage
merchant_id = "UATIDEEDSG0000001536"
order_id = "109281"
username = "UATIDEEDSG0000001536"  # Replace with actual username
password = "jtuamnwsggmkknstwycz"  # Replace with actual password
bank_reference_id = None  # Provide if available

response = query_transaction_status(merchant_id, order_id, username, password, bank_reference_id)
print(response)
# print(response["status"])
