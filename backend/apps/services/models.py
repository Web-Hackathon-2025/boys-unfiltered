from django.db import models
from django.core.validators import MinValueValidator
from apps.common.models import BaseModel


class ServiceCategory(BaseModel):
    """Service Category/Type."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon class name (e.g., 'fa-plumbing', 'fa-bolt')"
    )
    image = models.ImageField(
        upload_to='service_categories/',
        blank=True,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def has_subcategories(self):
        return self.subcategories.exists()


class Service(BaseModel):
    """Service offered by a provider."""
    # Use string reference to avoid circular import
    provider = models.ForeignKey(
        'providers.ServiceProvider',  # STRING REFERENCE
        on_delete=models.CASCADE,
        related_name='services'
    )
    category = models.ForeignKey(
        ServiceCategory,  # Local reference - OK
        on_delete=models.PROTECT,
        related_name='services'
    )
    
    # Service Details
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    
    # Pricing
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    price_unit = models.CharField(
        max_length=50,
        default='per_hour',
        choices=[
            ('per_hour', 'Per Hour'),
            ('per_service', 'Per Service'),
            ('per_sqft', 'Per Square Foot'),
            ('per_item', 'Per Item'),
            ('fixed', 'Fixed Price'),
        ]
    )
    minimum_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    is_price_negotiable = models.BooleanField(default=False)
    
    # Service Metadata
    estimated_duration_minutes = models.PositiveIntegerField(
        default=60,
        help_text="Estimated duration in minutes"
    )
    warranty_months = models.PositiveIntegerField(
        default=0,
        help_text="Service warranty in months"
    )
    requirements = models.JSONField(
        default=list,
        blank=True,
        help_text="List of requirements from customer"
    )
    tools_needed = models.JSONField(
        default=list,
        blank=True,
        help_text="List of tools needed for the service"
    )
    
    # Availability
    is_available = models.BooleanField(default=True)
    available_from = models.TimeField(default='09:00:00')
    available_to = models.TimeField(default='18:00:00')
    
    # Statistics
    total_bookings = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    
    # Media
    images = models.JSONField(
        default=list,
        blank=True,
        help_text="List of image URLs"
    )
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        indexes = [
            models.Index(fields=['provider', 'is_available']),
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['slug']),
            models.Index(fields=['base_price']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        # Use string formatting to avoid accessing provider.business_name at import time
        return f"{self.title}"
    
    def get_provider_name(self):
        """Get provider name without circular import."""
        # This method can be called after the model is fully loaded
        return self.provider.business_name if self.provider_id else ""


class ServicePackage(BaseModel):
    """Package of services offered together."""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='packages'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    included_items = models.JSONField(
        default=list,
        help_text="List of items/services included in package"
    )
    validity_days = models.PositiveIntegerField(
        default=30,
        help_text="Package validity in days"
    )
    
    class Meta:
        verbose_name = 'Service Package'
        verbose_name_plural = 'Service Packages'
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - {self.service.title}"
    
    @property
    def discounted_price(self):
        discount = self.price * (self.discount_percentage / 100)
        return self.price - discount


class ServiceRequest(BaseModel):
    """Customer request for custom service."""
    # Use string reference to avoid circular import
    customer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='service_requests',
        limit_choices_to={'role': 'customer'}
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.JSONField(
        default=dict,
        help_text="Location details including address and coordinates"
    )
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.TimeField(null=True, blank=True)
    budget_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    budget_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('viewed', 'Viewed by Providers'),
            ('quotes_received', 'Quotes Received'),
            ('assigned', 'Assigned to Provider'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    
    images = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['preferred_date']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        # Avoid accessing customer.email at import time
        return f"{self.title}"