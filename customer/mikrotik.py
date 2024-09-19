import routeros_api
import json
connection = routeros_api.RouterOsApiPool(
    '103.115.242.172',
    username='talha',
    password='123',
    port=8989,
    use_ssl=False,
    ssl_verify=False,
    ssl_verify_hostname=False,
    ssl_context=None,
)
api = connection.get_api()

def mikrotik_all_users(api):
    users_list=api.get_resource('/ip/address')
    return list(users_list.get())

def get_one_mikrotik_user(api,user_id):
    users_list = api.get_resource('/ip/address')
    user = users_list.get(id=user_id)
    return user
def add_mikrotik_user(api,id,*args, **kwargs):
    api.add(id=id,*args, **kwargs)
    added_user = get_one_mikrotik_user(api=api,id=id)
    print("Mikrotik User add Successfull")
    return added_user

def user_enable(api,user_id):
    user = api.get_resource('/ip/address')
    enabled_user=user.set(id=user_id,disabled=False)
    return enabled_user

def user_disable(api,user_id):
    user = api.get_resource('/ip/address')
    disabled_user=user.set(id=user_id,disabled=False)
    return disabled_user