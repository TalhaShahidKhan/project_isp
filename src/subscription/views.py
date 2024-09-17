from django.views.generic import CreateView,ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription,SubscriptionPlan
from .mixins import NoActiveSubscriptionMixin 
from django.shortcuts import redirect
from django.urls import reverse_lazy



class CreateSubscriptionView(LoginRequiredMixin, NoActiveSubscriptionMixin, CreateView):
    model = Subscription
    template_name = 'subscriptions/create_subscription.html'
    fields = ['plan']
    success_url= reverse_lazy("home:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        user = form.instance.user
        plan = form.instance.plan
        Subscription.assign_plan_permissions(user,plan)
        return super().form_valid(form)

class UpdatePlan(LoginRequiredMixin, UpdateView):
    model = Subscription
    template_name = 'subscriptions/update.html'
    fields = ['plan']
    success_url= reverse_lazy("home:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        user = form.instance.user
        plan = form.instance.plan
        Subscription.assign_plan_permissions(user,plan)
        return super().form_valid(form)


class PlanListView(ListView):
    model=SubscriptionPlan
    template_name="plans/list.html"
    context_object_name='plans'