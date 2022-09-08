from .nbcli import nbcli_object
from .organization import organization


@organization.group(help='Site management')
def sites():
    pass


@sites.command()
def list():
    """ Lists the sites in the Netbox database

        Parameters
        ----------
        Parameters and their types

        Returns
        -------
        Return values
    """
    # Create the object
    nbcli_object.create_pynetbox_object()

    # Get the sites
    resources = nbcli_object.nb.dcim.sites.all()
    for resource in resources:
        print(resource)
