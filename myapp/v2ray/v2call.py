from v2client import V2RayClient
from v2client.v2ray import stats
from v2client.exceptions import UserNotFound, UserAlreadyExists
from myapp.singlton import Singleton
from myapp.readconfig import get_config
from myapp.utils import stats as mystats


def query_response_user_to_obj(query_list_response: stats.QueryListResponse):
    user_usage_dict = dict()
    for response in query_list_response.stats:
        name = response.name.split(">>>")
        if name[1] in user_usage_dict.keys():
            user_usage_dict[f"{name[1]}"].update({f"{name[3]}": response.value})
        else:
            user_usage_dict[f"{name[1]}"] = {f"{name[3]}": response.value}
    return user_usage_dict


class V2Ray:

    def __init__(self):
        pass

    def v2_add_vmess_user(self, *args, **kwargs):
        pass

    def v2_add_vless_user(self, *args, **kwargs):
        pass

    def v2_remove_user(self, *args, **kwargs):
        pass

    def v2_users_usage(self, *args, **kwargs):
        pass

    def v2_user_usage(self, *args, **kwargs):
        pass

    def v2_inbound_usage(self, *args, **kwargs):
        pass


class V2Fly(V2Ray):

    def __init__(self, host: str, port: int):
        super().__init__()
        self.client = self.__v2ray_connect(host, port)

    @staticmethod
    def __v2ray_connect(host: str, port: int):
        return V2RayClient(host, port)

    def v2_add_vmess_user(self, vmess_user: mystats.VMessUser) -> mystats.Detail:
        try:
            self.client.add_user(
                inbound_tag=vmess_user.inbound_tag,
                proxy_type=vmess_user.proxyType,
                email=vmess_user.email,
                level=vmess_user.level,
                security=vmess_user.security,
                user_id=vmess_user.userUuid
            )
            return mystats.Detail(flag=True, status="user added in v2ray")
        except UserAlreadyExists:
            return mystats.Detail(flag=False, status="user already exists")

    def v2_remove_user(self, email: str, inbound_tag: str = get_config()["v2rayapi"]["inbound_tag"]) -> mystats.Detail:
        try:
            self.client.remove_user(inbound_tag=inbound_tag, email=email)
            return mystats.Detail(flag=True, status="user removed is v2ray")
        except UserNotFound:
            return mystats.Detail(flag=False, status="user not found")

    def v2_user_usage(self, email: str, reset: bool) -> mystats.Detail:
        try:
            user = self.client.get_user_usage(email=email, reset=reset)
            return mystats.Detail(flag=True, status=user)
        except UserNotFound:
            return mystats.Detail(flag=False, status="user usage not found. maybe up and down link is empty")

    def v2_users_usage(self, pattern: str = "", reset: bool = False) -> stats.QueryListResponse:
        return self.client.query_stats(pattern=pattern, reset=reset)


class XRay(V2Ray):
    def __init__(self, host: str, port: int):
        """coming soon"""

        super().__init__()


class MyV2RayClient(metaclass=Singleton):
    def __init__(self, client: str):
        self.client = client

    def connect(self, host: str, port: int):
        if self.client == "xray":
            return self.xray()
        elif self.client == "v2fly":
            return self.v2fly(host=host, port=port)

    @staticmethod
    def xray():
        return None  # coming soon

    @staticmethod
    def v2fly(host: str, port: int) -> V2Fly:
        return V2Fly(host=host, port=port)
