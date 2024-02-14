# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.domain.BayOptBounds import BayOptBounds
from src.service.ConfigService import ConfigService
    
class BayOptBoundsDTO:
    
    def __init__(self):
        """ Initialize the BayOptBounds instance using the values obtained from the configuration file """
        
        self.config_service = ConfigService()
        
        self.bay_opt_bounds_instance = BayOptBounds(
            b = self.config_service.get_config_value('bayesian_optimization.b'),
            config_service=self.config_service
        )
        
    """
    Getter and setter methods for returning or setting parameter values by calling terms defined in the model class 
    while handling exceptions
    """
        
    def get_b(self):
        try:
            return self.bay_opt_bounds_instance.get_b
        except (TypeError, KeyError):
            return None
        
    def set_b(self, values):
        try:
            self.config_service.set_config_value('bayesian_optimization.b', values)
        except (TypeError, KeyError):
            raise KeyError("Error when setting value of 'b'.")