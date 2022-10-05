import click
from ctypes import alignment
from .nbcli import nbcli_object
from .devices import devices as devices_group
from .cli import cli, console, tables
from rich.table import Table


@devices_group.group(help='Device management')
def devices():
    pass


#@sites.command(help='Create a new site')
#@click.option('--name', type=str, prompt=True)
#@click.option('--slug', type=str, prompt=True)
#@click.option('--status', type=click.Choice(
    #['planned', 'staging', 'active', 'decommissioning', 'retired']
#))
#@click.option('--facility', type=str)
#@click.option('--description', type=str)
#@click.option('--physical-address', type=str)
#@click.option('--shipping-address', type=str)
#@click.option('--comments', type=str)
#def create(**kwargs) -> None:
    #""" Method to create a new site
#
        #Parameters
        #----------
        #**kwargs: dict
            #Values to update
#
        #Returns
        #-------
        #None
    #"""
#
    ## Create the object
    #nbcli_object.create_pynetbox_object()
#
    ## Get the resources
    #resource_object = nbcli_object.nb.dcim.sites
#
    ## Add the new resource. We remove all fields that are set
    ## to None in a dict-comprehension
    #resource_object.create(
        #{setting: value for setting, value in kwargs.items() if value is not None})


@devices.command(help='List the devices in NetBox')
@click.option('--name', type=str)
@click.option('--name__ic', type=str)
def list(**kwargs) -> None:
    """ Lists the devices in the NetBox database

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
    table.add_column('Site')
    table.add_column('Location')
    table.add_column('Role')
    table.add_column('Platform')
    table.add_column('Type')
    table.add_column('IP address')

    # Get the resources
    resource_object = nbcli_object.nb.dcim.devices

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
            str(resource.site),
            str(resource.location),
            str(resource.device_role),
            str(resource.platform),
            str(resource.device_type),
            str(resource.primary_ip4)
        )

    # Print the table
    console.print(table)


#@sites.command(help='Inspect a specific site')
#@click.argument('name', type=str)
#def inspect(name: str) -> None:
    #""" Inspect a specific site
#
        #Parameters
        #----------
        #name : str
            #The name for the site to inspect
#
        #Returns
        #-------
        #None
    #"""
    ## Create the object
    #nbcli_object.create_pynetbox_object()
#
    ## Get the resource
    #resource_object = nbcli_object.nb.dcim.sites.get(name=name)
#
    ## Create a table for the site details
    #table = Table(show_header=False, **tables)
    #table.add_column('Setting', style='item_identification')
    #table.add_column('Value')
#
    ## Add the roes
    #table.add_row('Name', resource_object.name)
    #table.add_row('Region', str(resource_object.region))
    #table.add_row('Status', str(resource_object.status))
    #table.add_row('Tenant', resource_object.tenant)
    #table.add_row('Facility', resource_object.facility)
    #table.add_row('Description', resource_object.description)
    #table.add_row('Time zone', resource_object.time_zone)
    #table.add_row('Physical address', resource_object.physical_address)
    #table.add_row('Shipping address', resource_object.shipping_address)
#
    ## Print the table
    #console.print(table)
#
    ## Create a table for the related objects
    #table = Table(show_header=False, **tables)
    #table.add_column('Setting', style='item_identification')
    #table.add_column('Value')
#
    ## Add the roes
    #table.add_row('Racks', str(resource_object.rack_count))
    #table.add_row('Devices', str(resource_object.device_count))
    #table.add_row('Virtual Machines', str(
        #resource_object.virtualmachine_count))
    #table.add_row('Prefixes', str(resource_object.prefix_count))
    #table.add_row('VLANs', str(resource_object.vlan_count))
    #table.add_row('ASNs', str(len(resource_object.asns)))
    #table.add_row('Circuits', str(resource_object.circuit_count))
#
    ## Print the table
    #console.print(table)
#
#
#@sites.command(help='Update a site')
#@click.argument('name', type=str)
#@click.option('--slug', type=str)
#@click.option('--status', type=click.Choice(
    #['planned', 'staging', 'active', 'decommissioning', 'retired']
#))
#@click.option('--facility', type=str)
#@click.option('--description', type=str)
#@click.option('--physical-address', type=str)
#@click.option('--shipping-address', type=str)
#@click.option('--comments', type=str)
#def update(name: str, **kwargs) -> None:
    #""" Method to update a site
#
        #Parameters
        #----------
        #name: str
            #The name of the site to update
#
        #**kwargs: dict
            #Values to update
#
        #Returns
        #-------
        #None
    #"""
#
    ## Create the object
    #nbcli_object.create_pynetbox_object()
#
    ## Get the resources
    #resource_object = nbcli_object.nb.dcim.sites.get(name=name)
#
    ## Update the resource
    #for setting, value in kwargs.items():
        #if value is not None:
            #setattr(resource_object, setting, value)
#
    ## Update the resource
    #resource_object.save()
#
#
#@sites.command(help='Delete a site')
#@click.argument('name', type=str)
#def delete(name: str) -> None:
    #""" Method to delete a site
#
        #Parameters
        #----------
        #name: str
            #The name of the site to delete
#
        #Returns
        #-------
        #None
    #"""
#
    ## Create the object
    #nbcli_object.create_pynetbox_object()
#
    ## Get the resources
    #resource_object = nbcli_object.nb.dcim.sites.get(name=name)
#
    ## Delete the resource
    #resource_object.delete()
