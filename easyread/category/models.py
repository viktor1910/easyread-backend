from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name