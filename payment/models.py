from django.db import models
from customer.models import Customer
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

# Create your models here.





class CustomerPayment(models.Model):
    pay_choice = [
        ("Cash", "Cash"),
        ("Bkash", "Bkash"),
    ]
    customer = models.ForeignKey(
        Customer,
        related_name="payments",
        on_delete=models.CASCADE,
    )
    admin = models.ForeignKey(
        User,
        related_name="customer_payment",
        on_delete=models.CASCADE,
    )
    payment_id = models.CharField(max_length=250,blank=True,null=True)
    trxID = models.CharField(max_length=150,blank=True, null=True)
    payment_exec_time = models.DateTimeField(blank=True,null=True,default=datetime.datetime.now())
    amount = models.CharField(max_length=20,blank=False,null=False)
    payment_type = models.CharField(max_length=20,choices=pay_choice,null=False,blank=False,default="Cash")

class UserPayment(models.Model):
    user = models.ForeignKey(
        User, related_name="payments", blank=True, null=True, on_delete=models.SET_NULL
    )
    payer_reference = models.CharField(max_length=11, blank=False, null=False)
    payment_id = models.CharField(max_length=250)
    trxID = models.CharField(max_length=150,null=True)
    payment_exec_time = models.DateTimeField()
    amount = models.CharField(max_length=20)
