from django.views.generic import ListView,UpdateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription,SubscriptionPlan
from .forms import SubscriptionCreateForm
from .mixins import NoActiveSubscriptionMixin 
from django.shortcuts import redirect,render
from django.urls import reverse_lazy
from payment.bkash_utils import create_token,create_payment,exec_payment
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from payment.models import UserPayment
from datetime import datetime




class CreateSubscriptionView(LoginRequiredMixin, NoActiveSubscriptionMixin, View):
    def get(self, request):
        form = SubscriptionCreateForm()
        return render(request, 'subscriptions/create_subscription.html',context={"form":form})

    def post(self, request):
        try:
            get_token = create_token()
            token = get_token["id_token"]

            print(token)
            form = SubscriptionCreateForm(request.POST)
            if form.is_valid():
                price = form.instance.plan.price
                number = self.request.user.bkash_number
                payment = create_payment(token=str(token),amount=str(price),payer_reference=str(number),minumber="01611663361")
                print(payment)
                if payment['agreementStatus'] == 'Initiated':
                    form.instance.user = self.request.user
                    user = form.instance.user
                    plan = form.instance.plan
                    form.save()
                    Subscription.assign_plan_permissions(user,plan)
                    return redirect(payment['bkashURL'])
        except Exception as e:
            print(e)
            # form.add_error('plan',f"There is an error in API. Please contact developer. {e}")
            return redirect("subs:plans")
        

        

class UpdatePlan(LoginRequiredMixin, View):

    def get(self, request,pk):
        subs = Subscription.objects.get(id=pk)
        form = SubscriptionCreateForm(instance=subs)
        return render(request, 'subscriptions/update.html',context={"form":form})

    def post(self, request,pk):
        sub = Subscription.objects.filter(user=request.user,is_active=True)
        if sub:
            messages.warning(request,"You have already a subscription activated. Please wait until it overs.")
            return redirect("subs:plans")
        try:
            get_token = create_token()
            token = get_token["id_token"]
            # print(token)
            subs = Subscription.objects.get(id=pk)
            form = SubscriptionCreateForm(request.POST,instance=subs)
            if form.is_valid():
                price = form.instance.plan.price
                number = self.request.user.bkash_number
                payment = create_payment(token=str(token),amount=str(price),payer_reference=str(number),minumber="01611663361")
                # print(payment)
                if payment['agreementStatus'] == 'Initiated':
                    form.instance.user = self.request.user
                    user = form.instance.user
                    plan = form.instance.plan
                    form.save()
                    Subscription.assign_plan_permissions(user,plan)
                    return redirect(payment['bkashURL'])
        except Exception as e:
            form.add_error('plan',f"There is an error in API. Please contact developer. {e}")
            return redirect("subs:plans")


class PlanListView(ListView):
    model=SubscriptionPlan
    template_name="plans/list.html"
    context_object_name='plans'




@csrf_exempt
def bkash_callback_user(request):
    if request.method == "GET":
        status = request.GET['status']
        if status == 'cancel':
            sub = Subscription.objects.filter(user=request.user,is_active=True)
            sub.delete()
            messages.error(request,"Payment Canceled")
            return redirect("subs:plans")
        if status == 'failed':
            sub = Subscription.objects.filter(user=request.user,is_active=True)
            sub.delete()
            messages.error(request,"Payment Failed")
            return redirect("subs:plans")
    data = request.POST
    print(data)
    payment_id = data.get('paymentID')
    try:
        get_token = create_token()
        token = get_token["id_token"]
        exe_payment = exec_payment(token,paymentId=payment_id)
        date_string=exe_payment('agreementExecuteTime')
        date_string = date_string.replace(" GMT", "")
        if exe_payment.get('agreementStatus') == 'Completed' :
            spayment=UserPayment.objects.create(user=request.user,payer_reference=exe_payment.get('payerReference'),payment_id=exe_payment.get('paymentID'),trxID=request.POST.get('trxID'),amount=request.POST.get('amount'),payment_exec_time=date_string)
            messages.success(request,"Payment Successful")
            return redirect("subs:plans")
        sub = Subscription.objects.filter(user=request.user,is_active=True)
        sub.delete()
        messages.error(request,"Payment Failed. Please contact Developer")
        return redirect("subs:plans")
    except Exception as e:
        sub = Subscription.objects.filter(user=request.user,is_active=True)
        sub.delete()
        messages.error(request,"Payment Failed. Please contact Developer")
        return redirect("subs:plans")
