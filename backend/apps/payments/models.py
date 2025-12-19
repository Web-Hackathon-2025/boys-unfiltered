from django.db import models
from django.core.validators import MinValueValidator
from apps.common.models import BaseModel
from apps.users.models import User
# REMOVE: from apps.bookings.models import Booking  # Causes circular import


class Payment(BaseModel):
    """Payment transaction model."""
    
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        UPI = 'upi', 'UPI'
        CARD = 'card', 'Credit/Debit Card'
        NET_BANKING = 'net_banking', 'Net Banking'
        WALLET = 'wallet', 'Wallet'
        EMI = 'emi', 'EMI'
    
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        INITIATED = 'initiated', 'Initiated'
        PROCESSING = 'processing', 'Processing'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'
        PARTIALLY_REFUNDED = 'partially_refunded', 'Partially Refunded'
    
    booking = models.ForeignKey(
        'bookings.Booking',  # STRING REFERENCE
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    
    # Payment Details
    payment_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Payment gateway transaction ID"
    )
    order_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Order/Booking reference ID"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default='INR')
    
    # Payment Method
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.UPI
    )
    payment_gateway = models.CharField(
        max_length=50,
        choices=[
            ('razorpay', 'Razorpay'),
            ('stripe', 'Stripe'),
            ('paypal', 'PayPal'),
            ('paytm', 'Paytm'),
            ('cashfree', 'Cashfree'),
            ('manual', 'Manual'),
        ]
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    
    # Gateway Response
    gateway_response = models.JSONField(
        default=dict,
        blank=True,
        help_text="Raw response from payment gateway"
    )
    gateway_payment_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Payment ID from gateway"
    )
    
    # Timing
    initiated_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    # Refund Information
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    refund_reason = models.TextField(blank=True)
    refund_gateway_id = models.CharField(max_length=100, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        indexes = [
            models.Index(fields=['payment_id']),
            models.Index(fields=['order_id']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['booking']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.payment_id} - ₹{self.amount} ({self.status})"
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            import datetime
            import uuid
            date_str = datetime.datetime.now().strftime('%y%m%d')
            unique_id = str(uuid.uuid4())[:8]
            self.payment_id = f"PAY{date_str}{unique_id}"
        
        if not self.order_id and self.booking_id:
            # Use get_model to avoid circular import
            from django.apps import apps
            Booking = apps.get_model('bookings', 'Booking')
            try:
                booking = Booking.objects.get(id=self.booking_id)
                self.order_id = booking.booking_number
            except Booking.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
    
    @property
    def is_successful(self):
        return self.status == self.PaymentStatus.SUCCESS
    
    @property
    def is_refunded(self):
        return self.status in [self.PaymentStatus.REFUNDED, self.PaymentStatus.PARTIALLY_REFUNDED]


class PaymentRefund(BaseModel):
    """Refund details for payments."""
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='refunds'
    )
    refund_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    gateway_refund_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role__in': ['admin', 'provider']}  # FIXED: Use string list
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Payment Refund'
        verbose_name_plural = 'Payment Refunds'
    
    def __str__(self):
        return f"Refund {self.refund_id} - ₹{self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.refund_id:
            import datetime
            import uuid
            date_str = datetime.datetime.now().strftime('%y%m%d')
            unique_id = str(uuid.uuid4())[:8]
            self.refund_id = f"REF{date_str}{unique_id}"
        super().save(*args, **kwargs)


class Wallet(BaseModel):
    """User wallet for holding credits."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default='INR')
    
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
    
    def __str__(self):
        return f"Wallet #{self.id}"
    
    def can_withdraw(self, amount):
        return self.balance >= amount
    
    def deposit(self, amount, reason="Deposit"):
        """Add amount to wallet."""
        from .models import WalletTransaction
        self.balance += amount
        self.save()
        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type='credit',
            balance_after=self.balance,
            description=reason
        )
    
    def withdraw(self, amount, reason="Withdrawal"):
        """Withdraw amount from wallet."""
        from .models import WalletTransaction
        if not self.can_withdraw(amount):
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.save()
        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type='debit',
            balance_after=self.balance,
            description=reason
        )


class WalletTransaction(BaseModel):
    """Transaction history for wallet."""
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('credit', 'Credit'),
            ('debit', 'Debit'),
        ]
    )
    balance_before = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    balance_after = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField()
    reference_payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wallet_transactions'
    )
    
    class Meta:
        verbose_name = 'Wallet Transaction'
        verbose_name_plural = 'Wallet Transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Wallet Tx {self.transaction_id}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            import datetime
            import uuid
            date_str = datetime.datetime.now().strftime('%y%m%d')
            unique_id = str(uuid.uuid4())[:8]
            self.transaction_id = f"WLT{date_str}{unique_id}"
        super().save(*args, **kwargs)