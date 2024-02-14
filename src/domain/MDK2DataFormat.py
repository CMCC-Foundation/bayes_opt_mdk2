# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.service.ConfigService import ConfigService

class MDK2DataFormat:

    def __init__(self, data_type: str, time_resolution: str, process_files: str,
                 config_service: ConfigService):
        """ Initialize class with specified parameters """
        
        self._data_type = data_type
        self._time_resolution = time_resolution
        self._process_files = process_files
        self._config_service = config_service

    """
    Getter and setter methods to return or set values related to the class
    """

    @property
    def get_data_type(self):
        return self._data_type
    
    @get_data_type.setter
    def set_data_type(self, value):
        self._data_type = value

    @property
    def get_time_resolution(self):
        return self._time_resolution
    
    @get_time_resolution.setter
    def set_time_resolution(self, value):
        self._time_resolution = value

    @property
    def get_process_files(self):
        return self._process_files
    
    @get_process_files.setter
    def set_process_files(self, value):
        self._process_files = value
        
    @property
    def get_config_service(self):
        return self._config_service
    
    @get_config_service.setter
    def set_config_service(self, value):
        self._config_service = value
