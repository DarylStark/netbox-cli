import logging
import click
from rich.table import Table
from .nbcli import nbcli_object
from .cli import cli, console, tables

logger = logging.getLogger('config')


def get_config() -> dict:
    """ retrieve configuration from configfile """


@cli.group(help='Netbox CLI configuration')
def config() -> None:
    pass


@config.command(help='Add a Netbox instance. Default port is 8000')
@click.argument('name', type=str)
@click.argument('server', type=str)
@click.argument('api-key', type=str)
@click.argument('port', type=int, default=8000)
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
            config['instances'][name][item] = locals()['item']

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
