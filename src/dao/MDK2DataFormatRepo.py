# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.service.ConfigService import ConfigService

class MDK2DataFormatRepo:
    
    def __init__(self):
        """ Initializes multiple instances of workflow-related services and controllers with the same configuration file """
        
        self.config_instance = ConfigService()
                
    """
    Returns all coordinate-related parameters from the 'medslik2.data_format' configuration section
    """
    def get_all_params(self):
        return self.config_instance.get_config_value('medslik2.data_format')