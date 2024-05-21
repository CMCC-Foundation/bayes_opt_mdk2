# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.dto.BayOptSetupDTO import BayOptSetupDTO

class BayOptSetupServiceImpl:
    
    def __init__(self):
        """ Initializes DTO and services instances useful for method development """
        
        self.bay_opt_setup_dto_instance = BayOptSetupDTO()
        
    """
    Get useful parameters using the appropriate instances
    """
    def get_eval_metric_impl(self):
        return self.bay_opt_setup_dto_instance.get_eval_metric()

    def get_init_points_impl(self):
        return self.bay_opt_setup_dto_instance.get_init_points()
    
    def get_n_iter_impl(self):
        return self.bay_opt_setup_dto_instance.get_n_iter()
    
    def get_random_state_impl(self):
        return self.bay_opt_setup_dto_instance.get_random_state()
    
    def get_decimal_precision_impl(self):
        return self.bay_opt_setup_dto_instance.get_decimal_precision()
    
    def get_verbose_impl(self):
        return self.bay_opt_setup_dto_instance.get_verbose()