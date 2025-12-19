from rest_framework import serializers
from .models import Payment, PaymentRefund, Wallet, WalletTransaction
from apps.bookings.serializers import BookingSerializer
from apps.users.serializers import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    booking_details = BookingSerializer(source='booking', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_successful = serializers.BooleanField(read_only=True)
    is_refunded = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'payment_id', 'user', 'user_details', 'booking', 'booking_details',
                 'order_id', 'amount', 'currency', 'payment_method', 'payment_method_display',
                 'payment_gateway', 'status', 'status_display', 'gateway_response',
                 'gateway_payment_id', 'initiated_at', 'completed_at', 'refunded_at',
                 'refund_amount', 'refund_reason', 'refund_gateway_id', 'description',
                 'metadata', 'is_successful', 'is_refunded', 'created_at']
        read_only_fields = ['id', 'payment_id', 'created_at', 'is_successful', 'is_refunded']

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['booking', 'amount', 'payment_method', 'payment_gateway']

class PaymentRefundSerializer(serializers.ModelSerializer):
    payment_details = PaymentSerializer(source='payment', read_only=True)
    processed_by_details = UserSerializer(source='processed_by', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = PaymentRefund
        fields = ['id', 'refund_id', 'payment', 'payment_details', 'amount', 'reason',
                 'status', 'status_display', 'gateway_refund_id', 'gateway_response',
                 'processed_by', 'processed_by_details', 'processed_at', 'created_at']
        read_only_fields = ['id', 'refund_id', 'created_at']

class WalletSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'user_details', 'balance', 'currency', 'created_at']
        read_only_fields = ['id', 'created_at']

class WalletTransactionSerializer(serializers.ModelSerializer):
    wallet_details = WalletSerializer(source='wallet', read_only=True)
    reference_payment_details = PaymentSerializer(source='reference_payment', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    
    class Meta:
        model = WalletTransaction
        fields = ['id', 'transaction_id', 'wallet', 'wallet_details', 'amount',
                 'transaction_type', 'transaction_type_display', 'balance_before',
                 'balance_after', 'description', 'reference_payment',
                 'reference_payment_details', 'created_at']
        read_only_fields = ['id', 'transaction_id', 'created_at']