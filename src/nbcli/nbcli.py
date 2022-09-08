from genericpath import isfile
from pathlib import Path
from typing import Optional
import logging
import json
import os
import pynetbox

NBCLI_CONFIG_FILE = f'{Path.home()}/.nbcli.json'


class NetBoxCLI:
    def __init__(self) -> None:
        """ The initiator sets default values

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        # Default configuration is nothing
        self.config_dict: Optional[dict] = None

        # Create a logger
        self.logger = logging.getLogger('NetBoxCLI')

    def create_default_config(self, force: bool = False) -> None:
        """ Method to create the default config

            Parameters
            ----------
            force: bool
                If set, forces the method to create the
                default config even if there alrady is a
                config file.

            Returns
            -------
            None
        """
        if os.path.isfile(NBCLI_CONFIG_FILE) and not force:
            self.logger.debug(f'File "{NBCLI_CONFIG_FILE}" already exists')
            return

        # Default configuration
        default_config = {
            'active_instance': 'default',
            'instances': {
                'default': {
                    'server': 'localhost',
                    'port': 8000,
                    'base_path': '/',
                    'api_key': ''
                }
            }
        }

        self.logger.debug(f'Opening "{NBCLI_CONFIG_FILE}" for writing')
        with open(NBCLI_CONFIG_FILE, 'w') as config_file:
            config_file.write(json.dumps(default_config))
        self.config_dict = default_config

    def get_configuration(self) -> Optional[dict]:
        """ Method to retrieve the configuration ad save it
            into the object.

            Parameters
            ----------
            force: bool
                If set, forces the method to create the
                default config even if there alrady is a
                config file.

            Returns
            -------
            None
        """
        self.create_default_config()
        self.logger.debug(f'Opening "{NBCLI_CONFIG_FILE}" for reading')
        with open(NBCLI_CONFIG_FILE, 'r') as config_file:
            config = json.loads(config_file.read())

        self.logger.debug('Loaded config')

        # Save it
        self.config_dict = config
        return config

    @property
    def config(self) -> dict:
        """ Property that returns the config

            Parameters
            ----------
            None

            Returns
            -------
            dict
                The configuration
        """
        if not self.config_dict:
            self.get_configuration()
        return self.config_dict

    def save(self) -> None:
        """ Save the configuration

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        self.logger.debug(f'Opening "{NBCLI_CONFIG_FILE}" for writing')
        with open(NBCLI_CONFIG_FILE, 'w') as config_file:
            config_file.write(json.dumps(self.config_dict))

    def get_active_instance(self) -> dict:
        """ Method to get the active instance

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        config = self.config
        return config['instances'][config['active_instance']]

    def create_pynetbox_object(self) -> None:
        """ Method to create a PyNetbox object

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        instance = self.get_active_instance()
        nb_url = f'http://{instance["server"]}:{instance["port"]}{instance["base_path"]}'
        self.nb = pynetbox.api(
            nb_url,
            token=instance["api_key"])


nbcli_object = NetBoxCLI()
