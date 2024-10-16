from django.urls import path
from .views import home_page,dashboard,UserProfileView,UpdateProfileView,AddMikrotikView,contact

urlpatterns = [
    path('',home_page,name="home"),
    path('dashboard/',dashboard,name="dashboard"),
    path('contact/',contact,name="contact"),
    path('profile/<str:slug>/',UserProfileView.as_view(),name="profile"),
    path('profile/update/<str:slug>/',UpdateProfileView.as_view(),name="profile_upd"),
    path('profile/mikrotik/<str:slug>/',AddMikrotikView.as_view(),name="profile_add_mik"),
]

app_name = "home"
