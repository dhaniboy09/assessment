from django.urls import path

from core.api import views

urlpatterns = [
    path('balance/<int:pk>', views.Balance.as_view(), name='account_balance'),
    path('deposit/<int:pk>', views.Deposit.as_view(), name='deposit'),
    path('withdraw/<int:pk>', views.Withdraw.as_view(), name='withdraw')
]
