import random
from decimal import Decimal

from django.conf import settings
from django.db import models


def generate_account_number():
    """Create a unique 10-digit account number."""
    while True:
        number = str(random.randint(10**9, 10**10 - 1))
        if not Account.objects.filter(account_number=number).exists():
            return number


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account'
    )
    account_number = models.CharField(
        max_length=10, unique=True, default=generate_account_number, editable=False
    )
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    credit_score = models.PositiveIntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account_number} - {self.user.cnic}'


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    to_account = models.ForeignKey(
        Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='incoming'
    )
    balance_after = models.DecimalField(max_digits=14, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.type} {self.amount} ({self.account.account_number})'
