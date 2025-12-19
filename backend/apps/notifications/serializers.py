from rest_framework import serializers
from .models import Notification, NotificationTemplate, UserNotificationPreference, SMSLog, EmailLog
from apps.users.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    channel_display = serializers.CharField(source='get_channel_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'user_details', 'notification_type', 'notification_type_display',
                 'title', 'message', 'data', 'channel', 'channel_display', 'is_read',
                 'read_at', 'is_sent', 'sent_at', 'action_url', 'action_text',
                 'priority', 'expiry_date', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_read', 'read_at', 'is_sent', 'sent_at']

class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'notification_type', 'title', 'message', 'data', 
                 'channel', 'action_url', 'action_text', 'priority', 'expiry_date']

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'name', 'notification_type', 'channel', 'subject',
                 'message_template', 'html_template', 'variables', 'is_active',
                 'created_at']
        read_only_fields = ['id', 'created_at']

class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = UserNotificationPreference
        fields = ['id', 'user', 'user_details', 'email_notifications', 
                 'sms_notifications', 'push_notifications', 'in_app_notifications',
                 'booking_updates', 'payment_updates', 'review_updates',
                 'promotional_emails', 'system_alerts', 'quiet_hours_enabled',
                 'quiet_hours_start', 'quiet_hours_end', 'dnd_until', 'created_at']
        read_only_fields = ['id', 'created_at']

class SMSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSLog
        fields = ['id', 'recipient', 'message', 'template_id', 'provider',
                 'status', 'provider_message_id', 'error_message', 'cost',
                 'created_at']
        read_only_fields = ['id', 'created_at']

class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = ['id', 'recipient', 'subject', 'template_id', 'status',
                 'provider_message_id', 'error_message', 'created_at']
        read_only_fields = ['id', 'created_at']

class MarkAsReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=True
    )

class NotificationCountSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    unread = serializers.IntegerField()