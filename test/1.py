import zlib

messageType = ""
merchantId = "UATIDEEDSG0000001536"
serviceId = "IDEED03"
orderId = ""
customerId = ""
transactionAmount = 250
currencyCode = "INR"
requestDateTime = ""
successUrl = "https://www.google.com"
failUrl = "https://www.instagram.com"

message = f"{messageType}|{merchantId}|{serviceId}|{orderId}|{customerId}|{transactionAmount}|{currencyCode}|{requestDateTime}|{successUrl}|{failUrl}"

secret_key = "2cf0f5d878e83150c5d36b0b07b737db8636e259046ac4b05baa7deeb8712eed"
msg = message + "|" + secret_key
bytes_data = msg.encode('utf-8')
checksum_value = zlib.crc32(bytes_data)
print("Checksum: ", checksum_value)

def generate_checksum(message, secret_key):
    msg = message + "|" + secret_key
    bytes_data = msg.encode('utf-8')
    checksum_value = zlib.crc32(bytes_data)
    return checksum_value