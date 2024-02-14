# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.service.ConfigService import ConfigService

class MDK2SimCoords:

    def __init__(self, lat_degree: int, lat_minutes: float,
                 lon_degree: int, lon_minutes: float, delta: float,
                 config_service: ConfigService):
        """ Initialize class with specified parameters """
        
        self._lat_degree = lat_degree
        self._lat_minutes = lat_minutes
        self._lon_degree = lon_degree
        self._lon_minutes = lon_minutes
        self._delta = delta
        self._config_service = config_service

    """
    Getter and setter methods to return or set values related to the class
    """

    @property
    def get_lat_degree(self):
        return self._lat_degree
    
    @get_lat_degree.setter
    def set_lat_degree(self, value):
        self._lat_degree = value

    @property
    def get_lat_minutes(self):
        return self._lat_minutes
    
    @get_lat_minutes.setter
    def set_lat_minutes(self, value):
        self._lat_minutes = value

    @property
    def get_lon_degree(self):
        return self._lon_degree
    
    @get_lon_degree.setter
    def set_lon_degree(self, value):
        self._lon_degree = value

    @property
    def get_lon_minutes(self):
        return self._lon_minutes
    
    @get_lon_minutes.setter
    def set_lon_minutes(self, value):
        self._lon_minutes = value

    @property
    def get_delta(self):
        return self._delta
    
    @get_delta.setter
    def set_delta(self, value):
        self._delta = value
        
    @property
    def get_config_service(self):
        return self._config_service
    
    @get_config_service.setter
    def set_config_service(self, value):
        self._config_service = value
