from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class OrderItem(models.Model):
    """Model for order items - individual items within an order"""
    
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, related_name='order_items')
    
    # Quantity and pricing
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['order', 'book']  # One book per order
        
    def __str__(self):
        return f"{self.quantity}x {self.book.title} in Order {self.order.id}"
    
    def save(self, *args, **kwargs):
        """Calculate total before saving"""
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    @property
    def book_title(self):
        return self.book.title if self.book else "Unknown Book"
    
    @property
    def order_id(self):
        return self.order.id if self.order else None
