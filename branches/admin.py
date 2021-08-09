from django.contrib import admin

from branches.models import City, Branch, BranchItem


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(BranchItem)
class BranchItemAdmin(admin.ModelAdmin):
    list_display = ('id',)
