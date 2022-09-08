import click
from .cli import cli


@cli.group(help='Organization management')
def organization():
    pass
