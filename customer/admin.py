from django.contrib import admin
from .models import Customer,Package,Area
from unfold.admin import ModelAdmin

# Register your models here.

admin.site.register(Customer)
admin.site.register(Package)
admin.site.register(Area)


