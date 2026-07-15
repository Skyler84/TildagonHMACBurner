from . import SecretGenerator

class LocalSecretGenerator(SecretGenerator):
    def __init__(self, master_secret):
        self.master_secret = master_secret

    def generate_combined_secret(self, mac_str):
        """
        Generate a combined secret using the master secret and device ID.
        """
        combined_secret = self.master_secret + mac_str
        hmac_key = hashlib.sha256(combined_secret.encode()).digest()
        return hmac_key.hex()