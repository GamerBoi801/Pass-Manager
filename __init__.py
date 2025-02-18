from .main import app, DB_PATH, first_use
import typer
import os

typer.echo('Initialsing Password Manager Package.')

#checking to see whether the db exists or not
if not os.path.exists(DB_PATH):
    typer.echo('No database found. Please run the first-use command to set up the application.')
    typer.echo('Running the first-use setup...')
    first_use()

__all__ = ['app']
