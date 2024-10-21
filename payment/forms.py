from django.forms import ModelForm
from .models import CustomerPayment


class InvoiceForm(ModelForm):
    class Meta:
        model = CustomerPayment
        fields = ["payment_type", "amount"]