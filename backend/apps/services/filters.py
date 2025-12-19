import django_filters
from .models import Service

class ServiceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='base_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='base_price', lookup_expr='lte')
    min_rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    
    class Meta:
        model = Service
        fields = ['category', 'provider', 'price_unit', 'is_available']