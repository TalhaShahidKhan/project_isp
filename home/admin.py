from django.contrib import admin
from .models import CustomUser
from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from unfold.admin import ModelAdmin


@admin.register(CustomUser)
class UserAdmin(ModelAdmin):
    pass


admin.site.unregister(EmailAddress)


@admin.register(EmailAddress)
class UserAdmin(EmailAddressAdmin,ModelAdmin):
    pass


