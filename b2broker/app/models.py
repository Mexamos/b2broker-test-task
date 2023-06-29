from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=18, decimal_places=2)


class Transaction(models.Model):
    wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    txid = models.CharField(max_length=200, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
