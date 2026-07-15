import re

CHECK_MAC_STR = re.compile(r"^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$")

def generate_hmac_key(master_secret, mac_str):
    """
    Generate a combined secret using the master secret and device ID.
    """
    combined_secret = master_secret + mac_str
    hmac_key = hashlib.sha256(combined_secret.encode()).digest()
    # Ensure both inputs are bytes
    if isinstance(master_secret, str):
        master_secret = master_secret.encode('utf-8')
    if isinstance(device_id, str):
        device_id = device_id.encode('utf-8')

    if not CHECK_MAC_STR.match(mac_str):
        raise ValueError("Invalid MAC address format. Expected format: XX-XX-XX-XX-XX-XX")

    # Create a new HMAC object using the master secret as the key
    hmac_obj = hmac.new(master_secret, device_id, hashlib.sha256)

    # Return the hexadecimal digest of the HMAC
    return hmac_obj.hexdigest()