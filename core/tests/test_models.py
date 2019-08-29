import pendulum
from django.test import TestCase

from core.api.exceptions import InsufficientBalanceException, DailyLimitReachedException
from core.models import Account, Transaction, TYPE_DEPOSIT


class AccountTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number="123", first_name="James", last_name="Brown", balance=30.00)

    def test_get_balance(self):
        result = self.account.get_balance()
        self.assertEqual(result, 30.00)

    def test_deposit(self):
        initial_transaction_count = Transaction.objects.count()
        self.account.deposit(20.00)
        self.assertEqual(self.account.balance, 50.00)

        updated_transaction_count = Transaction.objects.count()
        self.assertEqual(updated_transaction_count, initial_transaction_count + 1)

    def test_withdraw_greater_than_balance(self):
        with self.assertRaises(InsufficientBalanceException):
            self.account.withdraw(70.00)

    def test_withdraw_violate_daily_transaction_limit(self):
        account = Account.objects.create(account_number="123", first_name="James", last_name="Brown", balance=290000.00)
        account.withdraw(90000.00)

        self.assertEqual(Transaction.objects.count(), 1)
        with self.assertRaises(DailyLimitReachedException):
            account.withdraw(20000.00)

    def test_withdraw_limit_only_applies_daily(self):
        account = Account.objects.create(account_number="123", first_name="James", last_name="Brown", balance=290000.00)
        Transaction.objects.create(
            account=account,
            date=pendulum.now().subtract(days=1),
            amount=100000.00,
            type=TYPE_DEPOSIT
        )

        self.assertIsNone(account.withdraw(90000.00))  # If the function returns None then we know everything went well
