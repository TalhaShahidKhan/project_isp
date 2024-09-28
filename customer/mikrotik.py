from routeros_api.resource import RouterOsResource
from django.contrib import messages


def get_all_customers(resource: RouterOsResource):
    customers = resource.get()
    return customers


def add_customer_to_mikrotik(resource: RouterOsResource, *args, **kwargs):
    new_customer = resource.add(*args, **kwargs)
    if new_customer:
        return messages.success("Customer Added to Mikrotik")


def update_customer_mik_details(resource: RouterOsResource, user_id, *args, **kwargs):
    upd_customer = resource.set(id=user_id, *args, **kwargs)
    if upd_customer:
        return messages.success("Details updated successfully")


def delete_customer_mikrotik(resource: RouterOsResource, user_id):
    dlt_customer = resource.remove(id=user_id)
    if dlt_customer:
        return messages.success("Customer Deleted successfully")
