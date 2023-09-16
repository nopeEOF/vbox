from v2client import utils
from v2client import V2RayClient
from v2client.enum import VMessSecurityTypes, ProxyTypes
from v2client.v2ray import stats
from app.singlton import Singleton
from app.readconfig import get_config


class VMessUser:
    def __init__(
            self,
            email: str,
            inbound_tag: str = get_config()["v2rayapi"]["inbound_tag"],
            level: int = 0,
            security: VMessSecurityTypes = VMessSecurityTypes.AUTO,
            uuid: str = utils.random_uuid()
    ):
        self.inbound_tag = inbound_tag
        self.email = email
        self.level = level
        self.security = security
        self.proxyType = ProxyTypes.VMESS
        self.userUuid = uuid


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

    def v2_add_vmess_user(self, vmess_user: VMessUser) -> None:
        self.client.add_user(
            inbound_tag=vmess_user.inbound_tag,
            proxy_type=vmess_user.proxyType,
            email=vmess_user.email,
            level=vmess_user.level,
            security=vmess_user.security,
            user_id=vmess_user.userUuid
        )

    def v2_remove_user(self, email: str, inbound_tag: str = get_config()["v2rayapi"]["inbound_tag"]) -> None:
        self.client.remove_user(inbound_tag=inbound_tag, email=email)

    def v2_user_usage(self, email: str, reset: bool) -> stats.UsageResponse:
        return self.client.get_user_usage(email=email, reset=reset)

    def v2_users_usage(self, pattern: str = "") -> stats.QueryListResponse:
        return self.client.query_stats(pattern=pattern)


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
