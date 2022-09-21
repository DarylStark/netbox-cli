import click
from ctypes import alignment
from .nbcli import nbcli_object
from .organization import organization
from .cli import cli, console, tables
from rich.table import Table


@organization.group(help='Region management')
def regions():
    pass


@regions.command(help='Create a new region')
@click.option('--name', type=str, prompt=True)
@click.option('--slug', type=str, prompt=True)
@click.option('--description', type=str)
def create(**kwargs) -> None:
    """ Method to create a new region

        Parameters
        ----------
        **kwargs: dict
            Values to update

        Returns
        -------
        None
    """

    # Create the object
    nbcli_object.create_pynetbox_object()

    # Get the resources
    resource_object = nbcli_object.nb.dcim.regions

    # Add the new resource. We remove all fields that are set
    # to None in a dict-comprehension
    resource_object.create(
        {setting: value for setting, value in kwargs.items() if value is not None})


@regions.command(help='List the regions in NetBox')
@click.option('--name', type=str)
@click.option('--name__ic', type=str)
@click.option('--description__ic', type=str)
def list(**kwargs) -> None:
    """ Lists the regions in the NetBox database

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
    table.add_column('Sites')
    table.add_column('Description')

    # Get the resources
    resource_object = nbcli_object.nb.dcim.regions

    # Filter resources if needed
    if len(kwargs) == 0:
        resources = resource_object.all()
    else:
        resources = resource_object.filter(**kwargs)

    for resource in resources:
        table.add_row(
            str(resource.id),
            str(resource.name),
            str(resource.site_count),
            str(resource.description)
        )

    # Print the table
    console.print(table)


@regions.command(help='Update a region')
@click.argument('name', type=str)
@click.option('--slug', type=str)
@click.option('--description', type=str)
def update(name: str, **kwargs) -> None:
    """ Method to update a region

        Parameters
        ----------
        name: str
            The name of the region to update

        **kwargs: dict
            Values to update

        Returns
        -------
        None
    """

    # Create the object
    nbcli_object.create_pynetbox_object()

    # Get the resources
    resource_object = nbcli_object.nb.dcim.regions.get(name=name)

    # Update the resource
    for setting, value in kwargs.items():
        if value is not None:
            setattr(resource_object, setting, value)

    # Update the resource
    resource_object.save()


@regions.command(help='Delete a region')
@click.argument('name', type=str)
def delete(name: str) -> None:
    """ Method to delete a region

        Parameters
        ----------
        name: str
            The name of the region to delete

        Returns
        -------
        None
    """

    # Create the object
    nbcli_object.create_pynetbox_object()

    # Get the resources
    resource_object = nbcli_object.nb.dcim.regions.get(name=name)

    # Delete the resource
    resource_object.delete()
