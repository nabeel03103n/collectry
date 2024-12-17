import requests
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Encryption Key - Ensure it is 16 bytes for AES-128
ENCRYPTION_KEY = "E-m!tr@2016".ljust(16, '0').encode('utf-8')
IV = ENCRYPTION_KEY[:16]  # IV for AES

def encrypt_aes(data):
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(IV))
    encryptor = cipher.encryptor()
    # Pad the data to 16 bytes
    padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)
    encrypted = encryptor.update(padded_data.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(encrypted).decode('utf-8')

# Parameters
request_data = {
    "MERCHANTCODE": "RISLTEST",
    "SSOID": "testKioskSSOID",
}

# Encrypt the data
data_string = str(request_data).replace("'", '"')  # JSON-like format
encrypted_data = encrypt_aes(data_string)

# UAT URL
url = "http://emitrauat.rajasthan.gov.in/webServicesRepositoryUat/getKioskDetailsJSON"

# Send the request
response = requests.post(url, data={"encData": encrypted_data})

# Output the response
print("Response:", response.text)
