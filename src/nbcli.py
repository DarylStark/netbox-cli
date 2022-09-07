""" Module that contains the main method for the CLI
    application """

from argparse import ArgumentParser


def nbcli() -> None:
    groups = {
        'organization': {
            'help': 'Organization',
            'models': {
                'sites': {
                    'commands': {
                        'create': {
                            'help': 'Create a site'
                        },
                        'list': {
                            'help': 'List sites',
                            'optionals': {
                                '--name': {}
                            }
                        },
                        'update': {
                            'help': 'Update a site'
                        },
                        'delete': {
                            'help': 'Delete a site'
                        },
                    }
                },
                'regions': {
                    'commands': {
                        'create': {
                            'help': 'Create a region'
                        },
                        'list': {
                            'help': 'List regions'
                        },
                        'update': {
                            'help': 'Update a region'
                        },
                    }
                }
            }
        },
        'devices': {
            'help': 'Devices',
            'models': {}
        }
    }
    # Create a argument parser
    arguments = ArgumentParser('Netbox CLI')
    group = arguments.add_subparsers(
        title='group',
        help='The group to manipulate')

    # Add the needed subparsers
    for group_name, group_details in groups.items():
        subgroup = group.add_parser(
            name=group_name,
            help=group_details['help'])
        model = subgroup.add_subparsers(
            title='model',
            help='The model to manipulate')
        for model_name, model_details in group_details['models'].items():
            submodel = model.add_parser(
                name=model_name)
            command = submodel.add_subparsers(
                title='command',
                help='The action to execute on the model')
            for command_name, command_details in model_details['commands'].items():
                ncommand = command.add_parser(
                    name=command_name,
                    help=command_details['help'])
                if 'optionals' in command_details.keys():
                    for argument_name, argument_details in command_details['optionals'].items():
                        command.add_argument(argument_name)

    # # Organization
    # group_organization = group.add_parser(
    #     name='organization',
    #     help='Organizations')
    # model = group_organization.add_subparsers(
    #     title='model',
    #     help='The model to manipulate')

    # # Organization / Sites
    # sites = model.add_parser(
    #     name='sites',
    #     help='Manipulate sites')
    # command = sites.add_subparsers(
    #     title='command',
    #     help='The action to execute')
    # command.add_parser(
    #     name='delete',
    #     help='Delete a site')
    # command.add_parser(
    #     name='create',
    #     help='Create a new site')
    # command.add_parser(
    #     name='list',
    #     help='List sites')
    # command.add_parser(
    #     name='update',
    #     help='Update a site')

    # group_devices = group.add_parser('devices', help='Devices')
    # group_connections = group.add_parser('connections', help='Connections')
    # group_wireless = group.add_parser('wireless', help='Wireless')
    # group_ipam = group.add_parser('ipam', help='IPAM')

    # Parse the arguments
    args = arguments.parse_args()


if __name__ == '__main__':
    nbcli()
