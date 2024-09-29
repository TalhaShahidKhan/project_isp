from django.urls import path
from .views import CreateSubscriptionView,PlanListView,UpdatePlan,bkash_callback_user

urlpatterns = [
    path('',CreateSubscriptionView.as_view(),name="add_sub"),
    path('pay/',bkash_callback_user,name="user_call"),
    path('update/<int:pk>/',UpdatePlan.as_view(),name="upd_sub"),
    path('plans/',PlanListView.as_view(),name="plans"),
    
]


app_name="subscription"