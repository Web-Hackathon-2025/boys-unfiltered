from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Notification, NotificationTemplate, UserNotificationPreference, SMSLog, EmailLog

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_email', 'notification_type', 'channel', 
                   'is_read', 'is_sent', 'priority', 'created_at')
    list_filter = ('notification_type', 'channel', 'is_read', 'is_sent', 'priority', 'created_at')
    search_fields = ('title', 'message', 'user__email')
    readonly_fields = ('created_at', 'read_at', 'sent_at')
    raw_id_fields = ('user',)
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    def user_email(self, obj):
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message Preview'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'notification_type', 'title', 'message', 'data')
        }),
        ('Delivery', {
            'fields': ('channel', 'is_sent', 'sent_at', 'action_url', 'action_text')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at', 'priority', 'expiry_date')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_sent']
    
    def mark_as_read(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_read=True, read_at=timezone.now())
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = "Mark selected as unread"
    
    def mark_as_sent(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_sent=True, sent_at=timezone.now())
        self.message_user(request, f'{updated} notifications marked as sent.')
    mark_as_sent.short_description = "Mark selected as sent"

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'notification_type', 'channel', 'is_active', 'created_at')
    list_filter = ('notification_type', 'channel', 'is_active')
    search_fields = ('name', 'subject', 'message_template')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'notification_type', 'channel', 'is_active')
        }),
        ('Templates', {
            'fields': ('subject', 'message_template', 'html_template')
        }),
        ('Variables', {
            'fields': ('variables',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'email_notifications', 'sms_notifications', 
                   'push_notifications', 'in_app_notifications', 'quiet_hours_enabled')
    search_fields = ('user__email',)
    raw_id_fields = ('user',)
    
    def user_email(self, obj):
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'

@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message_preview', 'provider', 'status', 'cost', 'created_at')
    list_filter = ('provider', 'status', 'created_at')
    search_fields = ('recipient', 'message', 'provider_message_id')
    readonly_fields = ('created_at',)
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject_preview', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('recipient', 'subject', 'provider_message_id')
    readonly_fields = ('created_at',)
    
    def subject_preview(self, obj):
        return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
    subject_preview.short_description = 'Subject'