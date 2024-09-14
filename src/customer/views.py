from typing import Any
from django.urls import reverse_lazy
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer,Area,Package
from .forms import CustomerCreateFrom,CustomerStatusForm,AreaForm,PackageForm
from django.views.generic import TemplateView,CreateView,ListView,DetailView,DeleteView,UpdateView
# Create your views here.



class CustomerListView(ListView,LoginRequiredMixin):
    model=Customer
    template_name = "customer/customer_list.html"
    context_object_name = "cmrs"
    def get_queryset(self) -> QuerySet[Any]:
        customer=Customer.objects.filter(admin=self.request.user)
        return customer
    

class CustomerCreateView(CreateView,LoginRequiredMixin):
    template_name = "customer/customer_create.html"
    model = Customer
    form_class = CustomerCreateFrom
    success_url = reverse_lazy("customer:cmr_list")


    def form_valid(self, form):
        form.instance.admin = self.request.user
        self.object = form.save()
        self.object.set_expairy()
        return super().form_valid(form)
    



class CustomerUpdateView(UpdateView):
    model=Customer
    form_class = CustomerCreateFrom
    template_name="customer/customer_update.html"
    success_url=reverse_lazy("customer:cmr_list")
    def form_valid(self, form):
        updated_duration = form.instance.duration
        customer = self.get_object()
        old_duration = customer.duration
        if updated_duration == old_duration:
            form.instance.duration = old_duration
        self.object.set_expairy()
        return super().form_valid(form)
    



class CustomerDetailsView(DetailView):
    template_name="customer/customer_details.html"
    model=Customer
    context_object_name="cmr"



class CustomerDeleteView(DeleteView):
    model = Customer
    success_url =  reverse_lazy("customer:cmr_list")




class CustomerEnableView(UpdateView):
    model = Customer
    form_class = CustomerStatusForm
    def get_success_url(self):
        # Assuming you want to redirect to the detail view of the updated object
        return reverse_lazy('customer:cmr_det', kwargs={'pk': self.object.pk})
    def form_valid(self, form):
        form.instance.active = True
        return super().form_valid(form)

class CustomerDisableView(UpdateView):
    model = Customer
    form_class  = CustomerStatusForm
    def get_success_url(self):
        # Assuming you want to redirect to the detail view of the updated object
        return reverse_lazy('customer:cmr_det', kwargs={'pk': self.object.pk})
    def form_valid(self, form):
        form.instance.active = False
        return super().form_valid(form)
    




class AddPackage(CreateView):
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy("customer:pkg_list")
    template_name = "package/add_package.html"
    def form_valid(self, form):
        form.instance.pkg_admin = self.request.user
        return super().form_valid(form)
    

class ListPackage(ListView):
    model = Package
    template_name = "package/package_list.html"
    context_object_name = "pkgs"
    def get_queryset(self) -> QuerySet[Any]:
        package=Package.objects.filter(pkg_admin=self.request.user)
        return package

class PackageDetailsView(DetailView):
    model=Package
    template_name="package/package_details.html"
    context_object_name="pkg"


class PackageUpdateView(UpdateView):
    template_name="package/package_update.html"
    model=Package
    form_class=PackageForm
    context_object_name="pkg"
    success_url=reverse_lazy("customer:pkg_list")

class PackageDeleteView(DeleteView):
    model=Package
    success_url=reverse_lazy("customer:pkg_list")







class AreaAddView(CreateView):
    model=Area
    template_name="area/add_area.html"
    form_class=AreaForm
    success_url=reverse_lazy("customer:ar_list")
    def form_valid(self, form):
        form.instance.area_admin = self.request.user
        return super().form_valid(form)


class AreaListView(ListView):
    model=Area
    context_object_name="areas"
    template_name="area/list_area.html"
    def get_queryset(self) -> QuerySet[Any]:
        area=Area.objects.filter(area_admin=self.request.user)
        return area



class AreaUpdateView(UpdateView):
    context_object_name='area'
    template_name="area/update_area.html"
    form_class=AreaForm
    model=Area
    success_url=reverse_lazy("customer:ar_list")


class AreaDeleteView(DeleteView):
    model=Area
    success_url=reverse_lazy("customer:ar_list")