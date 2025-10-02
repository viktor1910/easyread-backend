from django.db import models

# Create your models here.
class CartItem(models.Model):
    cart = models.ForeignKey('carts.Cart', on_delete=models.CASCADE, related_name='items')
    motopart = models.ForeignKey('motopart.Motopart', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    # price = models.FloatField(null=True, blank=True)  # Uncomment if migration has price column
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cart', 'motopart')  # Prevent duplicate items in same cart
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.motopart.name} x {self.quantity}"
    
    @property
    def unit_price(self):
        """Get the current price of the motopart"""
        return self.motopart.discounted_price
    
    @property
    def total(self):
        """Calculate total price for this cart item"""
        return self.unit_price * self.quantity
    
    def save(self, *args, **kwargs):
        """Override save to ensure quantity is valid"""
        if self.quantity <= 0:
            self.quantity = 1
        super().save(*args, **kwargs)
