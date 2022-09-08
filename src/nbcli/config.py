import click
import nbcli
from .cli import cli, console, tables
from .nbcli import nbcli_object
from rich.table import Table
from rich import box


def get_config() -> dict:
    """ retrieve configuration from configfile """


@cli.group(help='Netbox CLI configuration')
def config():
    pass


@config.command(help='List configured Netbox isntances')
def list_instances():
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
    table.add_column('Base path')
    table.add_column('State')

    # Add the rows
    for name, config in nbcli_object.config['instances'].items():
        table.add_row(name,
                      config['server'],
                      str(config['port']),
                      config['base_path'],
                      ('[item_activated]Activated[/]' if nbcli_object.config['selected_instance'] == name
                       else 'Configured'))

    # Print the table
    console.print(table)
