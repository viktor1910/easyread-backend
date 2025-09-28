from django.db import models
from category.models import Category

# Create your models here.
class Book(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('out_of_stock', 'Out of Stock'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.FloatField()
    discount = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    published_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    @property
    def discounted_price(self):
        """Calculate the price after discount"""
        if self.discount > 0:
            return self.price - (self.price * self.discount / 100)
        return self.price
    
    @property
    def is_available(self):
        """Check if book is available for purchase"""
        return self.status == 'active' and self.stock > 0
