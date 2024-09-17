from django.contrib import admin
from .models import Subscription,SubscriptionPlan
from django.utils import timezone

class SubscriptionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Restrict add permission if user already has an active subscription
        if Subscription.objects.filter(user=request.user, end_date__gt=timezone.now(), is_active=True).exists():
            return False
        return super().has_add_permission(request)

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionPlan)