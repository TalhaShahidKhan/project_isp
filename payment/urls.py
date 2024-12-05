from django.urls import path
from .views import customer_payment,customer_payment_execution
urlpatterns = [
    path('bill/',customer_payment,name="bill"),
    path('customer/',customer_payment_execution,name="customer_callback"),
]


app_name = "payment"