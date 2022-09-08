import click
from ctypes import alignment
from .nbcli import nbcli_object
from .organization import organization
from .cli import cli, console, tables
from rich.table import Table


@organization.group(help='Site management')
def sites():
    pass


@sites.command()
@click.option('--name', type=str)
@click.option('--name__ic', type=str)
@click.option('--description__ic', type=str)
def list(**kwargs) -> None:
    """ Lists the sites in the NetBox database

        Parameters
        ----------
        Parameters and their types

        Returns
        -------
        Return values
    """
    # Create the object
    nbcli_object.create_pynetbox_object()

    # Create a table for the output
    table = Table(**tables)
    table.add_column('ID', style='item_identification', justify='right')
    table.add_column('Name', style='item_identification')
    table.add_column('Status')
    table.add_column('Region')
    table.add_column('Group')
    table.add_column('Description')

    # Get the resources and add them to the table
    resource_object = nbcli_object.nb.dcim.sites

    # Filter resources if needed
    if len(kwargs) == 0:
        resources = resource_object.all()
    else:
        resources = resource_object.filter(**kwargs)

    for resource in resources:
        table.add_row(
            str(resource.id),
            str(resource.name),
            str(resource.status),
            str(resource.region),
            str(resource.group),
            str(resource.description)
        )

    # Print the table
    console.print(table)
