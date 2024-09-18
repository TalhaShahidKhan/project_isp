from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Group

User = get_user_model()




class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    customer_limit = models.PositiveIntegerField(max_length=10)
    installation_fee = models.DecimalField(max_digits=10,decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    group = models.OneToOneField(Group, on_delete=models.CASCADE,blank=True,null=True,related_name="plan")


    def save(self, *args, **kwargs):
        # Create a group automatically if it doesn't exist
        if not self.group:
            group, created = Group.objects.get_or_create(name=self.name)
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
            subscription.is_active = False
            subscription.save()

    @staticmethod
    def assign_plan_permissions(user, plan):
        # Remove user from previous group (if any)
        user.groups.clear()

        # Assign the user to the new group based on their plan
        group = plan.group
        user.groups.add(group)
    

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(minutes=self.plan.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.plan}"