from typing import Optional
from app.v2ray.v2call import VMessUser, MyV2RayClient
from enum import Enum
from app.utils import v2_match_db
from app.cli.utyper import UTyper
import typer

cli_app = UTyper()
v2ray = MyV2RayClient(client="v2fly")


class VMessSecurityTypes(str, Enum):
    UNKNOWN = "UNKNOWN"
    LEGACY = "LEGACY"
    AUTO = "AUTO"
    AES128_GCM = "AES128_GCM"
    CHACHA20_POLY1305 = "CHACHA20_POLY1305"
    NONE = "NONE"


@cli_app.command(help='')
async def add_user(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help="Email address"
        ),
        uuid: Optional[str] = typer.Option(
            None,
            "-u",
            "--uuid",
            help="uuid"
        ),
        level: Optional[int] = typer.Option(
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
    user = VMessUser(email=email, security=security, level=level, uuid=uuid)
    await v2_match_db.add_vmess_user(user=user)


@cli_app.command(help='')
async def user_usage(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help=""
        )
):
    db_flag = await v2_match_db.user_usage(email=email)
    if db_flag:
        if db_flag.flag:
            print("Download Usage: {0:.3f} G & Upload Usage: {1:.3f} G".format(
                db_flag.status.download / 1024 ** 3, db_flag.status.upload / 1024 ** 3)
            )
        else:
            print(db_flag.status)


@cli_app.command(help="")
async def delete_user(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help=""
        )
):
    await v2_match_db.remove_user(email=email)


@cli_app.command(help="")
async def set_user_usage(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help=""
        ),
        upload: Optional[int] = typer.Option(
            0,
            "--upload",
            "-u",
            help=""
        ),
        download: Optional[int] = typer.Option(
            0,
            "--download",
            "-d",
            help=""
        ),
        traffic: Optional[int] = typer.Option(
            0,
            "--traffic",
            "-t",
            help=""
        ),
):
    await v2_match_db.reset_user_usage(email=email, upload=upload, download=download, traffic=traffic)
