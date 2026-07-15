from . import SecretGenerator
import requests

class RemoteSecretGenerator(SecretGenerator):
    def __init__(self, server_url, api_key):
        self.server_url = server_url
        self.api_key = api_key

    def generate_combined_secret(self, mac_str):
        """
        Generate a combined secret using the remote server.
        """
        response = requests.post(
            f"{self.server_url}/api/generate_badge_secret/",
            json={"mac": mac_str},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return response.json()["hmac_key"]