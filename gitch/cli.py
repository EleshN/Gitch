import typer
from gitch.core import gitch_commit

app = typer.Typer()

@app.command()
def commit(m: str, files: bool = True, footer: bool = True):
    gitch_commit(message=m, include_files=files, include_footer=footer)

if __name__ == "__main__":
    app()
