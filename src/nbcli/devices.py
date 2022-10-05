import click
from .cli import cli


@cli.group(help='Device management')
def devices():
    pass
