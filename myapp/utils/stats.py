import datetime
from dataclasses import dataclass
from v2client.enum import VMessSecurityTypes, ProxyTypes, VLESSFlowTypes, VLESSEncryptionTypes
from v2client import utils
from myapp.readconfig import get_config


class VLessUser:
    def __init__(
            self,
            email: str,
            inbound_tag: str = get_config()["v2rayapi"]["inbound_tag"],
            level: int = 0,
            uuid: str = utils.random_uuid()
    ) -> None:
        self.inbound_tag = inbound_tag
        self.email = email
        self.level = level
        self.proxyType = ProxyTypes.VLESS
        self.flow = VLESSFlowTypes.XTLS_RPRX_ORIGIN
        self.encryption = VLESSEncryptionTypes.NONE
        self.userUuid = uuid


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


@dataclass
class UsersUsage:
    email: str
    upload: float
    download: float


@dataclass
class Detail:
    flag: bool
    status: any


@dataclass
class User:
    expireDate: datetime.datetime
    traffic: int
    v2user: VMessUser
    active: bool
    protocol: str
