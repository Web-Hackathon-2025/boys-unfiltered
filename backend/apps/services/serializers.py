from rest_framework import serializers
from .models import ServiceCategory, Service, ServicePackage, ServiceRequest

class ServiceCategorySerializer(serializers.ModelSerializer):
    has_subcategories = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'image', 
                 'parent', 'display_order', 'has_subcategories', 'is_active']
        read_only_fields = ['id', 'slug', 'has_subcategories']

class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    price_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'title', 'slug', 'description', 'category', 'category_name',
                 'provider', 'provider_name', 'base_price', 'price_unit', 'minimum_charge',
                 'price_display', 'is_price_negotiable', 'estimated_duration_minutes',
                 'warranty_months', 'requirements', 'tools_needed', 'is_available',
                 'available_from', 'available_to', 'total_bookings', 'average_rating',
                 'images', 'created_at']
        read_only_fields = ['id', 'slug', 'total_bookings', 'average_rating', 'created_at']

class ServicePackageSerializer(serializers.ModelSerializer):
    discounted_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    service_title = serializers.CharField(source='service.title', read_only=True)
    
    class Meta:
        model = ServicePackage
        fields = ['id', 'service', 'service_title', 'name', 'description', 'price',
                 'discount_percentage', 'discounted_price', 'included_items',
                 'validity_days', 'created_at']
        read_only_fields = ['id', 'created_at']

class ServiceRequestSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = ['id', 'customer', 'customer_name', 'category', 'category_name',
                 'title', 'description', 'location', 'preferred_date', 'preferred_time',
                 'budget_min', 'budget_max', 'status', 'status_display', 'images',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'customer_name',
                           'category_name', 'status_display']