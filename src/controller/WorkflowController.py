# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from enum import Enum

from src.service.BayOptSetupService import BayOptSetupService
from src.service.MDK2SimCoordsService import MDK2SimCoordsService
from src.service.MDK2SimDateService import MDK2SimDateService
from src.service.MDK2SimExtentService import MDK2SimExtentService
from src.service.MDK2SimParamsService import MDK2SimParamsService
from src.service.WorkflowService import WorkflowService

from src.controller.PathController import PathController
from src.controller.ObjFunctionController import ObjFunctionController

from src.exception.WrongConfigurationException import WrongConfigurationException
from src.exception.SetupException import SetupException
from src.exception.RunException import RunException

"""
Specifying valid execution types
"""
class ExecutionType(Enum):
    BAYES_OPT = 0
    MEDSLIK = 1

class WorkflowController:
    
    def __init__(self):
        """ Initializes multiple instances of workflow-related services and controllers with the same configuration file """
                
        self.bay_opt_setup_service_instance = BayOptSetupService()
        self.mdk2_sim_extent_service_instance = MDK2SimExtentService()
        self.mdk2_sim_date_service_instance = MDK2SimDateService()
        self.mdk2_sim_coords_service_instance = MDK2SimCoordsService()
        self.mdk2_sim_params_service_instance = MDK2SimParamsService()
        self.workflow_service_instance = WorkflowService()
        
        self.path_controller_instance = PathController()
        self.obj_function_controller_instance = ObjFunctionController()
        
    """
    Checks whether the specified value is among the valid ones. If not, raises an exception with the valid values
    """
    def check_execution_type(self, execution_type):
        execution_values = set(member.value for member in ExecutionType)

        if execution_type not in execution_values:
            enum_values = {name: member.value for name, member in ExecutionType.__members__.items()}
            raise WrongConfigurationException(f"The specified value is not among the valid values of ExecutionType, the accepted modes are: {enum_values}")
    
    """
    Call to the setup_service method from the WorkflowServiceInstance class with the specified execution type
    """
    def setup(self, execution_type:int):
        try:
            return self.workflow_service_instance.setup_service(execution_type)
        except ValueError as e:
            raise SetupException(e)
            
    """
    Call to the run_service method from the WorkflowServiceInstance class with the specified parameters
    """
    def run(self, execution_type:int, parameters_bound, random_state, verbose):
        try:
            return self.workflow_service_instance.run_service(execution_type, parameters_bound, random_state, verbose)
        except ValueError as e:
            raise RunException(e)