import requests
from api.models import Transaction


FIXER_URL = "http://data.fixer.io/api"
FIXER_API_KEY = "927f5c94d894bf4e8a33d2a1e7f1c53c"
url = "http://data.fixer.io/api/latest?access_key=927f5c94d894bf4e8a33d2a1e7f1c53c"


def perform_funding(amount, currnecy, wallet):
    ...


def perfrom_withdrawal(amount, currency, wallet_id):
    ...


def convert_to_main_currency(amount, currency, wallet, transaction_type):
    try:
        response = requests.post(f"{FIXER_URL}/latest?access_key={FIXER_API_KEY}")
        data = response.json().get('rates')
        euro_to_currency = data[currency]
        euro_to_wallet_currency = data[wallet.currency]
        amount_conversion = round((euro_to_wallet_currency / euro_to_currency) * amount, 2)
        transaction = Transaction.objects.create(wallet=wallet, amount=amount_conversion, transaction_type=transaction_type)
        return transaction
    except Exception as e:
        print(str(e))