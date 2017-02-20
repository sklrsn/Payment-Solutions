from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class AuthorizationSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    card_id = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    transaction_id = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    merchant_name = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    merchant_country = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    merchant_mcc = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    billing_amount = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    billing_currency = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    transaction_amount = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    transaction_currency = serializers.CharField(max_length=None, min_length=None, allow_blank=False)

    class Meta:
        fields = (
            'type', 'card_id', 'transaction_id', 'merchant_name', 'merchant_country', 'merchant_mcc', 'billing_amount',
            'billing_currency', 'transaction_amount', 'transaction_currency')


class PresentmentSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    card_id = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    transaction_id = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    merchant_name = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    merchant_country = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    merchant_mcc = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    billing_amount = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    billing_currency = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    transaction_amount = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    transaction_currency = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    settlement_amount = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    settlement_currency = serializers.CharField(max_length=None, min_length=None, allow_blank=False)

    class Meta:
        fields = (
            'type', 'card_id', 'transaction_id', 'merchant_name', 'merchant_country', 'merchant_mcc', 'billing_amount',
            'billing_currency', 'transaction_amount', 'transaction_currency', 'settlement_amount',
            'settlement_currency')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'issuer_account', 'acquirer_account', 'billing_currency', 'billing_amount', 'transaction_currency',
            'transaction_amount', 'transaction_status', 'transaction_date',
            'settlement_currency', 'settlement_amount')


class BalanceReportSerializer(serializers.Serializer):
    card_id = serializers.CharField(max_length=None, min_length=None, allow_blank=False)
    from_date = serializers.DateField()
    to_date = serializers.DateField()

    class Meta:
        fields = (
            'card_id', 'from_date', 'to_date')
