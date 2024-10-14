from typing import Any
from django.forms.models import ModelForm
from .models import Customer,Package,Area


class CustomerCreateFrom(ModelForm):
    class Meta:
        model = Customer
        fields = ["name","password","area","package","duration","phone_number","active"]
    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin',None)  # Get the logged-in admin
        super(CustomerCreateFrom,self).__init__(*args, **kwargs)
        if admin:
            # Filter the area and package fields based on the admin
            self.fields['area'].queryset = Area.objects.filter(area_admin=admin)
            self.fields['package'].queryset = Package.objects.filter(pkg_admin=admin)


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
    


