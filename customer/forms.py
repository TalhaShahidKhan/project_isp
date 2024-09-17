from typing import Any
from django.forms.models import ModelForm
from .models import Customer,Package,Area


class CustomerCreateFrom(ModelForm):
    class Meta:
        model = Customer
        fields = ["name","area","package","duration","phone_number","active"]


class CustomerStatusForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["active"]



class PackageForm(ModelForm):
    class Meta:
        model = Package
        fields = ["name","price","speed"]

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ["area_name"]
    


