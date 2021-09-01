from django.contrib import admin

from carts.models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # fields to be displayed in admin panel
    list_display = ("id",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    # fields to be displayed in admin panel
    list_display = ("id", "cart", 'item',)
