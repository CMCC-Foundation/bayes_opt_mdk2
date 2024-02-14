# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.service.ConfigService import ConfigService

class MDK2SimParams:

    def __init__(self, params:list, k: list, v: list, kparticles: str, vparticles: int, config_service: ConfigService):
        """ Initialize class with specified parameters """        

        self._params = params
        self._k = k
        self._v = v
        self._kparticles = kparticles
        self._vparticles = vparticles
        self._config_service = config_service
        
    """
    Getter and setter methods to return or set values related to the class
    """
        
    @property
    def get_params(self):
        return self._params
    
    @get_params.setter
    def set_params(self, value):
        self._params = value

    @property
    def get_k(self):
        return self._k
    
    @get_k.setter
    def set_k(self, value):
        self._k = value

    @property
    def get_v(self):
        return self._v
    
    @get_v.setter
    def set_v(self, value):
        self._v = value

    @property
    def get_kparticles(self):
        return self._kparticles
    
    @get_kparticles.setter
    def set_kparticles(self, value):
        self._kparticles = value

    @property
    def get_vparticles(self):
        return self._vparticles
    
    @get_vparticles.setter
    def set_vparticles(self, value):
        self._vparticles = value
        
    @property
    def get_config_service(self):
        return self._config_service
    
    @get_config_service.setter
    def set_config_service(self, value):
        self._config_service = value
