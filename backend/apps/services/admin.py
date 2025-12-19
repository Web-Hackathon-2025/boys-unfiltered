from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceCategory, Service, ServicePackage, ServiceRequest

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'display_order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'provider_name', 'base_price', 'price_unit', 'is_available', 'average_rating')
    list_filter = ('category', 'is_available', 'price_unit', 'provider__is_verified')
    search_fields = ('title', 'description', 'provider__business_name')
    readonly_fields = ('slug', 'total_bookings', 'average_rating', 'created_at', 'updated_at')
    raw_id_fields = ('provider', 'category')
    list_per_page = 20
    
    def provider_name(self, obj):
        return obj.provider.business_name if obj.provider else '-'
    provider_name.short_description = 'Provider'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('provider', 'category', 'title', 'slug', 'description', 'detailed_description')
        }),
        ('Pricing', {
            'fields': ('base_price', 'price_unit', 'minimum_charge', 'is_price_negotiable')
        }),
        ('Service Details', {
            'fields': ('estimated_duration_minutes', 'warranty_months', 'requirements', 'tools_needed')
        }),
        ('Availability', {
            'fields': ('is_available', 'available_from', 'available_to')
        }),
        ('Statistics', {
            'fields': ('total_bookings', 'average_rating', 'images'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price', 'discount_percentage', 'discounted_price', 'validity_days')
    list_filter = ('service__category',)
    search_fields = ('name', 'service__title')
    readonly_fields = ('discounted_price',)
    
    def discounted_price(self, obj):
        return obj.discounted_price
    discounted_price.short_description = 'Discounted Price'

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'category', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'category', 'preferred_date')
    search_fields = ('title', 'description', 'customer__email')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('customer', 'category')
    
    fieldsets = (
        ('Request Details', {
            'fields': ('customer', 'category', 'title', 'description')
        }),
        ('Location & Timing', {
            'fields': ('location', 'preferred_date', 'preferred_time')
        }),
        ('Budget', {
            'fields': ('budget_min', 'budget_max')
        }),
        ('Status & Images', {
            'fields': ('status', 'images')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(ServiceCategory, ServiceCategoryAdmin)