from django.contrib import admin
from .models import Category, Listing, ListingImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'user', 'created_at')
    list_filter = ('type', 'status', 'category')
    search_fields = ('title', 'description')

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image')