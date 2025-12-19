from django.db import models
from apps.common.models import BaseModel
from apps.users.models import User


class Notification(BaseModel):
    """System notifications model."""
    
    class NotificationType(models.TextChoices):
        SYSTEM = 'system', 'System Notification'
        BOOKING = 'booking', 'Booking Notification'
        PAYMENT = 'payment', 'Payment Notification'
        REVIEW = 'review', 'Review Notification'
        PROMOTIONAL = 'promotional', 'Promotional'
        ALERT = 'alert', 'Alert'
    
    class Channel(models.TextChoices):
        IN_APP = 'in_app', 'In-App'
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'
        PUSH = 'push', 'Push Notification'
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    # Content
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional data for the notification"
    )
    
    # Channel
    channel = models.CharField(
        max_length=20,
        choices=Channel.choices,
        default=Channel.IN_APP
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Action
    action_url = models.URLField(blank=True, null=True)
    action_text = models.CharField(max_length=100, blank=True)
    
    # Metadata
    priority = models.PositiveSmallIntegerField(
        default=1,
        help_text="1=Low, 2=Medium, 3=High, 4=Urgent"
    )
    expiry_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['channel', 'is_sent']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type}: {self.title}"
    
    def mark_as_read(self):
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class NotificationTemplate(BaseModel):
    """Templates for notifications."""
    name = models.CharField(max_length=100, unique=True)
    notification_type = models.CharField(
        max_length=20,
        choices=Notification.NotificationType.choices
    )
    channel = models.CharField(
        max_length=20,
        choices=Notification.Channel.choices
    )
    
    # Templates
    subject = models.CharField(
        max_length=200,
        blank=True,
        help_text="For email notifications"
    )
    message_template = models.TextField(
        help_text="Template with variables like {{user_name}}, {{booking_number}}"
    )
    html_template = models.TextField(
        blank=True,
        help_text="HTML template for email"
    )
    
    # Variables
    variables = models.JSONField(
        default=list,
        blank=True,
        help_text="List of variables used in template"
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
    
    def __str__(self):
        return f"{self.name} ({self.channel})"
    
    def render_message(self, context):
        """Render template with context."""
        message = self.message_template
        for key, value in context.items():
            message = message.replace(f'{{{{{key}}}}}', str(value))
        return message


class UserNotificationPreference(BaseModel):
    """User preferences for notifications."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Channel preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    
    # Notification type preferences
    booking_updates = models.BooleanField(default=True)
    payment_updates = models.BooleanField(default=True)
    review_updates = models.BooleanField(default=True)
    promotional_emails = models.BooleanField(default=False)
    system_alerts = models.BooleanField(default=True)
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(default='22:00:00')
    quiet_hours_end = models.TimeField(default='08:00:00')
    
    # Do Not Disturb
    dnd_until = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'User Notification Preference'
        verbose_name_plural = 'User Notification Preferences'
    
    def __str__(self):
        return f"Preferences - {self.user.email}"
    
    def can_send_notification(self, notification_type, channel):
        """Check if notification can be sent based on preferences."""
        # Check DND
        from django.utils import timezone
        if self.dnd_until and timezone.now() < self.dnd_until:
            return False
        
        # Check channel preference
        channel_field = {
            'email': 'email_notifications',
            'sms': 'sms_notifications',
            'push': 'push_notifications',
            'in_app': 'in_app_notifications',
        }.get(channel)
        
        if not getattr(self, channel_field, False):
            return False
        
        # Check notification type preference
        type_field = {
            'booking': 'booking_updates',
            'payment': 'payment_updates',
            'review': 'review_updates',
            'promotional': 'promotional_emails',
            'system': 'system_alerts',
        }.get(notification_type)
        
        if type_field:
            return getattr(self, type_field, True)
        
        return True


class SMSLog(BaseModel):
    """Log of SMS sent."""
    recipient = models.CharField(max_length=20)
    message = models.TextField()
    template_id = models.CharField(max_length=100, blank=True)
    provider = models.CharField(
        max_length=50,
        choices=[
            ('twilio', 'Twilio'),
            ('msg91', 'MSG91'),
            ('textlocal', 'TextLocal'),
            ('other', 'Other'),
        ]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('failed', 'Failed'),
            ('pending', 'Pending'),
        ]
    )
    provider_message_id = models.CharField(max_length=100, blank=True)
    error_message = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    
    class Meta:
        verbose_name = 'SMS Log'
        verbose_name_plural = 'SMS Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SMS to {self.recipient} - {self.status}"


class EmailLog(BaseModel):
    """Log of emails sent."""
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    template_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('bounced', 'Bounced'),
            ('failed', 'Failed'),
            ('opened', 'Opened'),
            ('clicked', 'Clicked'),
        ]
    )
    provider_message_id = models.CharField(max_length=200, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Email to {self.recipient} - {self.subject}"