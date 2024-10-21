from django.contrib import admin
from .models import Customer,Package,Area
from unfold.admin import ModelAdmin

@admin.register(Customer)
class UserAdmin(ModelAdmin):
    pass



@admin.register(Area)
class UserAdmin(ModelAdmin):
    pass


@admin.register(Package)
class UserAdmin(ModelAdmin):
    pass


