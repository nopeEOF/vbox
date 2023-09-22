from typing import Optional
from app.cli.cli_main import cli_app
from app.cli.utyper import UTyper
from app.service.service_main import Service
import typer


app = UTyper()
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


@app.command(help="")
async def service(
        first_run: Optional[bool] = typer.Option(
            False,
            "-f",
            "--first-run",
            help="first"
        )
):
    service_class = Service()
    await service_class.refresh_v2_in_db(first_run=first_run)


if __name__ == '__main__':
    app()

