import requests
import json


class Payment:
    def __init__(self):
        with open("tokens.json", "r") as f:
            token = json.load(f)['cryptobot']
        self.token = token
        self.headers = {
            "Crypto-Pay-API-Token": self.token
        }

    def get_invoices(self):
        response = requests.get(f"https://testnet-pay.crypt.bot/api/getInvoices?asset=USDT", headers=self.headers)

    def create_invoice(self, amount):
        response = requests.get(f"https://testnet-pay.crypt.bot/api/createInvoice?asset=USDT&amount={amount}", headers=self.headers)

    def get_me(self):
        response = requests.get(f"https://testnet-pay.crypt.bot/api/getMe", headers=self.headers)

    def get_balance(self):
        response = requests.get(f"https://testnet-pay.crypt.bot/api/getBalance", headers=self.headers)