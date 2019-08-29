from datetime import datetime

from django.db import models
import pendulum
from django.db.models import Sum

from core.api.exceptions import InsufficientBalanceException, DailyLimitReachedException

WITHDRAWAL_LIMIT_PERIOD = 1
WITHDRAWAL_LIMIT_AMOUNT = 100000
TYPE_WITHDRAWAL = 'Withdrawal'
TYPE_DEPOSIT = 'Deposit'


class Account(models.Model):
    account_number = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=100)
    latest_withdrawal = models.DateTimeField(auto_now=True)

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance = float(self.balance) + amount
        self.save()
        Transaction.objects.create(
            account=self,
            date=datetime.now(),
            amount=amount,
            type=TYPE_DEPOSIT
        )

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalanceException("Insufficent Balance")

        if amount > WITHDRAWAL_LIMIT_AMOUNT:
            raise DailyLimitReachedException("Withdrawal limit is 100,000 per day")

        now = pendulum.now()
        daily_transaction_total = Transaction.objects.filter(account_id=self.id, date__day=now.day,
                                                             type=TYPE_WITHDRAWAL).aggregate(Sum("amount"))

        if daily_transaction_total.get('amount__sum') and \
                (float(daily_transaction_total['amount__sum']) + amount) > WITHDRAWAL_LIMIT_AMOUNT:
            raise DailyLimitReachedException("Withdrawal limit is 100,000 per day")

        self.balance = float(self.balance) - amount
        self.save()
        Transaction.objects.create(
            account=self,
            date=datetime.now(),
            amount=amount,
            type=TYPE_WITHDRAWAL
        )


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=100)
    type = models.CharField(max_length=100)
