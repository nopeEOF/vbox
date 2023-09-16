from typing import Optional
from app.cli.cli_main import cli_app
from app.db import dbmanager
from app.v2ray.v2call import VMessUser
import typer
import asyncio

app = typer.Typer()
app.add_typer(cli_app, name="cli")


@app.command(help="")
def restapi(
        host: Optional[str] = typer.Option(
            "localhost",
            "-h",
            "--host",
            help=""
        ),
        port: Optional[int] = typer.Option(
            8000,
            "-p",
            "--port",
            help="port to listen"
        )
):
    pass


@app.command(help="")
def telbot():
    pass


if __name__ == '__main__':
    asyncio.run(dbmanager.db_add_vmess_user(VMessUser(email="sezfxsdsr@gmail.com")))
    # asyncio.run(a.remove_user(email="sefr@gmail.com"))
    # asyncio.run(a.add_vmess_user(email="sedsxxvdr@gmail.com"))
    # asyncio.run(a.update_activity(email="sefr@gmail.com", active=True))
    a = asyncio.run(dbmanager.db_users_usage())
    print(a)

