from django.contrib import admin
from .models import CustomerPayment,UserPayment
from unfold.admin import ModelAdmin
# Register your models here.


admin.site.register(CustomerPayment)
admin.site.register(UserPayment)