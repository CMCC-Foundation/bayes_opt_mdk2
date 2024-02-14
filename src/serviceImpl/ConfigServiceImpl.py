# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import toml

class configServiceImpl:
    
    @staticmethod
    def load_config_impl(config_file_path):
        """
        Loads the configuration from the specified file using the toml module
    
        Parameters:
            config_file_path (str): The file path to the TOML configuration file.

        Returns:
            dict: A dictionary representing the configuration loaded from the file.
        """
        
        with open(config_file_path, "r") as file:
            return toml.load(file)
    
    @staticmethod
    def get_config_value_impl(config, key):
        """
        Gets the value associated with a specific key in the configuration
        
        Parameters:
            config (dict): The nested configuration dictionary.
            key (str): The key whose associated value is to be retrieved, possibly containing dots for nested dictionaries.

        Returns:
            The value associated with the specified key or None if the key is not found.
        """
        
        if config is not None:
            keys = key.split('.')
            for k in keys:
                config = config[k]
            return config
        else:
            return None
    

    @staticmethod
    def set_config_value_impl(self, key, new_value, config):
        """
        Sets the new value associated with a specific key in the configuration
            
        Parameters:
            self: The current instance of the class.
            key (str): The key to be modified, possibly containing dots for nested dictionaries.
            new_value: The new value to be assigned to the specified key.
            config (dict): The nested configuration dictionary.

        Raises:
            KeyError: If the specified key does not exist in the configuration.

        """
        
        keys = key.split('.')
        for k in keys[:-1]:
            config = config[k]
        config[keys[-1]] = new_value

    @staticmethod
    def save_config_impl(config_file_path, config):
        """
        Saves the configuration to the specified file using the toml module
            
        Parameters:
            config_file_path (str): The file path where the configuration will be saved.
            config (dict): The configuration dictionary to be saved.

        Raises:
            Exception: If an error occurs during the saving process.
        """
        
        with open(config_file_path, "w") as file:
            toml.dump(config, file)
