from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from api.models import User, Wallet


class UserViewSetTes(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()

        self.johnnie = User.objects.create(username="johnnie", email="john@email.com")
        self.johnnie_token = Token.objects.create(user=self.johnnie)

    def test_create_user(self):
        data = {
            "username": "john",
            "email": "john@email.com",
            "currency": "USD",
            "first_name": "John",
            "last_name": "Doe",
            "password": "somepassword"
        }
        bad_data = {
            "uswrname": "janet",
            "emali": 1234,
            "currency": 123,
            "password": "mypassword"
        }
        bad_data_1 = {
            "username": "janet",
            "email": 1234,
            "currency": 123,
            "password": "mypassword"
        }
        elite_user_data = {
            "username": "johnson",
            "email": "johnson@email.com",
            "currency": "EUR",
            "user_type": "elite",
            "first_name": "Johnson",
            "last_name": "Doe",
            "password": "somepassword"
        }


        # test creation with correct data
        response = self.client.post(reverse('users-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'john')
        user = User.objects.get(username='john')
        wallet_exists = Wallet.objects.filter(owner=user).exists()
        self.assertEqual(wallet_exists, True)

        # test creation with bad data 0
        response = self.client.post(reverse('users-list'), data=bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test creation with data that already exists
        response = self.client.post(reverse('users-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test creation with bad data 1 - bad email value
        response = self.client.post(reverse('users-list'), data=bad_data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test creation with elite user data
        response = self.client.post(reverse('users-list'), data=elite_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'johnson')
        self.assertEqual(response.data['user_type'], 'elite')
        user = User.objects.get(username='johnson')
        wallet_exists = Wallet.objects.filter(owner=user)
        self.assertEqual(wallet_exists.exists(), True)
        self.assertEqual(wallet_exists[0].currency, 'EUR')

    def test_get_users(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.johnnie_token.key)
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data) > 0, True)


    def test_get_user(self):
        ...

    def test_update_user_type(self):
        ...

    def test_change_currency(self):
        ...
