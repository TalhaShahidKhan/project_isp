from celery import shared_task

from django.apps import apps

@shared_task
def check_active():
    print("task started")
    Subscription = apps.get_model("subscription","Subscription")
    Subscription.deactivate_expired_subscriptions(Subscription)
    print("task stopped") 
