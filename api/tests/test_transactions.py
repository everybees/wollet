from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from api.models import Transaction, User, Wallet
from api.serializers import WalletSerializer


class TransactionViewSetTes(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()

        self.admin = User.objects.create(username="admin", email="admin@email.com")
        self.admin_wallet = Wallet.objects.create(owner=self.admin, currency='NGN', balance=0.0)
        self.admin_token = Token.objects.create(user=self.admin)

        self.johnnie = User.objects.create(username="johnnie", email="johnson@email.com")
        self.johnnie_wallet = Wallet.objects.create(owner=self.johnnie, currency='NGN', balance=0.0)
        self.johnnie_token = Token.objects.create(user=self.johnnie)

        self.jane = User.objects.create(username="jane", email="jane@email.com", user_type='elite')
        self.jane_wallet = Wallet.objects.create(owner=self.jane, currency='NGN', balance=0.0)
        self.jane_token = Token.objects.create(user=self.jane)

        self.transaction = Transaction.objects.create(
            wallet=self.johnnie_wallet, amount=2000.0, is_approved=False
            )
    

    def test_noob_tries_to_approve_transaction(self):
        transaction_data = {
            "transaction_id": self.transaction.id
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.put(reverse('transactions-approve-withdrawal'), transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)