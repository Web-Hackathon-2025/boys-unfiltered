from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Review, ReviewImage, ReviewHelpful, ProviderReport

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

class ReviewHelpfulInline(admin.TabularInline):
    model = ReviewHelpful
    extra = 0
    readonly_fields = ('user', 'created_at')
    raw_id_fields = ('user',)
    
    def has_add_permission(self, request, obj):
        return False

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking_number', 'provider_name', 'customer_email', 
                   'rating', 'average_detailed_rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'is_verified', 'created_at')
    search_fields = ('customer__email', 'provider__business_name', 'booking__booking_number', 
                    'title', 'comment')
    readonly_fields = ('average_detailed_rating', 'helpful_count', 'created_at', 'updated_at')
    raw_id_fields = ('customer', 'provider', 'booking', 'moderated_by')
    inlines = [ReviewImageInline, ReviewHelpfulInline]
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    def booking_number(self, obj):
        return obj.booking.booking_number if obj.booking else '-'
    booking_number.short_description = 'Booking'
    
    def provider_name(self, obj):
        return obj.provider.business_name if obj.provider else '-'
    provider_name.short_description = 'Provider'
    
    def customer_email(self, obj):
        return obj.customer.email if obj.customer else '-'
    customer_email.short_description = 'Customer'
    
    def average_detailed_rating(self, obj):
        return f"{obj.average_detailed_rating:.1f}"
    average_detailed_rating.short_description = 'Avg Detailed'
    average_detailed_rating.admin_order_field = 'rating'
    
    fieldsets = (
        ('Review Information', {
            'fields': ('booking', 'customer', 'provider')
        }),
        ('Ratings', {
            'fields': ('rating', 'punctuality_rating', 'professionalism_rating', 
                      'quality_rating', 'communication_rating', 'average_detailed_rating')
        }),
        ('Review Content', {
            'fields': ('title', 'comment', 'response', 'responded_at')
        }),
        ('Verification & Features', {
            'fields': ('is_verified', 'is_featured', 'helpful_count')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'moderated_by', 'moderated_at', 'moderation_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews', 'unapprove_reviews', 'feature_reviews', 'unfeature_reviews']
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved.')
    approve_reviews.short_description = "Approve selected reviews"
    
    def unapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews unapproved.')
    unapprove_reviews.short_description = "Unapprove selected reviews"
    
    def feature_reviews(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} reviews featured.')
    feature_reviews.short_description = "Feature selected reviews"
    
    def unfeature_reviews(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} reviews unfeatured.')
    unfeature_reviews.short_description = "Unfeature selected reviews"

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'image_preview', 'caption', 'display_order')
    list_filter = ('review__provider',)
    search_fields = ('review__customer__email', 'caption')
    raw_id_fields = ('review',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'

@admin.register(ProviderReport)
class ProviderReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter_email', 'provider_name', 'report_type', 
                   'status', 'created_at')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('reporter__email', 'provider__business_name', 'description')
    readonly_fields = ('created_at', 'resolved_at')
    raw_id_fields = ('reporter', 'provider', 'booking', 'resolved_by')
    
    def reporter_email(self, obj):
        return obj.reporter.email if obj.reporter else '-'
    reporter_email.short_description = 'Reporter'
    
    def provider_name(self, obj):
        return obj.provider.business_name if obj.provider else '-'
    provider_name.short_description = 'Provider'
    
    actions = ['mark_as_resolved', 'mark_as_dismissed']
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='resolved', resolved_at=timezone.now(), resolved_by=request.user)
        self.message_user(request, f'{updated} reports marked as resolved.')
    mark_as_resolved.short_description = "Mark selected reports as resolved"
    
    def mark_as_dismissed(self, request, queryset):
        updated = queryset.update(status='dismissed')
        self.message_user(request, f'{updated} reports marked as dismissed.')
    mark_as_dismissed.short_description = "Mark selected reports as dismissed"

admin.site.register(ReviewHelpful)