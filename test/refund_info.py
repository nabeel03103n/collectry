import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import zlib

def generate_checksum(message, secret_key):
    msg = f"{message}|{secret_key}"
    bytes_data = msg.encode('utf-8')
    return zlib.crc32(bytes_data) & 0xffffffff  # Ensure checksum is unsigned


def initiate_refund(merchant_id, order_id, refund_req_id, bank_transaction_no,
                    service_id, surepay_txn_id, transaction_amount, refund_amount, username, password):
    """
    Initiates a refund request with SurePay.
    """
    base_url = "https://pilot.surepay.ndml.in/SurePayPayment/v1/refundTransaction"  # UAT URL
    secret_key = "2cf0f5d878e83150c5d36b0b07b737db8636e259046ac4b05baa7deeb8712eed"  # Replace with your actual secret key
    requestDateTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Construct the request message for checksum generation
    request_msg = f"{merchant_id}|{order_id}|{refund_req_id}|{bank_transaction_no}|{service_id}|{surepay_txn_id}|{requestDateTime}|{transaction_amount}|{refund_amount}"
    checksum = generate_checksum(request_msg, secret_key)

    # Construct the payload for the refund request
    payload = {
        "refundApiRequest": [
            {
                "surePayMerchantId": merchant_id,
                "orderId": order_id,
                "refundReqId": refund_req_id,
                "bankTransactionNo": bank_transaction_no,
                "serviceId": service_id,
                "surePayTxnId": surepay_txn_id,
                "requestDateTime": requestDateTime,
                "transactionAmount": transaction_amount,
                "refAmount": refund_amount,
                "additionalField1": "",
                "additionalField2": "",
                "additionalField3": "",
                "additionalField4": "",
                "additionalField5": "",
                "checkSum": str(checksum)
            }
        ]
    }

    try:
        # Send the POST request to initiate a refund
        response = requests.post(
            base_url,
            json=payload,
            auth=HTTPBasicAuth(username.strip(), password.strip())
        )

        # Debugging output for troubleshooting
        print(f"Request sent to {base_url}")
        print(f"Payload: {payload}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            return {"status": "success", "response": response.json()}
        else:
            return {"error": f"HTTP {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": "Exception occurred", "details": str(e)}

initiate_refund("UATIDEEDSG0000001536","109281","1","","IDEED03","7555706067","250.00","250.00","UATIDEEDSG0000001536","jtuamnwsggmkknstwycz")