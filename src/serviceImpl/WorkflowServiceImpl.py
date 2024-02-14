# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from enum import Enum
import numpy as np
import typing as t

from library.bayesian_optimization_core.bayes_opt.bayesian_optimization import BayesianOptimization

from src.service.BayOptSetupService import BayOptSetupService
from src.service.MDK2SimCoordsService import MDK2SimCoordsService
from src.service.MDK2SimDateService import MDK2SimDateService
from src.service.MDK2SimExtentService import MDK2SimExtentService
from src.service.MDK2SimParamsService import MDK2SimParamsService
from src.service.ExecutionService import ExecutionService
from src.service.MetricsService import MetricsService

from src.controller.PathController import PathController
from src.controller.ObjFunctionController import ObjFunctionController

from src.exception.WrongConfigurationException import WrongConfigurationException

from simulation.gen_mdk2_sim import Gen_Mdk2_Sim

class ExecutionType(Enum):
    BAYESOPT = 0
    MEDSLIK = 1

class WorkflowServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
                
        self.bay_opt_setup_service_instance = BayOptSetupService()
        self.mdk2_sim_extent_service_instance = MDK2SimExtentService()
        self.mdk2_sim_date_service_instance = MDK2SimDateService()
        self.mdk2_sim_coords_service_instance = MDK2SimCoordsService()
        self.mdk2_sim_params_service_instance = MDK2SimParamsService()
        self.execution_service_instance = ExecutionService()
        self.metrics_service_instance = MetricsService()
        
        self.path_controller_instance = PathController()
        self.obj_function_controller_instance = ObjFunctionController()
        
        self.gen_mdk2_sim_instance = Gen_Mdk2_Sim()
        
    def get_execution_type_name_impl(self, value):
        for et in ExecutionType:
            if et.value == value:
                return et.name
        return None
        
    def check_execution_type_service_impl(self, execution_type):
        """
        Verifies if the specified execution type is valid.

        Args:
            execution_type (int): The execution type to be checked.

        Raises:
            WrongConfigurationException: If the specified value is not among the valid values
            of ExecutionType. The accepted modes are printed in the error message.
        """
        
        """
        Ottiene l'insieme di valori validi dall'enumerazione ExecutionType.
        """
        execution_values = set(member.value for member in ExecutionType)

        if execution_type not in execution_values:
            enum_values = {name: member.value for name, member in ExecutionType.__members__.items()}
            raise WrongConfigurationException(f"The specified value is not among the valid values of ExecutionType, the accepted modes are: {enum_values}")
        
    def setup_service_impl(self, execution_type:int):
        """
        Sets up the workflow based on the specified execution type.

        Args:
            execution_type (int): The execution type to determine the workflow setup.

        Raises:
            ValueError: If the execution type is not recognized.
        """
        
        """
        Retrieves needed parameters from service instances
        """
        sim_extent = self.mdk2_sim_extent_service_instance.get_sim_extent_params_dict()
        sim_date = self.mdk2_sim_date_service_instance.get_sim_date_params_dict()
        sim_coords = self.mdk2_sim_coords_service_instance.get_sim_coords_params_dict()
        decimal_precision = self.bay_opt_setup_service_instance.get_decimal_precision()
        
        """
        Combine parameters to configure different parts of the workflow
        """
        # TODO: non servono più?
        config1_params: t.Dict = dict(**sim_extent, **sim_date, **sim_coords)
        # config2_params: t.Dict = dict(**sim_params, **sim_particles)
        
        self.execution_type: int = execution_type
        
        if (self.execution_type == ExecutionType.BAYESOPT.value):
                        
            # gather and process OCE and MET fields for setting-up the simulation
            print('> Gather and process OCE and MET fields for the oil spill ...')
            self.gen_mdk2_sim_instance.gen_mdk2_sim()
            
            """
            compile MEDSLIK-II
            """
            self.execution_service_instance.compile_model()

            """
            Return the best result found by Bayesian Optimization
            """
            #find_max(Path.WORKFLOW_FOLDER + Path.FINAL_FSS_RESULT_FILE)

        
        elif (self.execution_type == ExecutionType.MEDSLIK.value):
            print('*** Execution type : MEDSLIK-II simulation ***')
            
            # gather and process OCE and MET fields for setting-up the simulation
            print('> Gather and process OCE and MET fields for the oil spill ...')
            self.gen_mdk2_sim_instance.gen_mdk2_sim()
            
            params = self.mdk2_sim_params_service_instance.get_sim_params_kv_dict()
            particles_dict = self.mdk2_sim_params_service_instance.get_particles_key_value_dict()
            args = {k:round(np.float32(v), decimal_precision) for k,v in params.items()}
            pt = {k:int(v) for k,v in particles_dict.items()}
            
            config2_params = {**args, **pt}
            
            #update_config1(self.config1_params, src=Path.CONFIG1_TEMPLATE, dst=Path.CONFIG1)
            self.execution_service_instance.update_config2(config2_params, src=self.path_controller_instance.get_CONFIG2_TEMPLATE(), dst=self.path_controller_instance.get_CONFIG2())

            """
            compile MEDSLIK-II
            """
            self.execution_service_instance.compile_model()
            
    def run_service_impl(self, execution_type:int, parameters_bound, random_state, verbose):
        """Runs the workflow based on the specified execution type.

        Args:
            execution_type (int): The execution type to determine the workflow run.
            parameters_bound (dict): Dictionary defining the bounds for Bayesian Optimization.
            random_state (int): Seed for random number generation in Bayesian Optimization.
            verbose (int): Verbosity level for the optimization process.

        Raises:
            ValueError: If the execution type is not recognized.
        """
        
        """
        Set the execution type
        """
        self.execution_type: int = execution_type
        
        """
        Retrieve simulation parameters
        """
        sim_params = self.mdk2_sim_params_service_instance.get_sim_params_keys_values_dict()
        init_points_val = self.bay_opt_setup_service_instance.get_init_points()
        n_iter_val = self.bay_opt_setup_service_instance.get_n_iter()
        
        if (self.execution_type == ExecutionType.BAYESOPT.value):
            
            self.path_controller_instance.create_final_result_file_and_result_dir(self.path_controller_instance.get_sim_result_dir())
            
            """
            Definition of the optimizer that performs the Bayesian Optimization
            """
            optimizer = BayesianOptimization(
                f=self.obj_function_controller_instance.objective_function,
                pbounds=parameters_bound,
                random_state=random_state,
                verbose=verbose
            )

            """
            Launch the maximize function who try to find better parameters for the simulation
            """
            optimizer.probe(sim_params, lazy=True)
            optimizer.maximize(init_points=init_points_val, n_iter=n_iter_val)
            
            self.path_controller_instance.remove_old_detection_directories(self.path_controller_instance.get_sim_result_dir(), "detection_")
            
        elif (self.execution_type == ExecutionType.MEDSLIK.value):
            
            """
            Runs the MEDSLIK-II model
            """
            self.execution_service_instance.run_model()
            FSS = self.metrics_service_instance.compute_multi_fss_service()
            # print(FSS)