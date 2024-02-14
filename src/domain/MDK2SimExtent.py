# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.service.ConfigService import ConfigService

class MDK2SimExtent:

    def __init__(self, SIM_NAME: str, sim_length: str, duration: str,
                 spillrate: str, age: str, grid_size: str,
                 oil_api: float, oil_volume: float, number_slick: int,
                 config_service = ConfigService):
        """ Initialize class with specified parameters """
        
        self._SIM_NAME = SIM_NAME
        self._sim_length = sim_length
        self._duration = duration
        self._spillrate = spillrate
        self._age = age
        self._grid_size = grid_size
        self._oil_api = oil_api
        self._oil_volume = oil_volume
        self._number_slick = number_slick
        self._config_service = config_service
        
    """
    Getter and setter methods to return or set values related to the class
    """

    @property
    def get_SIM_NAME(self):
        return self._SIM_NAME
    
    @get_SIM_NAME.setter
    def set_SIM_NAME(self, value):
        self._SIM_NAME = value

    @property
    def get_sim_length(self):
        return self._sim_length
    
    @get_sim_length.setter
    def set_sim_length(self, value):
        self._sim_length = value

    @property
    def get_duration(self):
        return self._duration
    
    @get_duration.setter
    def set_duration(self, value):
        self._duration = value

    @property
    def get_spillrate(self):
        return self._spillrate
    
    @get_spillrate.setter
    def set_spillrate(self, value):
        self._spillrate = value

    @property
    def get_age(self):
        return self._age
    
    @get_age.setter
    def set_age(self, value):
        self._age = value

    @property
    def get_grid_size(self):
        return self._grid_size
    
    @get_grid_size.setter
    def set_grid_size(self, value):
        self._grid_size = value

    @property
    def get_oil_api(self):
        return self._oil_api
    
    @get_oil_api.setter
    def set_oil_api(self, value):
        self._oil_api = value

    @property
    def get_oil_volume(self):
        return self._oil_volume
    
    @get_oil_volume.setter
    def set_oil_volume(self, value):
        self._oil_volume = value

    @property
    def get_number_slick(self):
        return self._number_slick
    
    @get_number_slick.setter
    def set_number_slick(self, value):
        self._number_slick = value

    @property
    def get_config_service(self):
        return self._config_service
    
    @get_config_service.setter
    def set_config_service(self, value):
        self._config_service = value
