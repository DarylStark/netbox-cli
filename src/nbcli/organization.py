import click
from .cli import cli


@cli.group()
def organization():
    pass


@organization.group()
def sites():
    pass


@sites.command()
def list(all: bool = True):
    pass
