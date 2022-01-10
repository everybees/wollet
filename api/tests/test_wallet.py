from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import Transaction, User, Wallet


class WalletViewSetTes(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()

        self.admin = User.objects.create(username="admin", email="admin@email.com")
        self.admin_wallet = Wallet.objects.create(owner=self.admin, currency='NGN', balance=0.0)
        self.admin_token = Token.objects.create(user=self.admin)

        self.johnnie = User.objects.create(username="johnnie", email="johnson@email.com")
        self.johnnie_wallet = Wallet.objects.create(owner=self.johnnie, currency='NGN', balance=1000000.0)
        self.johnnie_token = Token.objects.create(user=self.johnnie)

        self.jane = User.objects.create(username="jane", email="jane@email.com", user_type='elite')
        self.jane_wallet = Wallet.objects.create(owner=self.jane, currency='NGN', balance=0.0)
        self.jane_token = Token.objects.create(user=self.jane)

    def test_noob_can_only_have_one_wallet(self):
        wallet_data = {
            "currency": "USD",
            "amount": 1000
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.post(reverse('wallet-create-wallet'), data=wallet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_noob_wallet_funding(self):
        funding_data = {
            "currency": "USD",
            "amount": 200,
            "wallet_id": self.johnnie_wallet.id
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.put(reverse('wallet-fund-wallet'), data=funding_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction = Transaction.objects.get(wallet_id=self.johnnie_wallet.id)
        self.assertEqual(transaction.amount != funding_data['amount'], True)

    def test_noob_wallet_withdrawal(self):
        withdraw_data = {
            "currency": "USD",
            "amount": 20,
            "wallet_id": self.johnnie_wallet.id
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.put(reverse('wallet-withdraw'), data=withdraw_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction = Transaction.objects.get(wallet_id=self.johnnie_wallet.id)
        self.assertEqual(transaction.amount != withdraw_data['amount'], True)
    
    def test_noob_change_wallet_currency(self):
        withdraw_data = {
            "currency": "USD",
            "wallet_id": self.johnnie_wallet.id
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.put(reverse('wallet-change-wallet-currency'), data=withdraw_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_elite_create_wallet(self):
        wallet_data = {
            "currency": "USD",
            "amount": 1000
        }
        wallet_data_1 = {
            "currency": "EUR",
            "amount": 100
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.jane_token.key)
        response = self.client.post(reverse('wallet-create-wallet'), data=wallet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('wallet-create-wallet'), data=wallet_data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_elite_wallet_funding(self):
        funding_data = {
            "currency": "USD",
            "amount": 200,
            "wallet_id": self.jane_wallet.id
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.jane_token.key)
        response = self.client.put(reverse('wallet-fund-wallet'), data=funding_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction = Transaction.objects.get(wallet_id=self.jane_wallet.id)
        self.assertEqual(transaction.amount == funding_data['amount'], True)

    def test_fund_wallet(self):
        funding_data = {
            "amount": 1000,
            "currency": "USD",
            "wallet_id": self.johnnie_wallet.id
        }

        elite_funding_data = {
            "amount": 1000,
            "currency": "USD",
            "wallet_id": self.jane_wallet.id
        }

        # with noob user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.put(reverse('wallet-fund-wallet'), data=funding_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = self.johnnie
        transaction = Transaction.objects.filter(wallet__owner=user)
        self.assertEqual(transaction.exists(), True)

        # with elite user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.jane_token.key)
        response = self.client.put(reverse('wallet-fund-wallet'), data=elite_funding_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = self.jane
        transaction = Transaction.objects.filter(wallet=self.jane_wallet)
        self.assertEqual(transaction.exists(), True)

    def test_withdraw_from_wallet(self):
        funding_data = {
            "amount": 1000,
            "currency": "USD",
            "wallet_id": self.johnnie_wallet.id
        }

        # with noob user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.put(reverse('wallet-withdraw'), data=funding_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_other_wallets(self):
        wallet_data = {
            'currency': 'USD',
        }

        # test creation of wallet with noob user 
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.post(reverse('wallet-create-wallet'), data=wallet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test creation of wallet with admin user 
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response = self.client.post(reverse('wallet-create-wallet'), data=wallet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test creation of wallet with elite user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.jane_token.key)
        response = self.client.post(reverse('wallet-create-wallet'), data=wallet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='jane')
        wallet = Wallet.objects.filter(owner=user, currency='USD')
        self.assertEqual(wallet.exists(), True)

    def test_approve_fund_request(self):
        ...
