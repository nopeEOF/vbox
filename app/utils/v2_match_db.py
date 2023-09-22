import json
import datetime
from app.v2ray import v2call
from app.readconfig import get_config
from app.db import dbmanager
from typing import List
from app.db import tables
from app.utils import stats as mystats

myv2client = v2call.MyV2RayClient(client=get_config()["v2rayapi"]["v2ray_engine"])
v2ray = myv2client.connect(
    get_config()["v2rayapi"]["host"], get_config()["v2rayapi"]["port"]
)


def check_user_traffic_usage(user: tables.Users) -> bool:
    if user.traffic == -1:
        return True
    if user.upload + user.download <= user.traffic:
        return True
    else:
        return False


def check_user_datetime(user: tables.Users) -> bool:
    if datetime.datetime.utcnow() <= user.expire:
        return True
    else:
        return False


def create_list_users_usage_update(data: dict) -> List[dict]:
    ls = list()
    for user in data.keys():
        ls.append({"email": user, "download": data[user]["downlink"], "upload": data[user]["uplink"]})
    return ls


async def add_vmess_user(user: mystats.User):
    v2_flag = v2ray.v2_add_vmess_user(vmess_user=user.v2user)
    if v2_flag.flag:
        db_flag = await dbmanager.db_add_vmess_user(user=user)
        print(db_flag.status)
    else:
        print(v2_flag.status)


def add_vless_user():
    pass


def add_trojan_user():
    pass


async def inactive_user(email: str):
    # inactive user in database
    db_flag = await dbmanager.db_update_activity(email=email, active=False)
    if db_flag.flag:
        # remove user from V2Ray
        v2_flag = v2ray.v2_remove_user(email=email)
        print(v2_flag.status)
    else:
        print(db_flag.status)


async def active_user(email: str):
    # active user in database
    db_flag = await dbmanager.db_update_activity(email=email, active=True)
    if db_flag.flag:
        if db_flag.status.protocol == "vmess":
            protocol_detail = json.loads(db_flag.status.protocol_detail)
            user_obj = mystats.VMessUser(
                email=db_flag.status.email,
                level=protocol_detail["level"],
                inbound_tag=protocol_detail["inbound_tag"],
                security=protocol_detail["security"],
                uuid=db_flag.status.uuid
            )
            v2ray.v2_add_vmess_user(vmess_user=user_obj)
            print("user activated")
    else:
        print(db_flag.status)


async def remove_user(email: str):
    db_flag = await dbmanager.db_remove_user(email=email)
    if db_flag.flag:
        v2_flag = v2ray.v2_remove_user(email=email)
        print(v2_flag.status)
    else:
        print(db_flag.status)


def update_usage():
    # get all users usage from V2Ray
    v2_users = v2ray.v2_users_usage(pattern="")
    print(v2_users)


async def user_usage(email: str):
    # get user usage from V2Ray
    v2_flag = v2ray.v2_user_usage(email=email, reset=True)
    # update user usage in database
    if v2_flag.flag:
        db_flag = await dbmanager.db_update_user_usage(
            email=email, upload=v2_flag.status.upload, download=v2_flag.status.download
        )
        if db_flag.flag:
            return db_flag
        else:
            print(db_flag.status)
    else:
        print(v2_flag.status)


async def users_usage():
    v2_users_usage = v2ray.v2_users_usage(pattern="user", reset=True)
    users_dict = v2call.query_response_user_to_obj(v2_users_usage)

    for key in users_dict.keys():
        await dbmanager.db_update_user_usage(
            email=key,
            upload=users_dict[key]["uplink"],
            download=users_dict[key]["downlink"]
        )

    # TODO: user bulk update with increase upload and download value
    # query_users_list = create_list_users_usage_update(users_dict)
    # await dbmanager.db_update_users_usage(query_users_list)


async def read_users_db_add_v2ray():
    db_flag = await dbmanager.get_all_users()
    if db_flag.flag:
        for user in db_flag.status:
            if user.active:
                if user.protocol == "vmess":
                    protocol_detail = json.loads(user.protocol_detail)
                    v2user = mystats.VMessUser(
                        email=user.email,
                        level=protocol_detail["level"],
                        inbound_tag=protocol_detail["inbound_tag"],
                        security=protocol_detail["security"],
                        uuid=user.uuid
                    )
                    user = mystats.User(
                        expireDate=user.expire,
                        traffic=user.traffic,
                        active=user.active,
                        protocol=user.protocol,
                        v2user=v2user
                    )
                    await v2ray.v2_add_vmess_user(user=user)
                elif user.protocol == "vless":
                    pass
                elif user.protocol == "trojan":
                    pass
    else:
        print(db_flag.status)


async def check_activity_users():
    db_flag = await dbmanager.get_all_users()
    if db_flag.flag:
        for user in db_flag.status:
            if user.active:
                if not check_user_datetime(user) or not check_user_traffic_usage(user):
                    await inactive_user(email=user.email)
                    print("checking inactive user")
            else:
                if check_user_datetime(user) and check_user_traffic_usage(user):
                    await active_user(email=user.email)
                    print("checking active user")


async def set_user_usage(email: str,  download: int = 0, upload: int = 0, traffic: int = 0):
    db_flag = await dbmanager.db_set_user_usage(email=email, upload=upload, download=download, traffic=traffic)
    if db_flag.flag:
        print(db_flag.status)
    else:
        print(db_flag.status)
