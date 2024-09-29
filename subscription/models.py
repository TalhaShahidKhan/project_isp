from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from customer.models import Customer,Area,Package
from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Group

User = get_user_model()




class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    customer_limit = models.PositiveIntegerField()
    installation_fee = models.DecimalField(max_digits=10,decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    group = models.OneToOneField(Group, on_delete=models.CASCADE,blank=True,null=True,related_name="plan")


    def save(self, *args, **kwargs):
        # Create a group automatically if it doesn't exist
        if not self.group:
            group, created = Group.objects.get_or_create(name=self.name)
            customer_ct = ContentType.objects.get_for_model(Customer)
            area_ct = ContentType.objects.get_for_model(Area)
            package_ct = ContentType.objects.get_for_model(Package)
            customer_permissions = Permission.objects.filter(content_type=customer_ct)
            area_permissions = Permission.objects.filter(content_type=area_ct)
            package_permissions = Permission.objects.filter(content_type=package_ct)
            group.permissions.set(customer_permissions)
            group.permissions.set(area_permissions)
            group.permissions.set(package_permissions)
            self.group = group

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    @staticmethod
    def deactivate_expired_subscriptions(model):
        expired_subscriptions = model.objects.filter(end_date__lt=timezone.now(), is_active=True)
        for subscription in expired_subscriptions:
            subscription.delete()

    @staticmethod
    def assign_plan_permissions(user, plan):
        user.groups.clear()
        group = plan.group
        user.groups.add(group)
    

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(minutes=self.plan.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.plan}"