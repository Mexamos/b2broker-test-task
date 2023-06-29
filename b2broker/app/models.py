from django.db import models, transaction as db_transaction


class Wallet(models.Model):
    label = models.CharField(max_length=200, blank=True, null=True)
    balance = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )


class Transaction(models.Model):
    wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    txid = models.CharField(max_length=200, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    def delete(self, *args, **kwargs):
        with db_transaction.atomic():
            self._delete_from_wallet()
            result = super().delete(*args, **kwargs)

        return result

    def _delete_from_wallet(self):
        wallet = Wallet.objects.select_for_update().get(pk=self.wallet_id.id)
        if wallet.balance is None:
            return

        wallet.balance = wallet.balance - self.amount
        wallet.save()
