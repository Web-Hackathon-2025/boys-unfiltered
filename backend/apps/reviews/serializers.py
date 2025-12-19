from rest_framework import serializers
from .models import Review, ReviewImage, ReviewHelpful, ProviderReport
from apps.bookings.serializers import BookingSerializer
from apps.providers.serializers import ServiceProviderSerializer
from apps.users.serializers import UserSerializer

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image', 'caption', 'display_order']
        read_only_fields = ['id']

class ReviewHelpfulSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = ReviewHelpful
        fields = ['id', 'user', 'user_name', 'is_helpful', 'created_at']
        read_only_fields = ['id', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    customer_details = UserSerializer(source='customer', read_only=True)
    provider_details = ServiceProviderSerializer(source='provider', read_only=True)
    booking_details = BookingSerializer(source='booking', read_only=True)
    average_detailed_rating = serializers.FloatField(read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)
    helpful_votes = ReviewHelpfulSerializer(many=True, read_only=True)
    helpful_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'booking', 'booking_details', 'customer', 'customer_details',
                 'provider', 'provider_details', 'rating', 'punctuality_rating',
                 'professionalism_rating', 'quality_rating', 'communication_rating',
                 'average_detailed_rating', 'title', 'comment', 'response',
                 'responded_at', 'is_verified', 'is_featured', 'helpful_count',
                 'is_approved', 'moderated_by', 'moderated_at', 'moderation_notes',
                 'images', 'helpful_votes', 'created_at']
        read_only_fields = ['id', 'is_verified', 'is_featured', 'helpful_count',
                           'is_approved', 'moderated_by', 'moderated_at',
                           'moderation_notes', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['booking', 'rating', 'title', 'comment', 'punctuality_rating',
                 'professionalism_rating', 'quality_rating', 'communication_rating']
    
    def validate(self, attrs):
        booking = attrs.get('booking')
        
        # Check if booking is completed
        if booking.status != 'completed':
            raise serializers.ValidationError(
                {"booking": "You can only review completed bookings."}
            )
        
        # Check if review already exists for this booking
        if Review.objects.filter(booking=booking).exists():
            raise serializers.ValidationError(
                {"booking": "A review already exists for this booking."}
            )
        
        # Check if customer is the one who made the booking
        if booking.customer != self.context['request'].user:
            raise serializers.ValidationError(
                {"booking": "You can only review your own bookings."}
            )
        
        return attrs

class ProviderReportSerializer(serializers.ModelSerializer):
    reporter_details = UserSerializer(source='reporter', read_only=True)
    provider_details = ServiceProviderSerializer(source='provider', read_only=True)
    booking_details = BookingSerializer(source='booking', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    
    class Meta:
        model = ProviderReport
        fields = ['id', 'reporter', 'reporter_details', 'provider', 'provider_details',
                 'booking', 'booking_details', 'report_type', 'report_type_display',
                 'description', 'evidence', 'status', 'status_display',
                 'resolved_by', 'resolution', 'resolved_at', 'created_at']
        read_only_fields = ['id', 'status', 'resolved_by', 'resolution',
                           'resolved_at', 'created_at']