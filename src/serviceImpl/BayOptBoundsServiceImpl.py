# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.dto.BayOptBoundsDTO import BayOptBoundsDTO
from src.dto.MDK2SimParamsDTO import MDK2SimParamsDTO

class BayOptBoundsServiceImpl:
    
    def __init__(self):
        """ Initializes DTO and services instances useful for method development """
                
        self.bay_opt_bounds_dto_instance = BayOptBoundsDTO()
        self.mdk2_sim_params_dto_instance = MDK2SimParamsDTO()
        
    """
    Get parameter bounds using appropriate instances
    """
    
    def get_parameter_bounds_dict_impl(self):
        return dict(zip(self.mdk2_sim_params_dto_instance.get_k(), self.bay_opt_bounds_dto_instance.get_b()))