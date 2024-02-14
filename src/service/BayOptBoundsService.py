# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.BayOptBoundsServiceImpl import BayOptBoundsServiceImpl

class BayOptBoundsService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.bay_opt_bounds_service_impl_instance = BayOptBoundsServiceImpl()
    
    """
    Recalls the implementation method to obtain the attributes present in the class by handling the exceptions
    """

    def get_parameter_bounds_dict(self):
        try:
            parameters_bound = self.bay_opt_bounds_service_impl_instance.get_parameter_bounds_dict_impl()
            return parameters_bound
        except Exception as e:
            print(f"An error occurred: {e}")
            return None