import routeros_api
import routeros_api.resource

def get_all_users_from_mikrotik(conn:routeros_api.RouterOsApiPool):
    api = conn.get_api()
    users = api.get_resource('/ppp/secret')
    return users.get()


def get_single_user(conn:routeros_api.RouterOsApiPool,name):
    api=conn.get_api()
    users=api.get_resource('/ppp/secret')
    user = users.get(name=name)
    return user[0] 





def add_user_to_mikrotik(conn:routeros_api.RouterOsApiPool,pkg,username,password):
    api = conn.get_api()
    users = api.get_resource('/ppp/secret')
    user = users.add(profile=pkg,name=username,password=password,service='pppoe')
    return user



def update_mikrotik_user(conn:routeros_api.RouterOsApiPool,pkg,username,password):
    api = conn.get_api()
    users = api.get_resource('/ppp/secret')
    user = users.set(profile=pkg,name=username,password=password)
    print(user)
    return user
def remove_mikrotik_user(conn:routeros_api.RouterOsApiPool,uid):
    api = conn.get_api()
    users = api.get_resource('/ppp/secret')
    user = users.remove(id=uid)
    return user



def active_user(conn:routeros_api.RouterOsApiPool,uid):
    api = conn.get_api()
    secret_users = api.get_resource('/ppp/secret')
    user = secret_users.get(id=uid)
    if user:
        secret_users.set(id=uid, disabled='false')


def deactivate_user(conn:routeros_api.RouterOsApiPool,uid):
    api = conn.get_api()
    secret_users = api.get_resource('/ppp/secret')
    user = secret_users.get(id=uid)
    if user:
        secret_users.set(id=uid, disabled='true')
    api = conn.get_api()
    active_ppp_users = api.get_resource('/ppp/active')
    active_users = active_ppp_users.get(id=uid)

    if active_users:
        for user in active_users:
            active_ppp_users.remove(id=user['.id'])
            