from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView,View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from subscription.models import SubscriptionPlan
from django.contrib import messages
# Create your views here.

User = get_user_model()


def home_page(request):
    if request.user.is_authenticated:
        return redirect("home:dashboard")
    plans = SubscriptionPlan.objects.all()
    context = {
        'plans':plans
    }
    return render(request, "home/home.html",context=context)


@login_required(login_url="account_login")
def dashboard(request):
    return render(request, "home/dashboard.html")

def contact(request):
    return render(request, "home/contact.html")


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "home/profile.html"
    context_object_name = "user"
    slug_field = "username"


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name","bkash_number","mikrotik_host", "mikrotik_username", "mikrotik_password", "mikrotik_port", "mikrotik_use_ssl", "mikrotik_verify_ssl", "mikrotik_ssl_verify_hostname"]
    slug_field = "username"
    template_name = "home/update_profile.html"

    def get_success_url(self) -> str:
        return reverse_lazy("home:profile", kwargs={"slug": self.object.username})


class AddMikrotikView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["mikrotik_host", "mikrotik_username", "mikrotik_password", "mikrotik_port", "mikrotik_use_ssl", "mikrotik_verify_ssl", "mikrotik_ssl_verify_hostname"]
    slug_field = "username"
    template_name = "home/add_mikrotik.html"
    def get_success_url(self) -> str:
        return reverse_lazy("home:profile",kwargs={"slug":self.object.username})

