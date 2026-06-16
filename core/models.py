from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    GENDER_CHOICES = [
        ('male',   'Male'),
        ('female', 'Female'),
        ('kids',   'Kids'),
        ('unisex', 'Unisex'),
    ]
    CATEGORY_CHOICES = [
        ('face',  'Eyewear'),
        ('neck',  'Neck & Jewellery'),
        ('chest', 'Tops & Shirts'),
        ('legs',  'Pants & Bottoms'),
        ('feet',  'Shoes & Footwear'),
    ]
    OCCASION_CHOICES = [
        ('casual',   'Casual'),
        ('party',    'Party'),
        ('wedding',  'Wedding'),
        ('gym',      'Gym'),
        ('office',   'Office'),
        ('all',      'All Occasions'),
    ]

    name        = models.CharField(max_length=200)
    category    = models.CharField(max_length=20,  choices=CATEGORY_CHOICES)
    gender      = models.CharField(max_length=10,  choices=GENDER_CHOICES)
    occasion    = models.CharField(max_length=20,  choices=OCCASION_CHOICES, default='all')
    image       = models.ImageField(upload_to='products/')
    overlay_png = models.ImageField(upload_to='overlays/', blank=True, null=True)
    price       = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    brand       = models.CharField(max_length=100, blank=True)
    trend_score = models.IntegerField(default=0)
    trend_label = models.CharField(max_length=50,  blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trend_score']

    def __str__(self):
        return f"{self.name} ({self.gender} - {self.category})"


class SavedOutfit(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outfits')
    name       = models.CharField(max_length=200, default='My Outfit')
    gender     = models.CharField(max_length=10)
    photo_url  = models.CharField(max_length=500)
    result_url = models.CharField(max_length=500, blank=True)
    face_item  = models.CharField(max_length=200, blank=True)
    neck_item  = models.CharField(max_length=200, blank=True)
    chest_item = models.CharField(max_length=200, blank=True)
    legs_item  = models.CharField(max_length=200, blank=True)
    feet_item  = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"