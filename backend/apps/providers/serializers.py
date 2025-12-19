from rest_framework import serializers
from .models import ServiceProvider, ProviderDocument, ProviderAvailability
from apps.services.serializers import ServiceCategorySerializer, ServiceSerializer
from apps.users.serializers import UserSerializer

class ProviderDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderDocument
        fields = ['id', 'document_type', 'document_name', 'document_file',
                 'is_verified', 'verified_at', 'verification_notes']
        read_only_fields = ['id', 'is_verified', 'verified_at', 'verification_notes']

class ProviderAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderAvailability
        fields = ['id', 'date', 'start_time', 'end_time', 'is_available', 'notes']
        read_only_fields = ['id']

class ServiceProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    service_categories = ServiceCategorySerializer(many=True, read_only=True)
    documents = ProviderDocumentSerializer(many=True, read_only=True)
    availabilities = ProviderAvailabilitySerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    full_address = serializers.CharField(read_only=True)
    
    class Meta:
        model = ServiceProvider
        fields = ['id', 'user', 'business_name', 'business_description',
                 'years_of_experience', 'certifications', 'skills',
                 'service_categories', 'services_offered', 'is_available',
                 'available_from', 'available_to', 'working_days',
                 'emergency_service', 'average_rating', 'total_reviews',
                 'total_jobs_completed', 'completion_rate', 'response_time_minutes',
                 'is_verified', 'verification_status', 'hourly_rate',
                 'min_service_charge', 'address_line1', 'address_line2',
                 'city', 'state', 'country', 'postal_code', 'latitude',
                 'longitude', 'full_address', 'documents', 'availabilities',
                 'services', 'created_at']
        read_only_fields = ['id', 'average_rating', 'total_reviews',
                           'total_jobs_completed', 'completion_rate',
                           'response_time_minutes', 'is_verified', 'created_at']

class ServiceProviderCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ServiceProvider
        fields = ['id', 'user_id', 'business_name', 'business_description',
                 'years_of_experience', 'address_line1', 'city', 'state',
                 'country', 'postal_code']
    
    def validate_user_id(self, value):
        from apps.users.models import User
        try:
            user = User.objects.get(id=value, role='provider')
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found or not a provider")
        return value
    
    def create(self, validated_data):
        from apps.users.models import User
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        provider = ServiceProvider.objects.create(user=user, **validated_data)
        return provider

class ProviderProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = ['business_name', 'business_description', 'years_of_experience',
                 'skills', 'available_from', 'available_to', 'working_days',
                 'emergency_service', 'hourly_rate', 'min_service_charge',
                 'address_line1', 'address_line2', 'city', 'state',
                 'country', 'postal_code', 'latitude', 'longitude']