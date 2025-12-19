from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, PaymentRefund, Wallet, WalletTransaction

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user_email', 'booking_number', 'amount', 'payment_method', 
                   'status', 'is_successful', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_gateway', 'created_at')
    search_fields = ('payment_id', 'order_id', 'user__email', 'booking__booking_number')
    readonly_fields = ('payment_id', 'order_id', 'is_successful', 'is_refunded', 
                      'created_at', 'initiated_at', 'completed_at', 'refunded_at')
    raw_id_fields = ('user', 'booking')
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    def user_email(self, obj):
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'
    
    def booking_number(self, obj):
        return obj.booking.booking_number if obj.booking else '-'
    booking_number.short_description = 'Booking'
    
    def amount_display(self, obj):
        return f"₹{obj.amount}"
    amount_display.short_description = 'Amount'
    
    def view_refunds_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:payments_paymentrefund_changelist') + f'?payment__id__exact={obj.id}'
        count = obj.refunds.count()
        return format_html('<a href="{}">Refunds ({})</a>', url, count)
    view_refunds_link.short_description = 'Refunds'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'order_id', 'user', 'booking')
        }),
        ('Amount & Currency', {
            'fields': ('amount', 'currency')
        }),
        ('Payment Method', {
            'fields': ('payment_method', 'payment_gateway')
        }),
        ('Status & Timing', {
            'fields': ('status', 'is_successful', 'is_refunded', 
                      'initiated_at', 'completed_at', 'refunded_at')
        }),
        ('Gateway Details', {
            'fields': ('gateway_response', 'gateway_payment_id')
        }),
        ('Refund Information', {
            'fields': ('refund_amount', 'refund_reason', 'refund_gateway_id', 'view_refunds_link')
        }),
        ('Metadata', {
            'fields': ('description', 'metadata', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_successful', 'mark_as_failed']
    
    def mark_as_successful(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='success', completed_at=timezone.now())
        self.message_user(request, f'{updated} payments marked as successful.')
    mark_as_successful.short_description = "Mark selected payments as successful"
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} payments marked as failed.')
    mark_as_failed.short_description = "Mark selected payments as failed"

@admin.register(PaymentRefund)
class PaymentRefundAdmin(admin.ModelAdmin):
    list_display = ('refund_id', 'payment', 'amount', 'status', 'processed_by', 'processed_at')
    list_filter = ('status', 'processed_at')
    search_fields = ('refund_id', 'payment__payment_id', 'gateway_refund_id')
    readonly_fields = ('refund_id', 'created_at', 'processed_at')
    raw_id_fields = ('payment', 'processed_by')
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status == 'processed' and not obj.processed_at:
            from django.utils import timezone
            obj.processed_at = timezone.now()
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'balance', 'currency', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)
    raw_id_fields = ('user',)
    
    def user_email(self, obj):
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'
    
    def view_transactions_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:payments_wallettransaction_changelist') + f'?wallet__id__exact={obj.id}'
        count = obj.transactions.count()
        return format_html('<a href="{}">Transactions ({})</a>', url, count)
    view_transactions_link.short_description = 'Transactions'

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'wallet_user', 'amount', 'transaction_type', 
                   'balance_before', 'balance_after', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('transaction_id', 'wallet__user__email', 'description')
    readonly_fields = ('transaction_id', 'created_at')
    raw_id_fields = ('wallet', 'reference_payment')
    
    def wallet_user(self, obj):
        return obj.wallet.user.email if obj.wallet and obj.wallet.user else '-'
    wallet_user.short_description = 'User'
    wallet_user.admin_order_field = 'wallet__user__email'