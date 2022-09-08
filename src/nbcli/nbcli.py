from genericpath import isfile
from pathlib import Path
from typing import Optional
import json
import os

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

        # Retrieve the configuration
        self.get_configuration()

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
            return

        # Default configuration
        default_config = {
            'selected_instance': 'default',
            'instances': {
                'default': {
                    'server': 'localhost',
                    'port': 8000,
                    'base_path': '/',
                    'api_key': ''
                }
            }
        }
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
        with open(NBCLI_CONFIG_FILE, 'r') as config_file:
            config = json.loads(config_file.read())

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
        with open(NBCLI_CONFIG_FILE, 'w') as config_file:
            config_file.write(json.dumps(self.config_dict))


nbcli_object = NetBoxCLI()
