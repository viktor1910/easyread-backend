from django.db import models
from django.conf import settings
from django.db.models import Sum, F, Count

# Create your models here.
class Cart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('checked_out', 'Checked Out'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Cart for {self.user.email}"
    
    @property
    def subtotal(self):
        """Calculate total amount of all items in cart"""
        from cartitem.models import CartItem
        total = CartItem.objects.filter(cart=self).aggregate(
            total=Sum(F('quantity') * F('book__price'))
        )['total']
        return total or 0
    
    @property
    def items_count(self):
        """Count total number of items in cart"""
        from cartitem.models import CartItem
        return CartItem.objects.filter(cart=self).aggregate(count=Sum('quantity'))['count'] or 0
