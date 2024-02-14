# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.domain.MDK2SimExtent import MDK2SimExtent
from src.service.ConfigService import ConfigService

class MDK2SimExtentDTO:
    
    def __init__(self):
        """ Initialize the MDK2SimExtent instance using the values obtained from the configuration file """
        
        self.config_service = ConfigService()
        
        self.mdk2_sim_extent_instance = MDK2SimExtent(
            SIM_NAME = self.config_service.get_config_value('medslik2.sim_extent.SIM_NAME'),
            sim_length = self.config_service.get_config_value('medslik2.sim_extent.sim_length'),
            duration = self.config_service.get_config_value('medslik2.sim_extent.duration'),
            spillrate = self.config_service.get_config_value('medslik2.sim_extent.spillrate'),
            age = self.config_service.get_config_value('medslik2.sim_extent.age'),
            grid_size = self.config_service.get_config_value('medslik2.sim_extent.grid_size'),
            oil_api = self.config_service.get_config_value('medslik2.sim_extent.oil_api'),
            oil_volume = self.config_service.get_config_value('medslik2.sim_extent.oil_volume'),
            number_slick = self.config_service.get_config_value('medslik2.sim_extent.number_slick'),
            config_service = self.config_service
        )
        
    """
    Getter and setter methods for returning or setting parameter values by calling terms defined in the model class 
    while handling exceptions
    """
        
    def get_SIM_NAME(self):
        try:
            return self.mdk2_sim_extent_instance.get_SIM_NAME
        except(TypeError, KeyError):
            return None
        
    def get_sim_length(self):
        try:
            return self.mdk2_sim_extent_instance.get_sim_length
        except(TypeError, KeyError):
            return None
        
    def get_duration(self):
        try:
            return self.mdk2_sim_extent_instance.get_duration
        except(TypeError, KeyError):
            return None
        
    def get_spillrate(self):
        try:
            return self.mdk2_sim_extent_instance.get_spillrate
        except(TypeError, KeyError):
            return None
        
    def get_age(self):
        try:
            return self.mdk2_sim_extent_instance.get_age
        except(TypeError, KeyError):
            return None
        
    def get_grid_size(self):
        try:
            return self.mdk2_sim_extent_instance.get_grid_size
        except(TypeError, KeyError):
            return None
        
    def get_oil_api(self):
        try:
            return self.mdk2_sim_extent_instance.get_oil_api
        except(TypeError, KeyError):
            return None
        
    def get_oil_volume(self):
        try:
            return self.mdk2_sim_extent_instance.get_oil_volume
        except(TypeError, KeyError):
            return None
        
    def get_number_slick(self):
        try:
            return self.mdk2_sim_extent_instance.get_number_slick
        except(TypeError, KeyError):
            return None