from django.contrib.auth.models import User

from .serializers import UserSerializer, AuthorizationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Merchant, Account, CardInstrument, Currency, Transaction, Transfer
from decimal import *


class UserList(APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Authorization(APIView):
    def post(self, request, format=None):
        serializer = AuthorizationSerializer(data=request.data)
        if serializer.is_valid():
            issuer_act = CardInstrument.objects.get(card_number=serializer.data['card_id'])
            merchant_act = Merchant.objects.get(merchant_mcc=serializer.data['merchant_mcc'])
            billing_currency = Currency.objects.get(currency_code=serializer.data['billing_currency'])
            billing_amt = serializer.data['billing_amount']
            transaction_currency = Currency.objects.get(currency_code=serializer.data['billing_currency'])
            transaction_amt = serializer.data['billing_amount']
            transaction_status = serializer.data['type']
            transaction = Transaction(id=None, issuer_account=issuer_act.bank_account,
                                      acquirer_account=merchant_act.bank_account, billing_currency=billing_currency,
                                      billing_amount=Decimal(billing_amt), transaction_currency=transaction_currency,
                                      transaction_amount=Decimal(transaction_amt),
                                      transaction_status=transaction_status)
            transaction.save()
            print(Transaction.objects.all)
            print("Post method invoked")
            return Response(transaction)
