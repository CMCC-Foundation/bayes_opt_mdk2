# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.domain.BayOptSetup import BayOptSetup
from src.service.ConfigService import ConfigService

class BayOptSetupDTO:
    
    def __init__(self):
        """ Initialize the BayOptSetup instance using the values obtained from the configuration file """
        
        self.config_service = ConfigService()
        
        self.bay_opt_setup_instance = BayOptSetup(
            eval_metric = self.config_service.get_config_value('bayesian_optimization.setup.eval_metric'),
            init_points = self.config_service.get_config_value('bayesian_optimization.setup.init_points'),
            n_iter = self.config_service.get_config_value('bayesian_optimization.setup.n_iter'),
            random_state = self.config_service.get_config_value('bayesian_optimization.setup.random_state'),
            decimal_precision = self.config_service.get_config_value('bayesian_optimization.setup.decimal_precision'),
            verbose = self.config_service.get_config_value('bayesian_optimization.setup.verbose'),
            config_service = self.config_service
        )
        
    """
    Getter and setter methods for returning or setting parameter values by calling terms defined in the model class 
    while handling exceptions
    """
    
    def get_eval_metric(self):
        try:
            return self.bay_opt_setup_instance.get_eval_metric
        except (TypeError, KeyError):
            return None
        
    def set_eval_metric(self, value):
        try:
            return self.config_service.set_config_value('bayesian_optimization.setup.eval_metric', value)
        except (TypeError, KeyError):
            raise KeyError("Error while setting the value of 'b'")
        
    def get_init_points(self):
        try:
            return self.bay_opt_setup_instance.get_init_points
        except (TypeError, KeyError):
            return None
        
    def get_n_iter(self):
        try:
            return self.bay_opt_setup_instance.get_n_iter
        except (TypeError, KeyError):
            return None
        
    def get_random_state(self):
        try:
            return self.bay_opt_setup_instance.get_random_state
        except (TypeError, KeyError):
            return None
        
    def get_decimal_precision(self):
        try:
            return self.bay_opt_setup_instance.get_decimal_precision
        except (TypeError, KeyError):
            return None
        
    def get_verbose(self):
        try:
            return self.bay_opt_setup_instance.get_verbose
        except (TypeError, KeyError):
            return None