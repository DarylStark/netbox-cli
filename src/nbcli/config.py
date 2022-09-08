import nbcli
import click
from rich import box
from rich.table import Table
from .nbcli import nbcli_object
from .cli import cli, console, tables


def get_config() -> dict:
    """ retrieve configuration from configfile """


@cli.group(help='Netbox CLI configuration')
def config() -> None:
    pass


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
    # Create a table for the output
    table = Table(**tables)
    table.add_column('Name', style='item_identification')
    table.add_column('Server')
    table.add_column('Port')
    table.add_column('State')

    # Add the rows
    for name, config in nbcli_object.config['instances'].items():
        table.add_row(name,
                      config['server'],
                      str(config['port']),
                      ('[item_activated]Activated[/]' if nbcli_object.config['selected_instance'] == name
                       else 'Configured'))

    # Print the table
    console.print(table)


@config.command(help='Add a Netbox instance. Default port is 8000')
@click.argument('name', type=str)
@click.argument('server', type=str)
@click.argument('api_key', type=str)
@click.argument('port', type=int, default=8000)
def add_instance(name: str, server: str, api_key: str, port: int) -> None:
    """ The `add-instance` command can be used to add a
        Netbox instance.

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
