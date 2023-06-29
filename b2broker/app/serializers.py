from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from app.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance']
        read_only_fields = ['balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet_id', 'txid', 'amount']

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            self._add_new_transaction_to_wallet(
                wallet_id=instance.wallet_id.id,
                amount=instance.amount
            )
        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            old_amount = instance.amount
            instance = super().update(instance, validated_data)
            self._update_transaction_in_wallet(
                wallet_id=instance.wallet_id.id,
                old_amount=old_amount,
                new_amount=instance.amount,
            )

        return instance

    def _update_transaction_in_wallet(
        self, wallet_id: str, old_amount: Decimal, new_amount: Decimal
    ):
        wallet = Wallet.objects.select_for_update().get(pk=wallet_id)
        balance = wallet.balance or 0
        wallet.balance = balance - old_amount + new_amount
        wallet.save()

    def _add_new_transaction_to_wallet(self, wallet_id: str, amount: Decimal):
        wallet = Wallet.objects.select_for_update().get(pk=wallet_id)
        balance = wallet.balance or 0
        wallet.balance = balance + amount
        wallet.save()
