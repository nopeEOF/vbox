from v2client import utils
from v2client import V2RayClient
from v2client.enum import VMessSecurityTypes, ProxyTypes
from utils.singlton import Singleton


class VMessUser:
    def __init__(
            self, email: str, inbound_tag: str, level: int = 0, security: VMessSecurityTypes = VMessSecurityTypes.AUTO
    ):
        self.inbound_tag = inbound_tag
        self.email = email
        self.level = level
        self.security = security


class V2Ray(metaclass=Singleton):
    def __init__(self):
        self.client = None

    def v2ray_connect(self, host: str, port: int):
        self.client = V2RayClient(host, port)

    def add_vmess_user(self, vmess_user: VMessUser):
        self.client.add_user(
            inbound_tag=vmess_user.inbound_tag,
            proxy_type=ProxyTypes.VMESS,
            email=vmess_user.email,
            level=vmess_user.level,
            security=vmess_user.security,
            user_id=utils.random_uuid()
        )

    def remove_vmess_user(self, email: str, inbound_tag: str):
        self.client.remove_user(inbound_tag=inbound_tag, email=email)

    def traffic_usage(self, email: str):
        usage = self.client.get_user_usage(email=email)
        print("Download Usage: {0:.3f} G & Upload Usage: {1:.3f} G".format(
            usage.download / 1024 ** 3, usage.upload / 1024 ** 3)
        )

    def reset_user_traffic(self, email: str):
        self.client.get_user_usage(email=email, reset=True)
        return True

    def traffic_all_usage(self, inbound_tag: str):
        pass

    def traffic_all_user(self, inbound_tag: str):
        pass

    def user_list(self, inbound_tag: str):
        print(self.client.query_stats(pattern=""))
