from django.core.exceptions import PermissionDenied
from .models import Subscription
from django.utils import timezone

class NoActiveSubscriptionMixin:
    """
    Mixin to check if the user has no active subscription.
    If an active subscription exists, raise PermissionDenied.
    """

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has an active subscription
        if Subscription.objects.filter(user=request.user, end_date__gt=timezone.now(), is_active=True).exists():
            raise PermissionDenied("You already have an active subscription.")
        return super().dispatch(request, *args, **kwargs)
