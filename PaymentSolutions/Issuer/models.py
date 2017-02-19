from django.db import models
import datetime


class Account(models.Model):
    account_holder_name = models.CharField(max_length=30)
    balance = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    creation_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        db_table = "Account"
        ordering = ['creation_date']

    def __str__(self):
        return self.account_holder_name


class CardInstrument(models.Model):
    card_number = models.CharField(max_length=16)
    bank_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        db_table = "CardInstruments"
        ordering = ['issued_date']

    def __str__(self):
        return self.card_number


class Merchant(models.Model):
    merchant_mcc = models.CharField(max_length=4)
    merchant_name = models.CharField(max_length=100)
    merchant_city = models.CharField(max_length=50)
    merchant_country = models.CharField(max_length=30)
    bank_account = models.OneToOneField(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = "Merchant"
        ordering = ['merchant_name']

    def __str__(self):
        return self.merchant_name


class Currency(models.Model):
    currency_code = models.CharField(max_length=20)
    exchange_rate = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    class Meta:
        db_table = "Currency"
        ordering = ["currency_code"]

    def __str__(self):
        return self.currency_code


class Transaction(models.Model):
    issuer_account = models.ForeignKey(Account, related_name="from_account", on_delete=models.CASCADE)
    acquirer_account = models.ForeignKey(Account, related_name="to_account", on_delete=models.CASCADE)
    billing_currency = models.ForeignKey(Currency, related_name="bill_currency", default=1)
    billing_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    transaction_currency = models.ForeignKey(Currency, related_name="trans_currency", default=1)
    transaction_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    transaction_status = models.CharField(max_length=10, blank=True)
    transaction_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        db_table = "Transaction"
        ordering = ['transaction_date']

    def __str__(self):
        return self.transaction_status


class Transfer(models.Model):
    account_number = models.ForeignKey(Account, related_name="account_details")
    transfer_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    transfer_type = models.CharField(max_length=20)  # authorisation, presentment
    transaction_id = models.ForeignKey(Transaction, related_name="to_trans", on_delete=models.CASCADE)
    transfer_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        db_table = "Transfer"
        ordering = ['transfer_date']

    def __str__(self):
        return str(self.account_number)
