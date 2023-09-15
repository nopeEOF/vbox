from typing import Optional
from app.v2ray.v2ray import VMessUser, MyV2RayClient
from enum import Enum
from app import readconfig
import typer

cli_app = typer.Typer()
v2ray = MyV2RayClient(client="v2fly")


class VMessSecurityTypes(str, Enum):
    UNKNOWN = "UNKNOWN"
    LEGACY = "LEGACY"
    AUTO = "AUTO"
    AES128_GCM = "AES128_GCM"
    CHACHA20_POLY1305 = "CHACHA20_POLY1305"
    NONE = "NONE"


@cli_app.command(help='')
def add_user(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help="Email address"
        ),
        inbound_tag: str = typer.Option(
            ...,
            "-i",
            "--inbound-tag",
            help="Inbound tag"
        ),
        level: int = typer.Option(
            0,
            "-l",
            "--level",
            help="Level"
        ),
        security: Optional[VMessSecurityTypes] = typer.Option(
            VMessSecurityTypes.AUTO,
            "-s",
            "--security",
            help="Security",
            case_sensitive=False
        )
):
    user = VMessUser(email=email, security=security, level=level, inbound_tag=inbound_tag)
    config = readconfig.get_config()
    v2ray_client = v2ray.connect(host=config["v2rayapi"]["host"], port=config["v2rayapi"]["port"])
    v2ray_client.add_vmess_user(vmess_user=user)


@cli_app.command(help='')
def user_usage(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help=""
        ),
        reset: Optional[bool] = typer.Option(
            False,
            "-r",
            "--reset",
            help=""
        )
):
    config = readconfig.get_config()
    v2ray_client = v2ray.connect(host=config["v2rayapi"]["host"], port=config["v2rayapi"]["port"])
    v2ray_client.user_usage(email=email, reset=reset)
