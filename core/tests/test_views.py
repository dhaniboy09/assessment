from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Account


class BankAPITest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(account_number="123", first_name="James", last_name="Brown",
                                               balance=30.00)
        self.account2 = Account.objects.create(account_number="123", first_name="James", last_name="Brown",
                                               balance=50.00)
        self.client = APIClient()

    def test_get_account_balance(self):
        response = self.client.get(reverse('account_balance', kwargs={'pk': self.account1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data.get('balance')), 30.00)

    def test_deposit(self):
        response = self.client.put(reverse('deposit', kwargs={'pk': self.account1.pk}), {'amount': 50.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Success")

    def test_withdraw(self):
        response = self.client.put(reverse('deposit', kwargs={'pk': self.account1.pk}), {'amount': 10.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Success")
