from rest_framework import serializers
from .models import BaseModel, TimeStampedModel, UUIDModel, Address

class BaseModelSerializer(serializers.ModelSerializer):
    """Base serializer for models inheriting from BaseModel."""
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        model = None  # Should be overridden in subclasses
        fields = ['id', 'created_at', 'updated_at', 'is_active']


class TimeStampedSerializer(serializers.ModelSerializer):
    """Serializer for models with timestamps."""
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = None
        fields = ['created_at', 'updated_at']


class UUIDSerializer(serializers.ModelSerializer):
    """Serializer for models with UUID primary key."""
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = None
        fields = ['id']


class AddressSerializer(serializers.Serializer):
    """Serializer for Address mixin fields."""
    address_line1 = serializers.CharField(max_length=255, required=True)
    address_line2 = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(max_length=100, required=True)
    state = serializers.CharField(max_length=100, required=True)
    country = serializers.CharField(max_length=100, default='India')
    postal_code = serializers.CharField(max_length=20, required=True)
    latitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False, 
        allow_null=True,
        help_text="Latitude coordinate"
    )
    longitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False, 
        allow_null=True,
        help_text="Longitude coordinate"
    )
    
    def to_representation(self, instance):
        """Convert model instance to dictionary."""
        ret = super().to_representation(instance)
        # Format the full address for display
        address_parts = [instance.address_line1]
        if instance.address_line2:
            address_parts.append(instance.address_line2)
        address_parts.extend([
            instance.city,
            instance.state,
            instance.country,
            instance.postal_code
        ])
        ret['full_address'] = ', '.join(filter(None, address_parts))
        return ret


class ModelChoiceSerializer(serializers.Serializer):
    """Serializer for model choice fields."""
    value = serializers.CharField()
    label = serializers.CharField()


class PaginationSerializer(serializers.Serializer):
    """Serializer for pagination metadata."""
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()


class SuccessResponseSerializer(serializers.Serializer):
    """Standard success response serializer."""
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    data = serializers.DictField(required=False, allow_null=True)


class ErrorResponseSerializer(serializers.Serializer):
    """Standard error response serializer."""
    success = serializers.BooleanField(default=False)
    error = serializers.CharField()
    error_code = serializers.CharField(required=False)
    details = serializers.DictField(required=False, allow_null=True)


class ValidationErrorSerializer(serializers.Serializer):
    """Serializer for validation errors."""
    field = serializers.CharField()
    message = serializers.CharField()
    code = serializers.CharField(required=False)


class ListResponseSerializer(serializers.Serializer):
    """Standard list response serializer."""
    success = serializers.BooleanField(default=True)
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()


class EmptyResponseSerializer(serializers.Serializer):
    """Empty response serializer."""
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()


# Mixin serializers for use in other serializers
class BaseModelMixinSerializer:
    """Mixin to add BaseModel fields to other serializers."""
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)


class TimeStampedMixinSerializer:
    """Mixin to add timestamp fields to other serializers."""
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class UUIDMixinSerializer:
    """Mixin to add UUID field to other serializers."""
    id = serializers.UUIDField(read_only=True)


class AddressMixinSerializer:
    """Mixin to add Address fields to other serializers."""
    address_line1 = serializers.CharField(max_length=255, required=True)
    address_line2 = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(max_length=100, required=True)
    state = serializers.CharField(max_length=100, required=True)
    country = serializers.CharField(max_length=100, default='India')
    postal_code = serializers.CharField(max_length=20, required=True)
    latitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False, 
        allow_null=True
    )
    longitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=False, 
        allow_null=True
    )
    
    def get_full_address(self, obj):
        """Get formatted full address."""
        address_parts = [obj.address_line1]
        if obj.address_line2:
            address_parts.append(obj.address_line2)
        address_parts.extend([
            obj.city,
            obj.state,
            obj.country,
            obj.postal_code
        ])
        return ', '.join(filter(None, address_parts))
    
    full_address = serializers.SerializerMethodField()


# Utility serializers
class IDNameSerializer(serializers.Serializer):
    """Serializer for ID and name representation."""
    id = serializers.UUIDField()
    name = serializers.CharField()


class StatusSerializer(serializers.Serializer):
    """Serializer for status responses."""
    status = serializers.CharField()
    message = serializers.CharField(required=False)


class CountSerializer(serializers.Serializer):
    """Serializer for count responses."""
    count = serializers.IntegerField()


class BulkOperationSerializer(serializers.Serializer):
    """Serializer for bulk operations."""
    ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="List of IDs to perform operation on"
    )
    action = serializers.CharField(
        help_text="Action to perform (activate, deactivate, delete, etc.)"
    )


class CSVImportSerializer(serializers.Serializer):
    """Serializer for CSV import."""
    file = serializers.FileField(help_text="CSV file to import")
    overwrite = serializers.BooleanField(default=False, help_text="Overwrite existing records")


class ExportSerializer(serializers.Serializer):
    """Serializer for data export."""
    format = serializers.ChoiceField(
        choices=['csv', 'json', 'xlsx'],
        default='json'
    )
    fields = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Specific fields to export"
    )
    filters = serializers.DictField(
        required=False,
        help_text="Filter criteria"
    )


# Geo serializers
class LocationSerializer(serializers.Serializer):
    """Serializer for geographic location."""
    latitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=True
    )
    longitude = serializers.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=True
    )
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    country = serializers.CharField(required=False)


class DistanceSerializer(serializers.Serializer):
    """Serializer for distance calculation."""
    from_location = LocationSerializer()
    to_location = LocationSerializer()
    distance_km = serializers.FloatField(read_only=True)
    distance_miles = serializers.FloatField(read_only=True)


class BoundingBoxSerializer(serializers.Serializer):
    """Serializer for geographic bounding box."""
    min_lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    max_lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    min_lng = serializers.DecimalField(max_digits=9, decimal_places=6)
    max_lng = serializers.DecimalField(max_digits=9, decimal_places=6)


class SearchRadiusSerializer(serializers.Serializer):
    """Serializer for radius-based search."""
    center = LocationSerializer()
    radius_km = serializers.FloatField(min_value=0.1, max_value=100)