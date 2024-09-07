import zlib

def generate_checksum(data, secret_key):
    msg = data + "|" + secret_key
    bytes_data = msg.encode('utf-8')
    checksum_value = zlib.crc32(bytes_data)
    return checksum_value
