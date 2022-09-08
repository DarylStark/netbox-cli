from .cli import cli, tables, console
from .nbcli import nbcli_object
from rich.table import Table


@cli.command(help='NetBox status')
def status():
    """ Method that returns the status of NetBox, like the
        version, installed apps and plugins.

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    # Create the object
    nbcli_object.create_pynetbox_object()
    status = nbcli_object.nb.status()

    # Create a table for the output
    table = Table(show_header=False, **tables)
    table.add_column('Field', style='item_identification')
    table.add_column('Value')

    # Add the rows
    table.add_row('Python version', status['python-version'])
    table.add_row('Django version', status['django-version'])
    table.add_row('NetBox version', status['netbox-version'])

    if len(status['installed-apps']):
        table.add_row('\nInstalled apps')
        for app, version in status['installed-apps'].items():
            table.add_row(f'  {app}', version)

    if len(status['plugins']):
        table.add_row('\nInstalled plugins')
        for plugin, version in status['plugins'].items():
            table.add_row(f'  {plugin}', version)

    # Print the table
    console.print(table)
