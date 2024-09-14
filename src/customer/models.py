from django.db import models
from django.contrib.auth import get_user_model
from datetime import date,timedelta
# Create your models here.

User = get_user_model()

class Area(models.Model):
    area_name = models.CharField(max_length=220)
    area_admin = models.ForeignKey(User,related_name="areas",on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self) -> str:
        return f'{self.area_name}'


class Package(models.Model):
    pkg_admin = models.ForeignKey(User,related_name="customer_packages",on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=110)
    price = models.IntegerField(blank=True,null=True)
    speed = models.IntegerField(blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.name}"



class Customer(models.Model):
    ONE_MONTH = '1 Month'
    TENTH_OF_NEXT = '10th of the next month'
    duration_choices = [
        (ONE_MONTH,'1 Month'),
        (TENTH_OF_NEXT,'10th of next'),
    ]
    name = models.CharField(max_length=110)
    phone_number = models.CharField(max_length=11,blank=False,null=False)
    admin = models.ForeignKey(User,related_name="customers",on_delete=models.CASCADE)
    area = models.ForeignKey(Area,related_name="customers",on_delete=models.SET_NULL,null=True)
    package = models.ForeignKey(Package,related_name="customers",on_delete=models.SET_NULL,null=True)
    duration = models.CharField(choices=duration_choices,max_length=110)
    expairy = models.DateTimeField(blank=True,null=True)
    active = models.BooleanField(default=False,null=True,blank=True)

    def set_expairy(self):
        if self.duration == self.ONE_MONTH:
            self.expairy = date.today() + timedelta(days=30)
        if self.duration == self.TENTH_OF_NEXT:
            today = date.today()
            # Calculate the first day of the next month
            first_day_next_month = (today.replace(day=1) + timedelta(days=30)).replace(day=1)
            # Set the expiry date to the 10th of the next month
            self.expairy = first_day_next_month.replace(day=10)
    def enable_internet(self):
        self.active = True
    def disable_internet(self):
        self.active = False
    

    def __str__(self) -> str:
        return f"{self.name}-->{self.admin}"
    



