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

from .mikrotik import get_all_customers
import routeros_api


# Create your views here.


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "customer/customer_list.html"
    context_object_name = "cmrs"

    def get_queryset(self) -> QuerySet[Any]:
        customer = Customer.objects.filter(admin=self.request.user)
        return customer


class CustomerCreateView(LoginRequiredMixin, CreateView):
    template_name = "customer/customer_create.html"
    model = Customer
    form_class = CustomerCreateFrom
    success_url = reverse_lazy("customer:cmr_list")

    def form_valid(self, form):
        user = self.request.user
        form.instance.admin = user
        if user.customers.count() >= user.subscription.plan.customer_limit:
            form.add_error(
                None,
                f"You have reached your limit of {user.subscription.plan.customer_limit} customers.",
            )
            return self.form_invalid(form)
        messages.success(self.request, "Customer added successfully.")
        self.object = form.save()
        self.object.set_expairy()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["admin"] = self.request.user  # Pass the logged-in admin to the form
        return kwargs


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerCreateFrom
    template_name = "customer/customer_update.html"
    success_url = reverse_lazy("customer:cmr_list")

    def form_valid(self, form):
        updated_duration = form.instance.duration
        customer = self.get_object()
        old_duration = customer.duration
        if updated_duration == old_duration:
            form.instance.duration = old_duration
        self.object.set_expairy()
        if form.instance.active == True:
            self.object.enable_internet()
        elif form.instance.active == False:
            self.object.disable_internet()
        return super().form_valid(form)


class CustomerDetailsView(LoginRequiredMixin, DetailView):
    template_name = "customer/customer_details.html"
    model = Customer
    context_object_name = "cmr"


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy("customer:cmr_list")


class CustomerEnableView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerStatusForm

    def get_success_url(self):
        # Assuming you want to redirect to the detail view of the updated object
        return reverse_lazy("customer:cmr_det", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        self.object.enable_internet()
        return super().form_valid(form)


class CustomerDisableView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerStatusForm

    def get_success_url(self):
        # Assuming you want to redirect to the detail view of the updated object
        return reverse_lazy("customer:cmr_det", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        self.object.disable_internet()
        return super().form_valid(form)


class AddPackage(LoginRequiredMixin, CreateView):
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy("customer:pkg_list")
    template_name = "package/add_package.html"

    def form_valid(self, form):
        form.instance.pkg_admin = self.request.user
        return super().form_valid(form)


class ListPackage(LoginRequiredMixin, ListView):
    model = Package
    template_name = "package/package_list.html"
    context_object_name = "pkgs"

    def get_queryset(self) -> QuerySet[Any]:
        package = Package.objects.filter(pkg_admin=self.request.user)
        return package


class PackageDetailsView(LoginRequiredMixin, DetailView):
    model = Package
    template_name = "package/package_details.html"
    context_object_name = "pkg"


class PackageUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "package/package_update.html"
    model = Package
    form_class = PackageForm
    context_object_name = "pkg"
    success_url = reverse_lazy("customer:pkg_list")


class PackageDeleteView(LoginRequiredMixin, DeleteView):
    model = Package
    success_url = reverse_lazy("customer:pkg_list")


class AreaAddView(LoginRequiredMixin, CreateView):
    model = Area
    template_name = "area/add_area.html"
    form_class = AreaForm
    success_url = reverse_lazy("customer:ar_list")

    def form_valid(self, form):
        form.instance.area_admin = self.request.user
        return super().form_valid(form)


class AreaListView(LoginRequiredMixin, ListView):
    model = Area
    context_object_name = "areas"
    template_name = "area/list_area.html"

    def get_queryset(self) -> QuerySet[Any]:
        area = Area.objects.filter(area_admin=self.request.user)
        return area


class AreaUpdateView(LoginRequiredMixin, UpdateView):
    context_object_name = "area"
    template_name = "area/update_area.html"
    form_class = AreaForm
    model = Area
    success_url = reverse_lazy("customer:ar_list")


class AreaDeleteView(LoginRequiredMixin, DeleteView):
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


def mikrotik_list_users(request):
    ppp_route = "/ppp/active"
    try:
        api = routeros_api.connect(
            host=request.user.mikrotik_host,
            port=request.user.mikrotik_port,
            username=request.user.mikrotik_username,
            password=request.user.mikrotik_password,
            plaintext_login=True,
            use_ssl=request.user.mikrotik_use_ssl,
            ssl_verify=request.user.mikrotik_verify_ssl,
            ssl_verify_hostname=request.user.mikrotik_ssl_verify_hostname,
        )
        resource = api.get_resource(ppp_route)
        customers = []
        for i in get_all_customers(resource=resource):
            i["caller_id"] = i["caller-id"]
            i["limit_bytes_in"] = i["limit-bytes-in"]
            i["limit_bytes_out"] = i["limit-bytes-out"]
            i["session_id"] = i["session-id"]
            del i["caller-id"]
            del i["limit-bytes-in"]
            del i["limit-bytes-out"]
            del i["session-id"]
            customers.append(i)
        context = {"customers": customers}
        return render(request, "customer/mikrotik_details.html", context=context)
    except Exception as e:
        messages.error(
            request,
            "There is a problem with mikrotik server. Please Check your mikrotik details first.",
        )
        return redirect("customer:cmr_list")
