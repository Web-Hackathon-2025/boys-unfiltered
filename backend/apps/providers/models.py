from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.common.models import BaseModel, Address
from apps.users.models import User


class ServiceProvider(BaseModel, Address):
    """Service Provider Profile."""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='provider_profile',
        limit_choices_to={'role': 'provider'}
    )
    
    # Business Information
    business_name = models.CharField(max_length=255)
    business_registration_number = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="GSTIN or other registration number"
    )
    business_description = models.TextField()
    business_logo = models.ImageField(
        upload_to='business_logos/', 
        blank=True, 
        null=True
    )
    
    # Professional Information
    years_of_experience = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # FIXED: Use callable defaults for JSONField
    certifications = models.JSONField(
        default=list,  # list is callable
        blank=True,
        help_text="List of certifications with name and year"
    )
    skills = models.JSONField(
        default=list,  # list is callable
        blank=True,
        help_text="List of skills/tags"
    )
    
    # Service Information
    service_categories = models.ManyToManyField(
        'services.ServiceCategory',
        related_name='providers',
        through='ProviderServiceCategory'
    )
    services_offered = models.JSONField(
        default=list,  # list is callable
        blank=True,
        help_text="Detailed list of services offered"
    )
    
    # Availability
    is_available = models.BooleanField(default=True)
    available_from = models.TimeField(default='09:00:00')
    available_to = models.TimeField(default='18:00:00')
    
    # FIXED: Use a callable function for working_days
    def default_working_days():
        return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    
    working_days = models.JSONField(
        default=default_working_days,  # Use callable function
        help_text="Days of week when provider is available"
    )
    emergency_service = models.BooleanField(default=False)
    
    # Ratings and Performance
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.PositiveIntegerField(default=0)
    total_jobs_completed = models.PositiveIntegerField(default=0)
    completion_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    response_time_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Average response time in minutes"
    )
    
    # Verification Status
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    verification_notes = models.TextField(blank=True, null=True)
    
    # Business Metrics
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Default hourly rate"
    )
    min_service_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    
    class Meta:
        verbose_name = 'Service Provider'
        verbose_name_plural = 'Service Providers'
        indexes = [
            models.Index(fields=['city', 'is_available']),
            models.Index(fields=['average_rating']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.business_name}"
    
    @property
    def full_address(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.country} - {self.postal_code}"
    
    def update_rating(self):
        """Update average rating from reviews."""
        from django.apps import apps
        Review = apps.get_model('reviews', 'Review')
        from django.db.models import Avg
        
        reviews = Review.objects.filter(provider=self)
        if reviews.exists():
            self.average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.00
            self.total_reviews = reviews.count()
            self.save(update_fields=['average_rating', 'total_reviews'])


class ProviderServiceCategory(BaseModel):
    """Intermediate model for provider-service category with additional data."""
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    category = models.ForeignKey('services.ServiceCategory', on_delete=models.CASCADE)
    experience_years = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['provider', 'category']
        verbose_name = 'Provider Service Category'
        verbose_name_plural = 'Provider Service Categories'
    
    def __str__(self):
        return f"{self.provider.business_name} - {self.category.name}"


class ProviderDocument(BaseModel):
    """Documents uploaded by service provider for verification."""
    provider = models.ForeignKey(
        ServiceProvider, 
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('id_proof', 'ID Proof (Aadhar/PAN)'),
            ('address_proof', 'Address Proof'),
            ('business_registration', 'Business Registration'),
            ('certification', 'Professional Certification'),
            ('portfolio', 'Portfolio/Work Samples'),
            ('other', 'Other'),
        ]
    )
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='provider_documents/')
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'admin'}
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Provider Document'
        verbose_name_plural = 'Provider Documents'
    
    def __str__(self):
        return f"{self.provider.business_name} - {self.document_name}"


class ProviderAvailability(BaseModel):
    """Detailed availability schedule for providers."""
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Provider Availability'
        verbose_name_plural = 'Provider Availabilities'
        unique_together = ['provider', 'date', 'start_time']
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.provider.business_name} - {self.date} {self.start_time}-{self.end_time}"