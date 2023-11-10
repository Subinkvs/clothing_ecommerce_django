from django.db import models
from accounts.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class MenClothing(models.Model):
    name = models.CharField(max_length=100)
    title = models.TextField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField(null=False,blank=False)
    brand = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='clothing_images')
    is_featured = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class BannerImage(models.Model):
    image = models.ImageField( upload_to='banner-images')
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(MenClothing, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(MenClothing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)