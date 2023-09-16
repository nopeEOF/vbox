from app.v2ray import v2call
from app.readconfig import get_config
from app.db import dbmanager

myv2client = v2call.MyV2RayClient(client=get_config()["v2rayapi"]["v2ray_engine"])
v2ray = myv2client.connect(
    get_config()["v2rayapi"]["host"], get_config()["v2rayapi"]["port"]
)


def add_vmess_user(email: str):
    user = v2call.VMessUser(email=email)
    # add user in V2Ray

    v2ray.v2_add_vmess_user(user=user)
    # add user in database
    dbmanager.db_add_vmess_user(user=user)


def add_vless_user():
    pass


def add_trojan_user():
    pass


def inactive_user(email: str):
    # inactive user in database
    user = dbmanager.db_update_activity(email=email, active=False)
    if user:
        # remove user from V2Ray
        v2ray.v2_remove_user(email=email)
    else:
        print("user not found" + email)


def active_user(email: str):
    # active user in database
    user = dbmanager.db_update_activity(email=email, active=False)
    if user:
        v2ray.add_user(user=user)
    else:
        print("user not found" + email)


def remove_user(email: str):
    flag = dbmanager.db_remove_user(email=email)
    if flag:
        v2ray.v2_remove_user(email=email)
    else:
        print("user not found" + email)


def update_usage():
    # get all users usage from V2Ray
    v2_users = v2ray.v2_users_usage(pattern="")
    print(v2_users)
