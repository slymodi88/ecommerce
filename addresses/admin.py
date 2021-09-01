from django.contrib import admin

from addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    # fields to be displayed in admin panel
    list_display = ('id', 'address_info', 'title',)
