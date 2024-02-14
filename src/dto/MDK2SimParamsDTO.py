# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.domain.MDK2SimParams import MDK2SimParams
from src.service.ConfigService import ConfigService

class MDK2SimParamsDTO:
    
    def __init__(self):
        """ Initialize the MDK2SimParams instance using the values obtained from the configuration file """
        
        self.config_service = ConfigService()
        
        self.mdk2_sim_params_instance = MDK2SimParams(
            params = self.config_service.get_config_value('medslik2.sim_params.params'),
            k = self.config_service.get_config_value('medslik2.sim_params.k'),
            v = self.config_service.get_config_value('medslik2.sim_params.v'),
            kparticles = self.config_service.get_config_value('medslik2.sim_params.kparticles'),
            vparticles = self.config_service.get_config_value('medslik2.sim_params.vparticles'),
            config_service = self.config_service
        )
        
    """
    Getter and setter methods for returning or setting parameter values by calling terms defined in the model class 
    while handling exceptions
    """
    
    def get_params(self):
        try:
            return self.mdk2_sim_params_instance.get_params
        except(TypeError, KeyError):
            return None
        
    def get_k(self):
        try:
            return self.mdk2_sim_params_instance.get_k
        except(TypeError, KeyError):
            return None
        
    def get_v(self):
        try:
            return self.mdk2_sim_params_instance.get_v
        except(TypeError, KeyError):
            return None
        
    def get_kparticles(self):
        try:
            return self.mdk2_sim_params_instance.get_kparticles
        except(TypeError, KeyError):
            return None
        
    def get_vparticles(self):
        try:
            return self.mdk2_sim_params_instance.get_vparticles
        except(TypeError, KeyError):
            return None