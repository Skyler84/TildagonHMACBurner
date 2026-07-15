import re
import hashlib

CHECK_MAC_STR = re.compile(r"^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$")

def generate_hmac_key(master_secret, mac_str: str) -> bytes:
    """
    Generate a combined secret using the master secret and MAC address.
    """

    if not CHECK_MAC_STR.match(mac_str):
        raise ValueError("Invalid MAC address format. Expected format: XX-XX-XX-XX-XX-XX")

    combined_secret = master_secret + mac_str
    hmac_key = hashlib.sha256(combined_secret.encode()).digest()

    return hmac_key