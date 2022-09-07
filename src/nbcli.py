""" Module that contains the main method for the CLI
    application """

from argparse import ArgumentParser

def nbcli() -> None:
    # Create a argument parser
    arguments = ArgumentParser('Netbox CLI')

    # Create a object for subparser
    subs = arguments.add_subparsers(
        title='group',
        metavar='group',
        help='Command group',
        dest='group',
        required=True)

    # Add the subparser for organization
    organization = subs.add_parser('organization', help='Organization management').add_subparsers(
        title='command', metavar='command', help='Command', required=True)
    organization_sites = organization.add_parser('sites', help='Site management')

    # Parse the arguments
    args = arguments.parse_args()

    print(args.command)

if __name__ == '__main__':
    nbcli()