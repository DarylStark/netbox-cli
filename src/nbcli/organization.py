import click
from .nbcli import nbcli


@nbcli.group()
def organization():
    pass


@organization.group()
def sites():
    pass


@sites.command()
@click.option('--all', is_flag=True)
def list(all: bool = True):
    print('listing sites')
