# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.domain.MDK2SimCoords import MDK2SimCoords
from src.service.ConfigService import ConfigService

class MDK2SimCoordsDTO:
    
    def __init__(self):
        """ Initialize the MDK2SimCoords instance using the values obtained from the configuration file """
        
        self.config_service = ConfigService()
        
        self.mdk2_sim_coords_service_instance = MDK2SimCoords(
            lat_degree = self.config_service.get_config_value('medslik2.sim_coords.lat_degree'),
            lat_minutes = self.config_service.get_config_value('medslik2.sim_coords.lat_minutes'),
            lon_degree = self.config_service.get_config_value('medslik2.sim_coords.lon_degree'),
            lon_minutes = self.config_service.get_config_value('medslik2.sim_coords.lon_minutes'),
            delta = self.config_service.get_config_value('medslik2.sim_coords.delta'),
            config_service = self.config_service
        )

    """
    Getter and setter methods for returning or setting parameter values by calling terms defined in the model class 
    while handling exceptions
    """
        
    def get_lat_degree(self):
        try:
            return self.mdk2_sim_coords_service_instance.get_lat_degree
        except(TypeError, KeyError):
            return None
        
    def get_lat_minutes(self):
        try:
            return self.mdk2_sim_coords_service_instance.get_lat_minutes
        except(TypeError, KeyError):
            return None
        
    def get_lon_degree(self):
        try:
            return self.mdk2_sim_coords_service_instance.get_lon_degree
        except(TypeError, KeyError):
            return None
        
    def get_lon_minutes(self):
        try:
            return self.mdk2_sim_coords_service_instance.get_lon_minutes
        except(TypeError, KeyError):
            return None
        
    def get_delta(self):
        try:
            return self.mdk2_sim_coords_service_instance.get_delta
        except(TypeError, KeyError):
            return None