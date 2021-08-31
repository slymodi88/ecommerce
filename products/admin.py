from django.contrib import admin

from products.models import Item, Category


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at',)

    search_fields = ['title', 'description']
    list_filter = ['is_available', 'created_at', 'categories']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
