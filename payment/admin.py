from django.contrib import admin
from .models import CustomerPayment,UserPayment
from unfold.admin import ModelAdmin
# Register your models here.


@admin.register(UserPayment)
class UserAdmin(ModelAdmin):
    pass

@admin.register(CustomerPayment)
class UserAdmin(ModelAdmin):
    pass
