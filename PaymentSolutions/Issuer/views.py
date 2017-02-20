from .serializers import AuthorizationSerializer, PresentmentSerializer, TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Merchant, Account, CardInstrument, Currency, Transaction, Transfer
from decimal import *


class Authorization(APIView):
    def post(self, request):
        try:
            serializer = AuthorizationSerializer(data=request.data)
            if serializer.is_valid():
                issuer_act = CardInstrument.objects.get(card_number=serializer.data['card_id'])
                merchant_act = Merchant.objects.get(merchant_mcc=serializer.data['merchant_mcc'])
                billing_currency = Currency.objects.get(currency_code=serializer.data['billing_currency'])
                transaction_currency = Currency.objects.get(currency_code=serializer.data['transaction_currency'])
                transaction_amt = serializer.data['transaction_amount']
                transaction_type = serializer.data['type']
                billing_amount = (Decimal(transaction_amt) * billing_currency.exchange_rate)
                print(issuer_act.bank_account.balance)
                print(billing_amount)
                if issuer_act.bank_account.balance >= billing_amount:
                    transaction = Transaction(id=None, issuer_account=issuer_act.bank_account,
                                              acquirer_account=merchant_act.bank_account,
                                              billing_currency=billing_currency,
                                              billing_amount=Decimal(billing_amount),
                                              transaction_currency=transaction_currency,
                                              transaction_amount=Decimal(transaction_amt),
                                              transaction_status=transaction_type,
                                              settlement_amount=0.0,
                                              settlement_currency=billing_currency)
                    transaction.save()

                    transfer = Transfer(id=None, transfer_amount=-1 * Decimal(billing_amount),
                                        transfer_type=transaction_type, transaction_id=transaction,
                                        account_number=issuer_act.bank_account)
                    transfer.save()

                    return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_403_FORBIDDEN)


class Presentment(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(transaction_status="presentment")
        txn_data = TransactionSerializer(transactions, many=True)
        return Response(txn_data.data)

    def post(self, request):
        try:
            serializer = PresentmentSerializer(data=request.data)
            if serializer.is_valid():
                issuer_act = CardInstrument.objects.get(card_number=serializer.data['card_id'])
                merchant_act = Merchant.objects.get(merchant_mcc=serializer.data['merchant_mcc'])
                billing_currency = Currency.objects.get(currency_code=serializer.data['billing_currency'])
                transaction_currency = Currency.objects.get(currency_code=serializer.data['transaction_currency'])
                transaction_amt = serializer.data['transaction_amount']
                transaction_type = serializer.data['type']
                settlement_currency = Currency.objects.get(currency_code=serializer.data['settlement_currency'])
                settlement_amount = (Decimal(transaction_amt) * settlement_currency.exchange_rate)
                billing_amount = (Decimal(transaction_amt) * billing_currency.exchange_rate)

                print(issuer_act.bank_account.balance)
                print(settlement_amount)
                if issuer_act.bank_account.balance >= settlement_amount:
                    transaction = Transaction(id=None, issuer_account=issuer_act.bank_account,
                                              acquirer_account=merchant_act.bank_account,
                                              billing_currency=billing_currency,
                                              billing_amount=Decimal(billing_amount),
                                              transaction_currency=transaction_currency,
                                              transaction_amount=Decimal(transaction_amt),
                                              transaction_status=transaction_type,
                                              settlement_amount=settlement_amount,
                                              settlement_currency=settlement_currency)
                    transaction.save()

                    transfer = Transfer(id=None, transfer_amount=-1 * Decimal(settlement_amount),
                                        transfer_type=transaction_type, transaction_id=transaction,
                                        account_number=issuer_act.bank_account)
                    transfer.save()
                    return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

        return Response(status=status.HTTP_403_FORBIDDEN)
