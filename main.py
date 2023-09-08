from typing import Optional
import typer

app = typer.Typer()


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
def cli():
    pass


@app.command(help="")
def telbot():
    pass
