# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import typing as t

from src.service.ConfigService import ConfigService

class BayOptBounds:
    
    def __init__(self, b: t.Dict,
                 config_service = ConfigService):
        """ Initialize class with specified parameters """
        
        self._b = b
        self.config_service = config_service

    """
    Getter and setter methods to return or set values related to the class
    """
    
    @property
    def get_b(self):
        return self._b
    
    @get_b.setter
    def set_b(self, value: t.Dict):
        self._b = value