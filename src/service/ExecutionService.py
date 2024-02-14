# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.ExecutionServiceImpl import ExecutionServiceImpl
from src.exception.UpdateConfigException import UpdateConfigException
from src.exception.WrongConfigurationException import WrongConfigurationException


class ExecutionService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.execution_service_impl_instance = ExecutionServiceImpl()
        self.update_config_exception_instance = UpdateConfigException()
    
    """
    Invokes the method that update the configuration using the specific implementation by handling its exceptions
    """
    def update_config2(self, config_dict, src, dst):
        try:
            self.execution_service_impl_instance.update_config2_impl(config_dict, src, dst)
        except UpdateConfigException as e:
            print(f"Error: {e}")
    
    """
    Invokes the method that compile the model using the specific implementation by handling its exceptions
    """
    def compile_model(self):
        try:
            self.execution_service_impl_instance.compile_model()
        except WrongConfigurationException as e:
            print(f"Error: {e}")

    """
    Invokes the method that runs the model using the specific implementation by handling its exceptions
    """            
    def run_model(self):
        try:
            self.execution_service_impl_instance.run_model()
        except WrongConfigurationException as e:
            print(f"Error: {e}")
            
    def save_best_detection(self, value):
        try:
            self.execution_service_impl_instance.save_best_detection_impl(value)
        except WrongConfigurationException as e:
            print(f"Error: {e}")