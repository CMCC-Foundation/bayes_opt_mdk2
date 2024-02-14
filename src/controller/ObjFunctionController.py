# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import numpy as np

from src.service.BayOptSetupService import BayOptSetupService
from src.service.ExecutionService import ExecutionService
from src.service.MDK2SimParamsService import MDK2SimParamsService
from src.service.MetricsService import MetricsService

from src.controller.PathController import PathController

class ObjFunctionController:
    
    def __init__(self):
        """ Initializes multiple instances of workflow-related services and controllers with the same configuration file """
                
        self.bay_opt_setup_service_instance = BayOptSetupService()
        self.execution_service_instance = ExecutionService()
        self.mdk2_sim_params_service_instance = MDK2SimParamsService()
        self.path_controller_instance = PathController()
        self.metrics_service_instance = MetricsService()
        
    def objective_function(self, **kwargs):
        
        """
        Gets accuracy from the configuration of the Bayesian optimization service
        """
        decimal_precision = self.bay_opt_setup_service_instance.get_decimal_precision()
        particles_dict = self.mdk2_sim_params_service_instance.get_particles_key_value_dict()
        
        """
        Round input parameter values to the desired decimal precision
        """
        kwargs = {k:round(np.float32(v), decimal_precision) for k,v in kwargs.items()}
        pt = {k:int(v) for k,v in particles_dict.items()}
        
        config2_params = {**kwargs, **pt}
        
        """
        Create the directory for simulation cases, if it does not exist
        """
        self.path_controller_instance.create_cases_dir()
        
        """
        Update the model configuration file with the new rounded parameters
        """
        self.execution_service_instance.update_config2(config2_params, src=self.path_controller_instance.get_CONFIG2_TEMPLATE(), dst=self.path_controller_instance.get_CONFIG2())

        """
        MEDSLIK II
        Model launcher for try new parameter returned from Bayesian Optimization
        """
        self.execution_service_instance.run_model()
        
        """
        Compute and returns the value of the FSS (Fraction Skill Score) metric
        """
        FSS = self.metrics_service_instance.compute_multi_fss_service()

        """
        Saves the best detection obtained using the execution service
        """
        self.execution_service_instance.save_best_detection(FSS)
        
        """
        Prepares the values to be written into the final file, including the values passed as arguments (kwargs) and the FSS value
        """
        values_to_write = list(kwargs.values()) + [str(FSS)]
        
        """
        Writes the prepared values into the final file, using the path controller to determine the simulation result directory
        """
        self.path_controller_instance.write_final_result_file(values_to_write, self.path_controller_instance.get_sim_result_dir())
    
        return FSS