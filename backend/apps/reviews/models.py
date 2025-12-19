from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.common.models import BaseModel
from apps.users.models import User
# Use string references to avoid circular imports
# REMOVE: from apps.providers.models import ServiceProvider
# REMOVE: from apps.bookings.models import Booking


class Review(BaseModel):
    """Review/Rating model."""
    booking = models.OneToOneField(
        'bookings.Booking',  # STRING REFERENCE
        on_delete=models.CASCADE,
        related_name='review',
        unique=True
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_given',
        limit_choices_to={'role': 'customer'}  # FIXED: Use string 'customer'
    )
    provider = models.ForeignKey(
        'providers.ServiceProvider',  # STRING REFERENCE
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    # Ratings (1-5)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    
    # Detailed Ratings
    punctuality_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    professionalism_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    quality_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    communication_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    
    # Review Content
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    response = models.TextField(blank=True, help_text="Provider's response to review")
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    is_verified = models.BooleanField(default=True, help_text="Verified booking")
    is_featured = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    
    # Moderation
    is_approved = models.BooleanField(default=True)
    moderated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'admin'}  # FIXED: Use string 'admin'
    )
    moderated_at = models.DateTimeField(null=True, blank=True)
    moderation_notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        indexes = [
            models.Index(fields=['provider', 'rating']),
            models.Index(fields=['customer']),
            models.Index(fields=['is_approved']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review #{self.id}"
    
    @property
    def average_detailed_rating(self):
        ratings = [
            self.punctuality_rating,
            self.professionalism_rating,
            self.quality_rating,
            self.communication_rating,
        ]
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        return self.rating


class ReviewImage(BaseModel):
    """Images attached to reviews."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='review_images/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Review Image'
        verbose_name_plural = 'Review Images'
        ordering = ['display_order']
    
    def __str__(self):
        return f"Image for review #{self.review.id}"


class ReviewHelpful(BaseModel):
    """Track helpful votes on reviews."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='helpful_votes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='helpful_votes'
    )
    is_helpful = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Review Helpful Vote'
        verbose_name_plural = 'Review Helpful Votes'
        unique_together = ['review', 'user']
    
    def __str__(self):
        return f"Helpful vote #{self.id}"


class ProviderReport(BaseModel):
    """Report/Complaint against a provider."""
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports_made',
        limit_choices_to={'role': 'customer'}  # FIXED: Use string 'customer'
    )
    provider = models.ForeignKey(
        'providers.ServiceProvider',  # STRING REFERENCE
        on_delete=models.CASCADE,
        related_name='reports'
    )
    booking = models.ForeignKey(
        'bookings.Booking',  # STRING REFERENCE
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports'
    )
    
    report_type = models.CharField(
        max_length=50,
        choices=[
            ('unprofessional', 'Unprofessional Behavior'),
            ('poor_service', 'Poor Service Quality'),
            ('safety_concern', 'Safety Concern'),
            ('overcharging', 'Overcharging'),
            ('no_show', 'No Show'),
            ('other', 'Other'),
        ]
    )
    description = models.TextField()
    evidence = models.JSONField(
        default=list,
        blank=True,
        help_text="List of evidence (images, documents)"
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('investigating', 'Under Investigation'),
            ('resolved', 'Resolved'),
            ('dismissed', 'Dismissed'),
        ],
        default='pending'
    )
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'admin'}  # FIXED: Use string 'admin'
    )
    resolution = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Provider Report'
        verbose_name_plural = 'Provider Reports'
        indexes = [
            models.Index(fields=['provider', 'status']),
            models.Index(fields=['reporter']),
        ]
    
    def __str__(self):
        return f"Report #{self.id}"