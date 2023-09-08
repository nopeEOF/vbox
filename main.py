from typing import Optional
from cli.main import cli_app
from utils.main import V2Ray
import typer

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
    v2ray = V2Ray()
    v2ray.v2ray_connect(host="127.0.0.1", port=8080)
    app()
