from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def home_page(request):
    if request.user.is_authenticated:
        return redirect("home:dashboard")
    return render(request,"home/home.html")
@login_required(login_url='account_login')
def dashboard(request):
    return render(request,"home/dashboard.html")

