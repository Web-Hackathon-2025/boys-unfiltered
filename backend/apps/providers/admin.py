from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ServiceProvider, ProviderServiceCategory, ProviderDocument, ProviderAvailability

class ProviderDocumentInline(admin.TabularInline):
    model = ProviderDocument
    extra = 1
    readonly_fields = ('is_verified', 'verified_at', 'verified_by')
    
    def has_change_permission(self, request, obj=None):
        return False

class ProviderAvailabilityInline(admin.TabularInline):
    model = ProviderAvailability
    extra = 1
    fields = ('date', 'start_time', 'end_time', 'is_available', 'notes')
    ordering = ('date', 'start_time')

class ProviderServiceCategoryInline(admin.TabularInline):
    model = ProviderServiceCategory
    extra = 1
    autocomplete_fields = ['category']

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user_email', 'city', 'average_rating', 'total_reviews', 
                   'is_verified', 'is_available', 'verification_status')
    list_filter = ('is_verified', 'is_available', 'verification_status', 'city', 'state')
    search_fields = ('business_name', 'user__email', 'user__first_name', 'user__last_name', 'city')
    readonly_fields = ('average_rating', 'total_reviews', 'total_jobs_completed', 
                      'completion_rate', 'response_time_minutes', 'full_address')
    raw_id_fields = ('user',)
    inlines = [ProviderServiceCategoryInline, ProviderDocumentInline, ProviderAvailabilityInline]
    list_per_page = 25
    
    def user_email(self, obj):
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'
    
    def view_bookings_link(self, obj):
        url = reverse('admin:bookings_booking_changelist') + f'?provider__id__exact={obj.id}'
        return format_html('<a href="{}">View Bookings ({})</a>', url, obj.bookings.count())
    view_bookings_link.short_description = 'Bookings'
    
    def view_reviews_link(self, obj):
        url = reverse('admin:reviews_review_changelist') + f'?provider__id__exact={obj.id}'
        return format_html('<a href="{}">View Reviews ({})</a>', url, obj.reviews.count())
    view_reviews_link.short_description = 'Reviews'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Business Information', {
            'fields': ('business_name', 'business_registration_number', 'business_description', 'business_logo')
        }),
        ('Professional Information', {
            'fields': ('years_of_experience', 'certifications', 'skills', 'services_offered')
        }),
        ('Availability', {
            'fields': ('is_available', 'available_from', 'available_to', 'working_days', 'emergency_service')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'country', 
                      'postal_code', 'latitude', 'longitude', 'full_address')
        }),
        ('Performance Metrics', {
            'fields': ('average_rating', 'total_reviews', 'total_jobs_completed', 
                      'completion_rate', 'response_time_minutes'),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_status', 'verification_notes')
        }),
        ('Pricing', {
            'fields': ('hourly_rate', 'min_service_charge')
        }),
        ('Quick Links', {
            'fields': ('view_bookings_link', 'view_reviews_link'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProviderDocument)
class ProviderDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'provider', 'document_type', 'is_verified', 'verified_at', 'verified_by')
    list_filter = ('document_type', 'is_verified', 'verified_at')
    search_fields = ('document_name', 'provider__business_name')
    readonly_fields = ('verified_at',)
    raw_id_fields = ('provider', 'verified_by')
    
    def save_model(self, request, obj, form, change):
        if 'is_verified' in form.changed_data and obj.is_verified:
            obj.verified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ProviderAvailability)
class ProviderAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('provider', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('is_available', 'date', 'provider')
    search_fields = ('provider__business_name', 'notes')
    date_hierarchy = 'date'
    ordering = ('date', 'start_time')

admin.site.register(ProviderServiceCategory)