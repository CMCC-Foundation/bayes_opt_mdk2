# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import toml

from src.service.PathService import PathService

from src.serviceImpl.ConfigServiceImpl import configServiceImpl

path_service_instance = PathService()
config_file_path = path_service_instance.get_WORKFLOW_CONFIG_path()

class ConfigService:
        
    def __init__(self):
        """ Initialize the ConfigService instance with the path to the configuration file """
        self.config_file_path = config_file_path
        self.config_loader = configServiceImpl()
        self.config = self.load_config(config_file_path)

    def load_config(self, config_file_path):
        """
        Loads configuration from the specified file, handling exceptions as appropriate
        """
        try:
            return self.config_loader.load_config_impl(config_file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_file_path}")
        except toml.TomlDecodeError as e:
            raise Exception(f"Error while loading the configuration file: {str(e)}")

    def get_config_value(self, key):
        """
        Returns the value associated with a specific key in the configuration file.
        If the key is not present, returns None
        """
        try:
            return configServiceImpl.get_config_value_impl(self.config, key)
        except (TypeError, KeyError):
            return None

    def set_config_value(self, key, new_value):
        """
        Sets the new value associated with a specific key in the configuration file
        """
        try:
            configServiceImpl.set_config_value_impl(self, key, new_value, self.config)
        except (TypeError, KeyError):
            raise KeyError(f"The key '{key}' does not exist in the configuration file")

        """
        Save changes in the file
        """
        self.save_config()

    def save_config(self):
        """
        Save changes to the configuration file
        """
        try:
            configServiceImpl.save_config_impl(self.config_file_path, self.config)
        except Exception as e:
            raise Exception(f"Error while saving the configuration file: {str(e)}")
