from v2client import utils
from v2client import V2RayClient
from v2client import enum as v2types
from utils.singlton import Singleton


class VMessUser:
    def __init__(self, email: str, inbound_tag: str):
        self.inbound_tag = inbound_tag
        self.email = email
        self.proxy_type = v2types.ProxyTypes.VMESS,
        self.level = 0,
        self.security = v2types.VMessSecurityTypes.AUTO,
        self.user_id = utils.random_uuid()


class V2Ray(metaclass=Singleton):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = None

    def v2ray_connect(self,):
        self.client = V2RayClient(self.host, self.port)

    def add_vmess_user(self, vmess_user: VMessUser):
        self.client.add_user(
            inbound_tag=vmess_user.inbound_tag,
            proxy_type=vmess_user.proxy_type,
            email=vmess_user.email,
            level=vmess_user.level,
            security=vmess_user.security,
            user_id=vmess_user.user_id
        )

    def remove_vmess_user(self, email: str, inbound_tag: str):
        self.client.remove_user(inbound_tag=inbound_tag, email=email)

    def traffic_usage(self, email: str):
        return self.client.get_user_usage(email=email)

    def reset_user_traffic(self, email: str):
        self.client.get_user_usage(email=email, reset=True)
        return True

    def traffic_all_usage(self, inbound_tag: str):
        pass

    def traffic_all_user(self, inbound_tag: str):
        pass
