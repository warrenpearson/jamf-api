import json
import os
from base64 import b64encode

import requests


class JamfInventory:
    """A Jamf API client for returning inventory data

    Running the script requires you to have the three environment variables set
    which are referenced in the __init__ method. These are the URL, username and
    password you would use to login to your Jamf Pro instance via a browser.

    When run from the command line, the script returns JSON for easy parsing by jq.
    """

    def __init__(self, filter_type=None):
        self._base_url = os.environ["JAMF_URL"]
        self._username = os.environ["JAMF_USER"]
        self._password = os.environ["JAMF_PASS"]
        if filter:
            self._filter_type = filter_type

    def get_inventory(self):
        auth_token = self._get_auth_token()
        inventory = self._get_inventory_details(auth_token)
        return self.report_details(inventory)

    def _get_auth_token(self):
        """Auth tokens can be reused for up to 30 minutes
        but we currently generate a new one on each request
        """

        auth_url = self._base_url + "/uapi/auth/tokens"
        credential_string = self._get_credential_string()

        response = requests.post(
            auth_url, headers={"Authorization": f"Basic {credential_string}"}
        )
        response_dir = json.loads(response.text)
        token = response_dir["token"]
        return token

    def _get_credential_string(self):
        text_string = f"{self._username}:{self._password}"
        encoded_string = b64encode(text_string.encode("utf-8"))
        return encoded_string.decode("utf-8")

    def _get_inventory_details(self, auth_token: str):
        inv_url = self._base_url + "/uapi/v1/computers-inventory?"

        sections = [
            "GENERAL",
            "DISK_ENCRYPTION",
            "HARDWARE",
            "LOCAL_USER_ACCOUNTS",
            "OPERATING_SYSTEM",
            "SOFTWARE_UPDATES",
        ]
        query_string = ""
        for section in sections:
            query_string += f"section={section}&"
        inv_url += query_string

        response = requests.get(
            inv_url, headers={"Authorization": f"Bearer {auth_token}"}
        )

        return json.loads(response.text)

    def report_details(self, inventory: dict):
        if self._filter_type:
            print("TODO: filtering not enabled yet")

        return json.dumps(inventory)


if __name__ == "__main__":
    inv = JamfInventory().get_inventory()
    print(inv)
