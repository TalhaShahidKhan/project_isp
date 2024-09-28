from django.urls import path
from .views import CustomerListView,CustomerCreateView,CustomerUpdateView,CustomerDetailsView,CustomerDeleteView,CustomerDisableView,CustomerEnableView,AddPackage,ListPackage,PackageDetailsView,PackageUpdateView,PackageDeleteView,AreaAddView,AreaDeleteView,AreaListView,AreaUpdateView,search_customer,mikrotik_list_users
urlpatterns = [
    path('customer/',CustomerListView.as_view(),name="cmr_list"),
    path('customer/mikrotik',mikrotik_list_users,name="cmr_mlist"),
    path('customer/add/',CustomerCreateView.as_view(),name="cmr_add"),
    path('customer/update/<int:pk>/',CustomerUpdateView.as_view(),name="cmr_upd"),
    path('customer/detail/<int:pk>/',CustomerDetailsView.as_view(),name="cmr_det"),
    path('customer/delete/<int:pk>/',CustomerDeleteView.as_view(),name="cmr_del"),
    path('customer/enable/<int:pk>/',CustomerEnableView.as_view(),name="cmr_enb"),
    path('customer/disable/<int:pk>/',CustomerDisableView.as_view(),name="cmr_dis"),
    path('customer/search/',search_customer,name="cmr_srch"),



    path('package/list/',ListPackage.as_view(),name="pkg_list"),
    path('package/add/',AddPackage.as_view(),name="pkg_add"),
    path('package/detail/<int:pk>/',PackageDetailsView.as_view(),name="pkg_det"),
    path('package/update/<int:pk>/',PackageUpdateView.as_view(),name="pkg_upd"),
    path('package/delete/<int:pk>/',PackageDeleteView.as_view(),name="pkg_dlt"),


    path('area/list/',AreaListView.as_view(),name="ar_list"),
    path('area/add/',AreaAddView.as_view(),name="ar_add"),
    path('area/update/<int:pk>/',AreaUpdateView.as_view(),name="ar_upd"),
    path('area/delete/<int:pk>/',AreaDeleteView.as_view(),name="ar_dlt"),

]


app_name = "customer"