import click
from .cli import cli


@cli.group(help='Organization management')
def organization():
    pass


@organization.group(help='Site management')
def sites():
    pass


@organization.group(help='Region management')
def regions():
    pass


@organization.group(help='Location management')
def locations():
    pass
