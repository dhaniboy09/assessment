from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Account


class Balance(APIView):
    def get(self, request, pk):
        try:
            account = Account.objects.get(id=pk)
            balance = account.get_balance()
            return Response(status=status.HTTP_200_OK, data={"balance": balance})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=e)


class Deposit(APIView):
    def put(self, request, pk, format=None):
        amount = request.data.get('amount')
        try:
            account = Account.objects.get(id=pk)
            account.deposit(amount)
            return Response(status=status.HTTP_200_OK, data="Success")
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=e)


class Withdraw(APIView):
    def put(self, request, pk, format=None):
        amount = request.data.get('amount')
        try:
            account = Account.objects.get(id=pk)
            account.withdraw(amount)
            return Response(status=status.HTTP_200_OK, data="Success")
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=e)
