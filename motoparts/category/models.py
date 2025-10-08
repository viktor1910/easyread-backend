from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"

    @property
    def image_full_url(self):
        """Return full URL for the image"""
        if self.image:
            from django.conf import settings
            return f"{settings.SITE_URL}{self.image.url}" if hasattr(self.image, 'url') else None
        return None