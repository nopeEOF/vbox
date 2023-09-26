import datetime
import typer
import json
import base64
from typing import Optional
from app.v2ray.v2call import MyV2RayClient
from enum import Enum
from app.utils import v2_match_db
from app.utils import stats as mystats
from app.cli.utyper import UTyper
from rich import print
from app.readconfig import get_config
from v2client import utils

cli_app = UTyper()
v2ray = MyV2RayClient(client="v2fly")


class VMessSecurityTypes(str, Enum):
    UNKNOWN = "UNKNOWN"
    LEGACY = "LEGACY"
    AUTO = "AUTO"
    AES128_GCM = "AES128_GCM"
    CHACHA20_POLY1305 = "CHACHA20_POLY1305"
    NONE = "NONE"


@cli_app.command(help="add vmess user")
async def add_vmess_user(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help="Email address"
        ),
        uuid: Optional[str] = typer.Option(
            utils.random_uuid(),
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
        ),
        expire_days: int = typer.Option(
            ...,
            "-ed",
            "--expire-days",
            help="set expire date from days"
        ),
        active: Optional[bool] = typer.Option(
            True,
            "-a",
            "--active",
            help="active user"
        ),
        traffic: float = typer.Option(
            ...,
            "-t",
            "--traffic",
            help="set traffic usage allowed. use GIGByte"
        )
):
    now = datetime.datetime.utcnow()
    expire_date = now + datetime.timedelta(days=+expire_days)
    traffic = traffic * (1024 ** 3)
    v2user = mystats.VMessUser(email=email, security=security, level=level, uuid=uuid)
    user = mystats.User(expireDate=expire_date, active=active, traffic=traffic, v2user=v2user, protocol="vmess")
    await v2_match_db.add_vmess_user(user=user)


@cli_app.command(help="get user usage")
async def user_usage(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help=""
        )
):
    db_flag = await v2_match_db.update_user_usage(email=email)
    if db_flag:
        if db_flag.flag:
            print("Download Usage: {0:.3f} G & Upload Usage: {1:.3f} G".format(
                db_flag.status.download / 1024 ** 3, db_flag.status.upload / 1024 ** 3)
            )
        else:
            print(db_flag.status)


@cli_app.command(help="delete user from db and v2ray")
async def delete_user(
        email: str = typer.Option(
            ...,
            "-e",
            "--email",
            help=""
        )
):
    await v2_match_db.remove_user(email=email)


@cli_app.command(help="set user usage or reset traffic")
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
    traffic = traffic * (1024 ** 3)
    await v2_match_db.set_user_usage(email=email, upload=upload, download=download, traffic=traffic)


@cli_app.command(help="get all user list and usage")
async def all_user(
        link: Optional[bool] = typer.Option(
            False,
            "-l",
            "--link",
            help="get vmess user link"
        )
):
    users = await v2_match_db.list_users()
    if users.flag:
        for user in users.status:
            domain = get_config()["v2rayapi"]["domain"]
            expire = user.expire.strftime("%m/%d/%Y, %H:%M")
            if user.traffic == -1:
                traffic = -1
            else:
                traffic = "{:.3f}".format(user.traffic / 1024 ** 3)
            j = json.dumps({
                "v": "2", "ps": user.email, "add": domain, "port": "443", "id": user.uuid, "aid": "0", "net": "ws",
                "type": "none",
                "host": domain, "path": "/ws", "tls": "tls", "sni": domain
            })

            config = "vmess://" + base64.b64encode(j.encode('ascii')).decode('ascii')
            print(f"user: {user.email}\nuuid: {user.uuid}\nexpire: {expire}\ntraffic: {traffic}")
            if link:
                print(config)
            print("Download Usage: {0:.3f} G & Upload Usage: {1:.3f} G".format(
                user.download / 1024 ** 3, user.upload / 1024 ** 3)
            )
            print("-" * 20)
    else:
        print(users.status)
