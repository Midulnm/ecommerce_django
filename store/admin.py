from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_active']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
