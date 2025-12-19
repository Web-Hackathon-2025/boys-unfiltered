from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

urlpatterns = [
    # Payments
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    
    # Refunds
    path('refunds/', views.PaymentRefundCreateView.as_view(), name='refund-create'),
    path('refunds/<int:pk>/', views.PaymentRefundDetailView.as_view(), name='refund-detail'),
    
    # Wallet
    path('wallet/', views.WalletDetailView.as_view(), name='wallet-detail'),
    path('wallet/transactions/', views.WalletTransactionListView.as_view(), name='wallet-transactions'),
    path('wallet/deposit/', views.WalletDepositView.as_view(), name='wallet-deposit'),
    path('wallet/withdraw/', views.WalletWithdrawView.as_view(), name='wallet-withdraw'),
]