from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('digital_wallet', 'Digital Wallet'),
    ]
    
    PAYMENT_GATEWAY_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('razorpay', 'Razorpay'),
        ('square', 'Square'),
        ('manual', 'Manual'),
    ]
    
    # Basic fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    
    # Transaction details
    transaction_id = models.CharField(max_length=100, unique=True)
    external_transaction_id = models.CharField(max_length=200, blank=True, null=True)  # From payment gateway
    
    # Amount and currency
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Status and payment info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_gateway = models.CharField(max_length=20, choices=PAYMENT_GATEWAY_CHOICES, default='manual')
    
    # Payment details
    payment_reference = models.CharField(max_length=200, blank=True, null=True)
    gateway_response = models.JSONField(blank=True, null=True)  # Store gateway response
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Additional info
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['created_at']),
        ]
        
    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.user.email} - {self.amount} {self.currency}"
    
    @property
    def is_successful(self):
        """Check if transaction is successful"""
        return self.status == 'completed'
    
    @property
    def is_pending(self):
        """Check if transaction is pending"""
        return self.status == 'pending'
    
    @property
    def is_failed(self):
        """Check if transaction failed"""
        return self.status in ['failed', 'cancelled']
    
    def mark_as_completed(self):
        """Mark transaction as completed"""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_as_failed(self, reason=None):
        """Mark transaction as failed"""
        self.status = 'failed'
        if reason:
            self.notes = f"Failed: {reason}"
        self.save()
    
    def mark_as_cancelled(self, reason=None):
        """Mark transaction as cancelled"""
        self.status = 'cancelled'
        if reason:
            self.notes = f"Cancelled: {reason}"
        self.save()
    
    def mark_as_refunded(self, reason=None):
        """Mark transaction as refunded"""
        self.status = 'refunded'
        if reason:
            self.notes = f"Refunded: {reason}"
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())
        super().save(*args, **kwargs)