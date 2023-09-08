from typing import Optional
from utils.main import VMessUser, V2Ray
from enum import Enum
import typer

cli_app = typer.Typer()
v2ray = V2Ray()


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
    v2ray.add_vmess_user(vmess_user=user)


@cli_app.command(help='')
def user_usage(
        email: str = typer.Option(
            str,
            "-e",
            "--email",
            help=""
        )
):
    v2ray.traffic_usage(email=email)
