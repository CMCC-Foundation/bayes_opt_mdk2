# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.BayOptSetupServiceImpl import BayOptSetupServiceImpl

class BayOptSetupService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.bay_opt_setup_service_impl_instance = BayOptSetupServiceImpl()
        
    """
    Recalls the implementation method to obtain the attributes present in the class by handling the exceptions
    """
    def get_eval_metric(self):
        try:
            return self.bay_opt_setup_service_impl_instance.get_eval_metric_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_init_points(self):
        try:
            return self.bay_opt_setup_service_impl_instance.get_init_points_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_n_iter(self):
        try:
            return self.bay_opt_setup_service_impl_instance.get_n_iter_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None        
    
    def get_random_state(self):
        try:
            random_state = self.bay_opt_setup_service_impl_instance.get_random_state_impl()
            return random_state
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_decimal_precision(self):
        try:
            decimal_precision = self.bay_opt_setup_service_impl_instance.get_decimal_precision_impl()
            return decimal_precision
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
            
        
    def get_verbose(self):
        try:
            verbose = self.bay_opt_setup_service_impl_instance.get_verbose_impl()
            return verbose
        except Exception as e:
            print(f"An error occurred: {e}")
            return None