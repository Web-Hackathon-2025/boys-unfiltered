from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Booking, BookingStatusHistory, BookingAttachment

class BookingStatusHistoryInline(admin.TabularInline):
    model = BookingStatusHistory
    extra = 0
    readonly_fields = ('old_status', 'new_status', 'changed_by', 'notes', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj):
        return False

class BookingAttachmentInline(admin.TabularInline):
    model = BookingAttachment
    extra = 1
    fields = ('file_type', 'file', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'customer_email', 'provider_name', 'service_title', 
                   'scheduled_date', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'priority', 'scheduled_date', 'city')
    search_fields = ('booking_number', 'customer__email', 'provider__business_name', 
                    'service__title', 'service_address')
    readonly_fields = ('booking_number', 'total_amount', 'balance_amount', 'is_past_due', 
                      'status_changed_at', 'created_at', 'updated_at')
    raw_id_fields = ('customer', 'provider', 'service')
    inlines = [BookingStatusHistoryInline, BookingAttachmentInline]
    list_per_page = 50
    date_hierarchy = 'scheduled_date'
    
    def customer_email(self, obj):
        return obj.customer.email if obj.customer else '-'
    customer_email.short_description = 'Customer'
    customer_email.admin_order_field = 'customer__email'
    
    def provider_name(self, obj):
        return obj.provider.business_name if obj.provider else '-'
    provider_name.short_description = 'Provider'
    
    def service_title(self, obj):
        return obj.service.title if obj.service else '-'
    service_title.short_description = 'Service'
    
    def total_amount(self, obj):
        return f"₹{obj.total_amount}"
    total_amount.short_description = 'Total'
    total_amount.admin_order_field = 'quoted_price'
    
    def view_payments_link(self, obj):
        url = reverse('admin:payments_payment_changelist') + f'?booking__id__exact={obj.id}'
        count = obj.payments.count()
        return format_html('<a href="{}">Payments ({})</a>', url, count)
    view_payments_link.short_description = 'Payments'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_number', 'customer', 'provider', 'service')
        }),
        ('Schedule & Location', {
            'fields': ('scheduled_date', 'scheduled_time', 'estimated_duration_minutes',
                      'service_address', 'city', 'state', 'postal_code', 
                      'latitude', 'longitude')
        }),
        ('Problem Description', {
            'fields': ('problem_description', 'customer_notes', 'provider_notes')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'status_changed_at')
        }),
        ('Pricing', {
            'fields': ('quoted_price', 'final_price', 'additional_charges', 
                      'discount_amount', 'total_amount')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'advance_paid', 'balance_amount', 'view_payments_link')
        }),
        ('Tracking', {
            'fields': ('assigned_at', 'started_at', 'completed_at', 'cancelled_at', 
                      'cancellation_reason')
        }),
        ('Metadata', {
            'fields': ('is_urgent', 'requires_follow_up', 'follow_up_date', 
                      'is_past_due', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} bookings marked as completed.')
    mark_as_completed.short_description = "Mark selected bookings as completed"
    
    def mark_as_cancelled(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='cancelled', cancelled_at=timezone.now())
        self.message_user(request, f'{updated} bookings marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected bookings as cancelled"

@admin.register(BookingStatusHistory)
class BookingStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('booking', 'old_status', 'new_status', 'changed_by', 'created_at')
    list_filter = ('new_status', 'created_at')
    search_fields = ('booking__booking_number', 'changed_by__email')
    readonly_fields = ('booking', 'old_status', 'new_status', 'changed_by', 'notes', 'created_at')
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(BookingAttachment)
class BookingAttachmentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'file_type', 'uploaded_by', 'created_at')
    list_filter = ('file_type',)
    search_fields = ('booking__booking_number', 'uploaded_by__email')
    raw_id_fields = ('booking', 'uploaded_by')