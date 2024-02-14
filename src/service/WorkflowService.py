# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.WorkflowServiceImpl import WorkflowServiceImpl

from src.exception.SetupException import SetupException
from src.exception.RunException import RunException

class WorkflowService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.workflow_service_impl_instance = WorkflowServiceImpl()
        
    def get_execution_type_name(self, value):
        try:
            self.workflow_service_impl_instance.get_execution_type_name_impl(value)
        except ValueError as e:
            print(f"Error during paramenters check: {e}")
    
    """
    Checks the type of execution using the specific implementation by handling error
    """   
    def check_execution_type_service(self, execution_type):
        try:
            self.workflow_service_impl_instance.check_execution_type_service_impl(execution_type)
        except ValueError as e:
            print(f"Error during paramenters check: {e}")
    
    """
    Performs model setup using the specific implementation by handling its errors
    """
    def setup_service(self, execution_type:int):
        try:
            self.workflow_service_impl_instance.setup_service_impl(execution_type)
        except ValueError as e:
            raise SetupException(e)
    
    """
    Runs the model using the specific implementation by handling its errors
    """
    def run_service(self, execution_type:int, parameters_bound, random_state, verbose):
        try:
            self.workflow_service_impl_instance.run_service_impl(execution_type, parameters_bound, random_state, verbose)
        except ValueError as e:
            raise RunException(e)