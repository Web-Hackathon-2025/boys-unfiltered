from rest_framework import serializers
from .models import Booking, BookingStatusHistory, BookingAttachment
from apps.services.serializers import ServiceSerializer
from apps.providers.serializers import ServiceProviderSerializer
from apps.users.serializers import UserSerializer

class BookingAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = BookingAttachment
        fields = ['id', 'file_type', 'file', 'uploaded_by', 'uploaded_by_name',
                 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class BookingStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source='changed_by.get_full_name', read_only=True)
    
    class Meta:
        model = BookingStatusHistory
        fields = ['id', 'old_status', 'new_status', 'changed_by', 'changed_by_name',
                 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    customer_details = UserSerializer(source='customer', read_only=True)
    provider_details = ServiceProviderSerializer(source='provider', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    total_amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    balance_amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    is_past_due = serializers.BooleanField(read_only=True)
    attachments = BookingAttachmentSerializer(many=True, read_only=True)
    status_history = BookingStatusHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'booking_number', 'customer', 'customer_details',
                 'provider', 'provider_details', 'service', 'service_details',
                 'scheduled_date', 'scheduled_time', 'estimated_duration_minutes',
                 'service_address', 'city', 'state', 'postal_code', 'latitude',
                 'longitude', 'problem_description', 'customer_notes',
                 'provider_notes', 'status', 'status_display', 'priority',
                 'priority_display', 'status_changed_at', 'quoted_price',
                 'final_price', 'additional_charges', 'discount_amount',
                 'total_amount', 'payment_status', 'payment_status_display',
                 'advance_paid', 'balance_amount', 'assigned_at', 'started_at',
                 'completed_at', 'cancelled_at', 'cancellation_reason',
                 'is_urgent', 'requires_follow_up', 'follow_up_date',
                 'is_past_due', 'attachments', 'status_history',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'booking_number', 'status_changed_at',
                           'total_amount', 'balance_amount', 'is_past_due',
                           'created_at', 'updated_at']

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['customer', 'provider', 'service', 'scheduled_date',
                 'scheduled_time', 'service_address', 'city', 'state',
                 'postal_code', 'problem_description', 'customer_notes',
                 'quoted_price']
    
    def validate(self, attrs):
        # Check if provider is available
        provider = attrs.get('provider')
        if not provider.is_available:
            raise serializers.ValidationError(
                {"provider": "This provider is currently not available for bookings."}
            )
        
        # Check if service is active
        service = attrs.get('service')
        if not service.is_available:
            raise serializers.ValidationError(
                {"service": "This service is currently not available."}
            )
        
        return attrs

class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status', 'provider_notes', 'final_price', 'additional_charges',
                 'discount_amount', 'payment_status', 'advance_paid',
                 'cancellation_reason']