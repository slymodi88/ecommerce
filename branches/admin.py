from django.contrib import admin
from branches.models import City, Branch, BranchItem


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    # fields to be displayed in admin panel
    list_display = ('id', 'name',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    # fields to be displayed in admin panel
    list_display = ('id',)


@admin.register(BranchItem)
class BranchItemAdmin(admin.ModelAdmin):
    # fields to be displayed in admin panel
    list_display = ('id', 'item', 'is_available', 'branch',)
