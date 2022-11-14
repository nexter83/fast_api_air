import requests
from datetime import datetime
import unittest

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}
url = 'http://localhost:8000/api/accounts'


class TestAccounts(unittest.TestCase):
    def test_create_account(self):
        json_data = {
            'login': 'nexter83',
            'first_name': 'Oleg',
            'last_name': 'Basmanov',
            'update_ts': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        }
        response = requests.post(url, headers=headers, json=json_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual("ok", response.json()["status"])

    def test_get_accounts(self):
        response = requests.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual("ok", response.json()["status"])

    def test_get_account(self):
        response = requests.get(url + "/257350")
        self.assertEqual(200, response.status_code)
        self.assertEqual("ok", response.json()["status"])

    def test_update_account(self):
        json_data = {
            'login': 'nexter83',
            'first_name': 'Oleg',
            'last_name': 'Basmanov',
            'update_ts': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        }
        response = requests.put(url + "/257350", headers=headers, json=json_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("ok", response.json()["status"])

    def test_delete_account(self):
        response = requests.delete(url + "/257350")
        self.assertEqual(204, response.status_code)


if __name__ == "__main__":
    unittest.main()