import json
import os
from base64 import b64encode

import requests


class JamfInventory:
    def get_inventory(self):
        base_url = os.environ["JAMF_URL"]
        username = os.environ["JAMF_USER"]
        password = os.environ["JAMF_PASS"]

        auth_token = self._get_auth_token(base_url, username, password)
        inventory = self._get_inventory_details(base_url, auth_token)
        return inventory  # ["totalCount"]

    def _get_auth_token(self, base_url, username, password):
        auth_url = base_url + "/uapi/auth/tokens"
        credential_string = self._get_credential_string(username, password)

        response = requests.post(
            auth_url, headers={"Authorization": f"Basic {credential_string}"}
        )
        response_dir = json.loads(response.text)
        token = response_dir["token"]
        return token

    def _get_credential_string(self, username, password):
        text_string = f"{username}:{password}"
        encoded_string = b64encode(text_string.encode("utf-8"))
        return encoded_string.decode("utf-8")

    def _get_inventory_details(self, base_url, auth_token):
        inv_url = base_url + "/uapi/v1/computers-inventory"
        response = requests.get(
            inv_url, headers={"Authorization": f"Bearer {auth_token}"}
        )
        return json.loads(response.text)


if __name__ == "__main__":
    inv = JamfInventory().get_inventory()
    print(inv)
