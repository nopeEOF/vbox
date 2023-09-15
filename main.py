from typing import Optional
from app.cli.cli_main import cli_app
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
    app()
