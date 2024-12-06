from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer, Area, Package
from .forms import CustomerCreateFrom, CustomerStatusForm, AreaForm, PackageForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
from django.contrib import messages
from .mixins import SubscriptionRequiredMixin
from routeros_api import RouterOsApiPool
from .mikrotik import get_all_users_from_mikrotik


# Create your views here.


class CustomerListView(LoginRequiredMixin,SubscriptionRequiredMixin, ListView):
    model = Customer
    template_name = "customer/customer_list.html"
    context_object_name = "cmrs"

    def get_queryset(self) -> QuerySet[Any]:
        customer = Customer.objects.filter(admin=self.request.user)
        return customer


class CustomerCreateView(LoginRequiredMixin,SubscriptionRequiredMixin, CreateView):
    template_name = "customer/customer_create.html"
    model = Customer
    form_class = CustomerCreateFrom
    success_url = reverse_lazy("customer:cmr_list")


    def form_valid(self, form):
        try:
            user = self.request.user
            form.instance.admin = user
            if user.customers.count() >= user.subscription.plan.customer_limit:
                form.add_error(
                    None,
                    f"You have reached your limit of {user.subscription.plan.customer_limit} customers.",
                )
                return self.form_invalid(form)
            self.object=form.save(commit=False)
            self.object.add_to_mik()
            messages.success(self.request, "Customer added successfully.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request,"There is an error in API. Please Try again letter or contact Developer.")
            return redirect("customer:cmr_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["admin"] = self.request.user  # Pass the logged-in admin to the form
        return kwargs


class CustomerUpdateView(LoginRequiredMixin,SubscriptionRequiredMixin, UpdateView):
    model = Customer
    fields =  ["name","password","area","package","duration","phone_number"]
    template_name = "customer/customer_update.html"
    success_url = reverse_lazy("customer:cmr_list")

    def form_valid(self, form):
        try:
            updated_duration = form.instance.duration
            customer = self.get_object()
            old_duration = customer.duration
            if updated_duration == old_duration:
                form.instance.duration = old_duration
            self.object.set_expairy()
            response = super().form_valid(form) 
            self.object.update_in_mik()
            messages.success(self.request,"Customer Added Successfully")
            return response
        except Exception as e:
            messages.error(self.request,"There is an error in API. Please Try again letter or contact Developer.")
            return redirect("customer:cmr_list")



class CustomerDetailsView(LoginRequiredMixin,SubscriptionRequiredMixin, DetailView):
    template_name = "customer/customer_details.html"
    model = Customer
    context_object_name = "cmr"


class CustomerDeleteView(LoginRequiredMixin,SubscriptionRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy("customer:cmr_list")

    def form_valid(self, form):
        try:
            instance = self.object
            instance.remove_from_mik()
            messages.success(self.request,"Customer Deleted")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request,"There is an error in API. Please Try again letter or contact Developer.")
            return redirect("customer:cmr_list")
            
    


class CustomerEnableView(LoginRequiredMixin,SubscriptionRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerStatusForm

    def get_success_url(self):
        # Assuming you want to redirect to the detail view of the updated object
        return reverse_lazy("customer:cmr_det", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        try:
            self.object.enable_internet()
            messages.success(self.request,"Internet Enabled")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request,"There is an error in API. Please Try again letter or contact Developer.")
            return redirect("customer:cmr_list")


class CustomerDisableView(LoginRequiredMixin,SubscriptionRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerStatusForm

    def get_success_url(self):
        # Assuming you want to redirect to the detail view of the updated object
        return reverse_lazy("customer:cmr_det", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        try:
            self.object.disable_internet()
            messages.success(self.request,"Internet Disabled")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request,"There is an error in API. Please Try again letter or contact Developer.")
            return redirect("customer:cmr_list")


class AddPackage(LoginRequiredMixin,SubscriptionRequiredMixin, CreateView):
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy("customer:pkg_list")
    template_name = "package/add_package.html"

    def form_valid(self, form):
        form.instance.pkg_admin = self.request.user
        return super().form_valid(form)


class ListPackage(LoginRequiredMixin,SubscriptionRequiredMixin, ListView):
    model = Package
    template_name = "package/package_list.html"
    context_object_name = "pkgs"

    def get_queryset(self) -> QuerySet[Any]:
        package = Package.objects.filter(pkg_admin=self.request.user)
        return package


class PackageDetailsView(LoginRequiredMixin,SubscriptionRequiredMixin, DetailView):
    model = Package
    template_name = "package/package_details.html"
    context_object_name = "pkg"


class PackageUpdateView(LoginRequiredMixin,SubscriptionRequiredMixin, UpdateView):
    template_name = "package/package_update.html"
    model = Package
    form_class = PackageForm
    context_object_name = "pkg"
    success_url = reverse_lazy("customer:pkg_list")


class PackageDeleteView(LoginRequiredMixin,SubscriptionRequiredMixin, DeleteView):
    model = Package
    success_url = reverse_lazy("customer:pkg_list")


class AreaAddView(LoginRequiredMixin,SubscriptionRequiredMixin, CreateView):
    model = Area
    template_name = "area/add_area.html"
    form_class = AreaForm
    success_url = reverse_lazy("customer:ar_list")

    def form_valid(self, form):
        form.instance.area_admin = self.request.user
        return super().form_valid(form)


class AreaListView(LoginRequiredMixin,SubscriptionRequiredMixin, ListView):
    model = Area
    context_object_name = "areas"
    template_name = "area/list_area.html"

    def get_queryset(self) -> QuerySet[Any]:
        area = Area.objects.filter(area_admin=self.request.user)
        return area


class AreaUpdateView(LoginRequiredMixin,SubscriptionRequiredMixin, UpdateView):
    context_object_name = "area"
    template_name = "area/update_area.html"
    form_class = AreaForm
    model = Area
    success_url = reverse_lazy("customer:ar_list")


class AreaDeleteView(LoginRequiredMixin,SubscriptionRequiredMixin, DeleteView):
    model = Area
    success_url = reverse_lazy("customer:ar_list")


def search_customer(request):
    if request.method == "POST":
        customer = request.POST.get("cname")
        if customer:
            result = Customer.objects.filter(
                name__icontains=customer, admin=request.user
            )
            return render(request, "extra/search_c.html", context={"cmrs": result})
    return render(request, "extra/search_c.html")



def mikrotik_users_list(request):
    try:
        conn = RouterOsApiPool(host=request.user.mikrotik_host,username=request.user.mikrotik_username,password=request.user.mikrotik_password,port=request.user.mikrotik_port,use_ssl=request.user.mikrotik_use_ssl,ssl_verify=request.user.mikrotik_verify_ssl,ssl_verify_hostname=request.user.mikrotik_ssl_verify_hostname,plaintext_login=True)
        users = get_all_users_from_mikrotik(conn=conn)
        customer = []
        for usr in users:
            usr['last_logged_out'] = usr['last-logged-out']
            usr['limit_bytes_in'] = usr['limit-bytes-in']
            usr['limit_bytes_out'] = usr['limit-bytes-out']
            del usr['last-logged-out']
            del usr['limit-bytes-in']
            del usr['limit-bytes-out']
            customer.append(usr)
        context = {
            "customers": customer
        }
        return render(request,'customer/mikrotik_details.html',context=context)
    except Exception as e:
        messages.error(request,f'There are problem with api. Please Check your Mikrotik Details. ERROR:{e}')
        return redirect('customer:cmr_list')