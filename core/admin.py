from django.contrib import admin
from .models import Product, SavedOutfit

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'gender', 'occasion', 'brand', 'price', 'trend_score', 'is_active')
    list_filter   = ('category', 'gender', 'occasion', 'is_active')
    search_fields = ('name', 'brand')
    list_editable = ('trend_score', 'is_active')

@admin.register(SavedOutfit)
class SavedOutfitAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender', 'created_at')