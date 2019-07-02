from django.db import models
from django.utils.timezone import now
# Create your models here.
class image(models.Model):
    title=models.CharField(max_length=100)
    category=models.CharField(max_length=5000, default=None, null=True, blank=True)
    photographer=models.CharField(max_length=100, default=None, null=True, blank=True)
    share_link=models.CharField(max_length=5000, default=None, null=True, blank=True)
    url=models.CharField(max_length=5000)
    thumbnail_url=models.CharField(max_length=5000, default=None, blank=True, null=True)
    upload_date=models.DateTimeField(auto_now_add=True, blank=True)
    likes=models.CharField(max_length=10, default=None, null=True, blank=True)
    comments=models.CharField(max_length=99999999, default=None, null=True, blank=True)
    tags=models.CharField(max_length=10000, default=None, null=True, blank=True)
    downloads=models.PositiveIntegerField(default=0)

    class Meta:
        ordering=('title',)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('shop:image', args=[self.id])

class Category(models.Model):
    name=models.CharField(max_length=100)

    class Meta:
        ordering=('name',)

    def __str__(self):
        return self.name

class appearance(models.Model):
    background_image_link=models.CharField(max_length=10000, default=None, null=True, blank=True)