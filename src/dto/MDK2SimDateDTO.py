# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.domain.MDK2SimDate import MDK2SimDate
from src.service.ConfigService import ConfigService

class MDK2SimDateDTO:
    
    def __init__(self):
        """ Initialize the MDK2SimDate instance using the values obtained from the configuration file """
        
        self.config_service = ConfigService()
        
        self.mdk2_sim_date_instance = MDK2SimDate(
            day = self.config_service.get_config_value('medslik2.sim_date.day'),
            month = self.config_service.get_config_value('medslik2.sim_date.month'),
            year = self.config_service.get_config_value('medslik2.sim_date.year'),
            hour = self.config_service.get_config_value('medslik2.sim_date.hour'),
            minutes = self.config_service.get_config_value('medslik2.sim_date.minutes'),
            config_service = self.config_service
        )

    """
    Getter and setter methods for returning or setting parameter values by calling terms defined in the model class 
    while handling exceptions
    """
       
    def get_day(self):
        try:
            return self.mdk2_sim_date_instance.get_day
        except(TypeError, KeyError):
            return None
        
    def get_month(self):
        try:
            return self.mdk2_sim_date_instance.get_month
        except(TypeError, KeyError):
            return None
        
    def get_year(self):
        try:
            return self.mdk2_sim_date_instance.get_year
        except(TypeError, KeyError):
            return None
        
    def get_hour(self):
        try:
            return self.mdk2_sim_date_instance.get_hour
        except(TypeError, KeyError):
            return None
        
    def get_minutes(self):
        try:
            return self.mdk2_sim_date_instance.get_minutes
        except(TypeError, KeyError):
            return None