from celery import shared_task
from django.utils import timezone
from django.apps import apps

@shared_task
def customer_active():
    Customer = apps.get_model("customer","Customer")
    customers = Customer.objects.filter(active=True, expiry__lt=timezone.now())
    for customer in customers:
        customer.active = False
        customer.disable_internet()
        customer.save()
