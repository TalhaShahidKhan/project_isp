from django.contrib import admin
from .models import CustomerPayment,UserPayment
# Register your models here.


admin.site.register(CustomerPayment)
admin.site.register(UserPayment)