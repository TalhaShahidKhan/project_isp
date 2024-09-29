from django.db import models
from customer.models import Customer
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.


{
    "statusCode": "0000",
    "statusMessage": "Successful",
    "paymentID": "TR0011ON1565154754797",
    "payerReference": "01770618575",
    "customerMsisdn": "01770618575",
    "trxID": "6H7801QFYM",
    "amount": "15",
    "transactionStatus": "Completed",
    "paymentExecuteTime": "2019-08-07T11:15:56:336 GMT+0600",
    "currency": "BDT",
    "intent": "sale",
    "merchantInvoiceNumber": "MER1231",
}


class CustomerPayment(models.Model):
    customer = models.ForeignKey(
        Customer,
        related_name="payments",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    payment_id = models.CharField(max_length=250)
    trxID = models.CharField(max_length=150)
    payment_exec_time = models.DateTimeField()
    amount = models.CharField(max_length=20)


class UserPayment(models.Model):
    user = models.ForeignKey(
        User, related_name="payments", blank=True, null=True, on_delete=models.SET_NULL
    )
    payer_reference = models.CharField(max_length=11, blank=False, null=False)
    payment_id = models.CharField(max_length=250)
    trxID = models.CharField(max_length=150)
    payment_exec_time = models.DateTimeField()
    amount = models.CharField(max_length=20)
