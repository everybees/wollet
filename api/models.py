from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


USER_TYPE = (
    ('noob', 'Noob'),
    ('elite', 'Elite'),
    ('admin', "Admin")
)


class User(AbstractUser):
    user_type = models.CharField(max_length=6, blank=False, choices=USER_TYPE, default='noob')

    def __str__(self) -> str:
        return self.username


class Wallet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    main_wallet = models.BooleanField(default=False)
    currency = models.CharField(max_length=5)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.owner.username} {self.currency} account"


TRANSACTION_TYPE = (
    ('funding', 'Funding'),
    ('withdrawal', 'Withdrawal')
)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    transaction_type = models.CharField(max_length=12, choices=TRANSACTION_TYPE, default='funding')
    is_approved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Transaction for {self.wallet.owner.username} {self.wallet.currency}"
