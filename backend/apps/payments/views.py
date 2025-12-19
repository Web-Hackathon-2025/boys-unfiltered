from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

from .models import Payment, PaymentRefund, Wallet, WalletTransaction
from .serializers import (
    PaymentSerializer, PaymentCreateSerializer,
    PaymentRefundSerializer, WalletSerializer,
    WalletTransactionSerializer
)
from apps.users.permissions import IsCustomer, IsServiceProvider, IsAdmin


class PaymentListView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Payment.objects.filter(user=user)
        elif user.role == 'provider':
            # Providers can see payments for their bookings
            return Payment.objects.filter(booking__provider=user.provider_profile)
        return Payment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Payment.objects.filter(user=user)
        elif user.role == 'provider':
            return Payment.objects.filter(booking__provider=user.provider_profile)
        return Payment.objects.all()


class PaymentRefundCreateView(generics.CreateAPIView):
    serializer_class = PaymentRefundSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def perform_create(self, serializer):
        serializer.save(processed_by=self.request.user)


class PaymentRefundDetailView(generics.RetrieveAPIView):
    queryset = PaymentRefund.objects.all()
    serializer_class = PaymentRefundSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class WalletDetailView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        return wallet


class WalletTransactionListView(generics.ListAPIView):
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        return WalletTransaction.objects.filter(wallet=wallet)


class WalletDepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        amount = request.data.get('amount')
        description = request.data.get('description', 'Deposit')
        
        if not amount or float(amount) <= 0:
            return Response({"error": "Valid amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        
        try:
            wallet.deposit(float(amount), description)
            return Response({
                "message": "Deposit successful",
                "balance": wallet.balance
            })
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WalletWithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        amount = request.data.get('amount')
        description = request.data.get('description', 'Withdrawal')
        
        if not amount or float(amount) <= 0:
            return Response({"error": "Valid amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        
        try:
            wallet.withdraw(float(amount), description)
            return Response({
                "message": "Withdrawal successful",
                "balance": wallet.balance
            })
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request):
        stats = {
            'total_payments': Payment.objects.count(),
            'total_amount': Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0,
            'successful_payments': Payment.objects.filter(status='success').count(),
            'pending_payments': Payment.objects.filter(status='pending').count(),
            'failed_payments': Payment.objects.filter(status='failed').count(),
            'total_refunds': PaymentRefund.objects.count(),
            'total_refund_amount': PaymentRefund.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        return Response(stats)
    
class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)