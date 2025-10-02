from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class OrderItem(models.Model):
    """Model for order items - individual items within an order"""
    
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='items')
    motopart = models.ForeignKey('motopart.Motopart', on_delete=models.CASCADE, related_name='order_items')
    
    # Quantity and pricing
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['order', 'motopart']  # One motopart per order
        
    def __str__(self):
        return f"{self.quantity}x {self.motopart.name} in Order {self.order.id}"
    
    def save(self, *args, **kwargs):
        """Calculate total before saving"""
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    @property
    def motopart_name(self):
        return self.motopart.title if self.motopart else "Unknown Motopart"
    
    @property
    def order_id(self):
        return self.order.id if self.order else None
