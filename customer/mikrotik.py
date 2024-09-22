import routeros_api
from routeros_api.api import RouterOsApiPool,RouterOsApi
from routeros_api.resource import RouterOsResource
from django.contrib import messages
from django.http import HttpRequest



ppp_route = "/ppp/active"




def add_customer_to_mikrotik(resource:RouterOsResource,request:HttpRequest,*args, **kwargs):
    try:
        new_customer = resource.add(*args, **kwargs)
        if new_customer:
            return messages.success(request,"Customer Added to Mikrotik")
    except Exception as e:
        return messages.error(request,f"{e}")
    

def update_customer_mik_details(resource:RouterOsResource,user_id,request:HttpRequest,*args, **kwargs):
    try:
        upd_customer = resource.set(id=user_id,*args, **kwargs)
        if upd_customer:
            return messages.success(request,"Details updated successfully")
    except Exception as e:
        return messages.error(request,f"{e}")
    


def delete_customer_mikrotik(resource:RouterOsResource,user_id,request:HttpRequest):
    try:
        upd_customer = resource.remove(id=user_id)
        if upd_customer:
            return messages.success(request,"Customer Deleted successfully")
    except Exception as e:
        return messages.error(request,f"{e}")
    


