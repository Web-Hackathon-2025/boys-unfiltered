from django.db import models
from django.core.validators import MinValueValidator
from apps.common.models import BaseModel
from apps.users.models import User  # Keep this import
# REMOVE: from apps.services.models import Service  # This causes circular import

class Booking(BaseModel):
    """Booking/Appointment model."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        ACCEPTED = 'accepted', 'Accepted by Provider'
        REJECTED = 'rejected', 'Rejected by Provider'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        RESCHEDULED = 'rescheduled', 'Rescheduled'
        NO_SHOW = 'no_show', 'No Show'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        EMERGENCY = 'emergency', 'Emergency'
    
    # Relationships
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'customer'}  # FIXED: Use string 'customer'
    )
    provider = models.ForeignKey(
        'providers.ServiceProvider',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    
    # Booking Details
    booking_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Auto-generated booking number"
    )
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    estimated_duration_minutes = models.PositiveIntegerField(
        default=60,
        help_text="Estimated service duration in minutes"
    )
    
    # Location
    service_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    
    # Problem Description
    problem_description = models.TextField()
    customer_notes = models.TextField(blank=True)
    provider_notes = models.TextField(blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    status_changed_at = models.DateTimeField(auto_now=True)
    
    # Pricing
    quoted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    additional_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    
    # Payment
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('partial', 'Partially Paid'),
            ('paid', 'Paid'),
            ('refunded', 'Refunded'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    advance_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    
    # Tracking
    assigned_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    # Metadata
    is_urgent = models.BooleanField(default=False)
    requires_follow_up = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        indexes = [
            models.Index(fields=['booking_number']),
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['provider', 'status']),
            models.Index(fields=['scheduled_date', 'status']),
            models.Index(fields=['status', 'payment_status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-scheduled_date', '-scheduled_time']
    
    def __str__(self):
        return f"Booking #{self.booking_number}"
    
    def save(self, *args, **kwargs):
        if not self.booking_number:
            import datetime
            date_str = datetime.datetime.now().strftime('%y%m%d')
            last_booking = Booking.objects.filter(
                booking_number__startswith=f'BK{date_str}'
            ).order_by('booking_number').last()
            
            if last_booking:
                last_num = int(last_booking.booking_number[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.booking_number = f"BK{date_str}{new_num:04d}"
        
        super().save(*args, **kwargs)
    
    @property
    def total_amount(self):
        base = self.final_price or self.quoted_price
        return base + self.additional_charges - self.discount_amount
    
    @property
    def balance_amount(self):
        return self.total_amount - self.advance_paid
    
    @property
    def is_past_due(self):
        from django.utils import timezone
        if self.scheduled_date and self.status in [self.Status.PENDING, self.Status.CONFIRMED]:
            scheduled_datetime = timezone.make_aware(
                timezone.datetime.combine(self.scheduled_date, self.scheduled_time)
            )
            return timezone.now() > scheduled_datetime
        return False


class BookingStatusHistory(BaseModel):
    """Track status changes of bookings."""
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='status_changes'
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Booking Status History'
        verbose_name_plural = 'Booking Status Histories'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booking.booking_number}: {self.old_status} → {self.new_status}"


class BookingAttachment(BaseModel):
    """Files/Images attached to bookings."""
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file_type = models.CharField(
        max_length=50,
        choices=[
            ('image', 'Image'),
            ('document', 'Document'),
            ('invoice', 'Invoice'),
            ('estimate', 'Estimate'),
            ('other', 'Other'),
        ]
    )
    file = models.FileField(upload_to='booking_attachments/')
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Booking Attachment'
        verbose_name_plural = 'Booking Attachments'
    
    def __str__(self):
        return f"Attachment for {self.booking.booking_number}"