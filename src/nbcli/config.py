import logging
import click
from rich.table import Table

from nbcli.exceptions import ConfigInstancesLastDeleted
from .nbcli import nbcli_object
from .cli import cli, console, tables

logger = logging.getLogger('config')


def get_config() -> dict:
    """ retrieve configuration from configfile """


@cli.group(help='Netbox CLI configuration')
def config() -> None:
    pass


@config.command(help='Add a Netbox instance. Default port is 8000')
@click.option('--name', type=str, prompt=True)
@click.option('--server', type=str, prompt=True)
@click.option('--api-key', type=str, prompt='API key')
@click.option('--port', type=int, default=8000, prompt=True)
def add_instance(name: str, server: str, api_key: str, port: int) -> None:
    """ The `add-instance` command can be used to add a
        Netbox instance.

        Parameters
        ----------
        name: str
            The name of the instance

        server: str
            The name of the server

        api_key: str
            The API key to use for this server

        port: int
            The port to connect to

        Returns
        -------
        None
    """
    # Retrieve the config
    config = nbcli_object.config

    # Check if this instance is unique
    if name in config['instances'].keys():
        console.print(
            f'[error]There is alrady an instance with the name "[error_highlight]{name}[/]"[/]')
        return

    # Create the instance dict
    instance_dict = {
        'server': server,
        'port': port,
        'base_path': '/',
        'api_key': api_key
    }

    # Add it to the configuration
    config['instances'][name] = instance_dict

    # Save the new config
    nbcli_object.save()


@config.command(help='List configured Netbox instances')
def list_instances() -> None:
    """ The `list_instances` command returns a list of
        configured instances.

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    # Retrieve the config
    config = nbcli_object.config

    # Create a table for the output
    table = Table(**tables)
    table.add_column('*', style='item_selected')
    table.add_column('Name', style='item_identification')
    table.add_column('Server')
    table.add_column('Port')

    # Add the rows
    for name, instance_detail in nbcli_object.config['instances'].items():
        table.add_row(
            '*' if name == config['active_instance'] else '',
            name,
            instance_detail['server'],
            str(instance_detail['port']),
        )

    # Print the table
    console.print(table)


@config.command(help='Inspect a specific Netbox instance')
@click.argument('name', type=str)
def inspect_instance(name: str) -> None:
    """ Inspect a specific instance of Netbox

        Parameters
        ----------
        name: str
            The name of the instance to inspect

        Returns
        -------
        None
    """
    # Retrieve the config
    config = nbcli_object.config

    # Check if this instance is unique
    if name not in config['instances'].keys():
        logger.debug(
            f'Possible instances: {list(config["instances"].keys())}')
        console.print(
            f'[error]No instance with name "[error_highlight]{name}[/]" found[/]')
        return

    # Get the instance object
    instance_object = config['instances'][name]

    # Create a table for the output
    table = Table(**tables)
    table.add_column('Setting', style='item_identification')
    table.add_column('Value')

    # Add the rows
    table.add_row('Name', name)
    table.add_row('Server', instance_object['server'])
    table.add_row('Port', str(instance_object['port']))
    table.add_row('Base path', instance_object['base_path'])
    table.add_row('API key', instance_object['api_key'])

    # Print the table
    console.print(table)


@config.command(help='Update a configured Netbox instance')
@click.argument('name', type=str)
@click.option('--server', type=str)
@click.option('--api-key', type=str)
@click.option('--port', type=int)
@click.option('--base-path', type=str)
def update_instance(name: str, server: str, api_key: str, port: int, base_path: str) -> None:
    """ Update a instance

        Parameters
        ----------
        name: str
            The name of the instance

        server: str
            The name of the server

        api_key: str
            The API key to use for this server

        port: int
            The port to connect to

        base_path: str
            The base path on the server for Netbox

        Returns
        -------
        None
    """
    # Retrieve the config
    config = nbcli_object.config

    # Check if this instance is unique
    if name not in config['instances'].keys():
        logger.debug(
            f'Possible instances: {list(config["instances"].keys())}')
        console.print(
            f'[error]No instance with name "[error_highlight]{name}[/]" found[/]')
        return

    # Update the dict
    for item in ('server', 'api_key', 'port', 'base_path'):
        if locals()['item']:
            config['instances'][name][item] = locals()[item]

    nbcli_object.save()


@config.command(help='Delete a configured Netbox instance')
@click.argument('name', type=str)
def delete_instance(name: str) -> None:
    """ Delete a instance

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    # Retrieve the config
    config = nbcli_object.config

    # Check if this instance is unique
    if name not in config['instances'].keys():
        logger.debug(
            f'Possible instances: {list(config["instances"].keys())}')
        console.print(
            f'[error]No instance with name "[error_highlight]{name}[/]" found[/]')
        return

    # If this instance is the selected one, we selected another
    if config['active_instance'] == name:
        other_instances = [
            instance
            for instance in config['instances'].keys()
            if instance != name]
        if len(other_instances) == 0:
            raise ConfigInstancesLastDeleted(
                'This instance cannot be deleted since it is the last available instance')
        config['active_instance'] = other_instances[0]

    # Remove the key from the dict
    config['instances'].pop(name)
    nbcli_object.save()


@config.command(help='Activate a specific Netbox instance')
@click.argument('name', type=str)
def activate_instance(name: str) -> None:
    """ Activate a specific instance of Netbox

        Parameters
        ----------
        name: str
            The name of the instance to activate

        Returns
        -------
        None
    """
    # Retrieve the config
    config = nbcli_object.config

    # Check if this instance is unique
    if name not in config['instances'].keys():
        logger.debug(
            f'Possible instances: {list(config["instances"].keys())}')
        console.print(
            f'[error]No instance with name "[error_highlight]{name}[/]" found[/]')
        return

    # Set the active instance
    config['active_instance'] = name
    nbcli_object.save()
