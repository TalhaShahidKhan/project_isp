import routeros_api

def get_all_users_from_mikrotik(conn:routeros_api.RouterOsApiPool):
    api = conn.get_api()
    users = api.get_resource('/ppp/secret')
    return users.get()


def add_user_to_mikrotik(conn:routeros_api.RouterOsApiPool,pkg,username,password):
    api = conn.get_api()
    users = api.get_resource('/ppp/secret')
    user = users.add(profile=pkg,name=username,password=password,service='pppoe')
    print(user)
    return user



def update_mikrotik_user(conn:routeros_api.RouterOsApiPool,pkg,username,password):
    api = conn.get_api()
    users = api.get_resource('/ppp/secret')
    user = users.set(profile=pkg,name=username,password=password)
    print(user)
    return user
def remove_mikrotik_user(conn:routeros_api.RouterOsApiPool,username,password):
    api = conn.get_api()
    users = api.get_resource('/ppp/secret')
    user = users.remove(name=username,password=password)
    print(user)
    return user



def active_user(conn:routeros_api.RouterOsApiPool,uid,username):
    api = conn.get_api()
    users = api.get_resource('/ppp/active')
    user = users.add(name=username,id=uid)
    print(user)
    return user


def deactivate_user(conn:routeros_api.RouterOsApiPool,uid,username):
    api = conn.get_api()
    users = api.get_resource('/ppp/active')
    user = users.remove(name=username,id=uid)
    print(user)
    return user