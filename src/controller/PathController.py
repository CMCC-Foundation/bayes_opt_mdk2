# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import os
import time

from src.service.PathService import PathService
from src.service.MDK2SimDateService import MDK2SimDateService
from src.service.MDK2SimExtentService import MDK2SimExtentService
from src.service.MDK2SimParamsService import MDK2SimParamsService

timestamp = time.strftime('%Y%m%d-%H%M%S')

class PathController:
    
    def __init__(self):
        """ Initializes multiple instances of workflow-related services and controllers with the same configuration file """

        self.path_service_instance = PathService()
        self.mdk2_sim_date_service_instance = MDK2SimDateService()
        self.mdk2_sim_extent_service_instance = MDK2SimExtentService()
        self.mdk2_sim_params_service_instance = MDK2SimParamsService()
    
    """
    Creates the cases folder in case it does not exist
    """
    def create_cases_dir(self):
        dst_dir = f'{self.path_service_instance.get_CASES_path(), self.mdk2_sim_extent_service_instance.get_SIM_NAME()}'
        return os.makedirs(dst_dir, exist_ok=True)
    
    def create_final_result_file_and_result_dir(self, result_dir):
        """
        Creates a final result file and the associated result directory.

        Args:
            result_dir (str): The path to the result directory.
        """
        # Ensure that the result directory exists
        os.makedirs(result_dir, exist_ok=True)
        
        # Create a new path for the final result file using a timestamp
        new_path = os.path.join(result_dir, f'final_result_{timestamp}.csv')
        
        # Define the values to write to the final result file (including 'FSS')
        values_to_write = self.mdk2_sim_params_service_instance.get_config_keys()[::-1] + ['FSS']
        
        # Create the header string by joining the values with commas
        header = ','.join(map(str, values_to_write))
        
        # Write the header to the final result file
        with open(new_path, mode='w', newline='') as f:
            f.write(header)
            
    def write_final_result_file(self, values, result_dir):
        """
        Appends values to an existing final result file in the specified result directory.

        Args:
            values (list): List of values to append to the final result file.
            result_dir (str): The path to the result directory.
        """
        # Create a new path for the final result file using a timestamp
        new_path = os.path.join(result_dir, f'final_result_{timestamp}.csv')
        
        # Create the header string by joining the values with commas
        header = ','.join(map(str, values))
        
        # Append a newline and the header to the final result file
        with open(new_path, mode='a', newline='') as f:
            f.write("\n")
            f.write(header)

    def get_sim_str(self):
        """
        Generates a string representation of simulation parameters.

        Returns:
            str: String representation of simulation parameters.
        """
        # Obtain simulation date components
        year = self.mdk2_sim_date_service_instance.get_year()
        month = self.mdk2_sim_date_service_instance.get_month()
        day = self.mdk2_sim_date_service_instance.get_day()
        hour = self.mdk2_sim_date_service_instance.get_hour()
        minutes = self.mdk2_sim_date_service_instance.get_minutes()
        
        # Obtain simulation extent parameters
        duration = self.mdk2_sim_extent_service_instance.get_duration()
        grid_size = self.mdk2_sim_extent_service_instance.get_grid_size()
        sim_name = self.mdk2_sim_extent_service_instance.get_SIM_NAME()
        nparticles = self.mdk2_sim_params_service_instance.get_particles_value()
        
        # Construct the simulation string
        return f"MDK_BAYESOPT_SIM_20{year}_{month}_{day}_{hour}{minutes}_{duration}h_{grid_size}m_{nparticles}_{sim_name}_{timestamp}"
    
    def get_sim_result_dir(self):
        """
        Generates the simulation result directory path based on various parameters.

        Returns:
            str: The path to the simulation result directory.
        """
        sim_name = self.mdk2_sim_extent_service_instance.get_SIM_NAME()
        
        #exec_type = self.workflow_service_instance.get_execution_type_name(execution_type)
        
        sim_str = self.get_sim_str()
        
        return os.path.join(self.path_service_instance.get_CASES_path(), sim_name, sim_str)
    
    def get_detection_dir(self, obs):
        """
        Generates the complete path for storing detection data based on information 
        obtained from various service instances.

        Args:
            obs (int): Number of observation or detection.

        Returns:
            str: Complete path for storing detection data.
        """        
        obs_str = "detection_" + str(obs)
        
        return os.path.join(self.get_sim_result_dir(), obs_str)
    
    def get_simulation_result_file(self, result_dir):
        """
        Appends values to an existing final result file in the specified result directory.

        Args:
            values (list): List of values to append to the final result file.
            result_dir (str): The path to the result directory.
        """
        return os.path.join(result_dir, f'final_result_{timestamp}.csv')
        
    
    def copy_detection_directories_with_content(self, source_path, destination_path, prefix):
        """
        Copies detection directories with content from the source path to the destination path,
        filtering directories based on the given prefix.

        Args:
            source_path (str): The source path containing detection directories.
            destination_path (str): The destination path where detection directories will be copied.
            prefix (str): The prefix used to filter directories.
        """
        return self.path_service_instance.copy_detection_directories_with_content_service(source_path, destination_path, prefix)
                
    def remove_old_detection_directories(self, source_path, prefix):
        """
        Removes old detection directories from the specified source path
        based on the given prefix.

        Args:
            source_path (str): The source path containing detection directories.
            prefix (str): The prefix used to filter directories.
        """
        return self.path_service_instance.remove_old_detection_directories_service(source_path, prefix)
    
    """
    Creates the folder containing the observations of the various use cases in case it does not exist
    """
    def create_detection_dir(self, obs):
        return os.makedirs(self.get_detection_dir(str(obs)), exist_ok=True)
    
    """
    Methods for obtaining paths to various directories or files useful for workflow
    """
    
    def get_ROOT(self):
        return self.path_service_instance.get_ROOT_path()
    
    def get_MEDSLIK_FOLDER(self):
        return self.path_service_instance.get_MEDSLIK_FOLDER_path()
    
    def get_WORKFLOW_CONFIG(self):
        return self.path_service_instance.get_WORKFLOW_CONFIG_path()
    
    def get_CONFIG2_TEMPLATE(self):
        return self.path_service_instance.get_CONFIG2_TEMPLATE_path()
    
    def get_MEDSLIK_RUN(self):
        return self.path_service_instance.get_MEDSLIK_RUN_path()
    
    def get_MEDSLIK_MODEL_SRC(self):
        return self.path_service_instance.get_MEDSLIK_MODEL_SRC_path()
    
    def get_CONFIG1(self):
        return self.path_service_instance.get_CONFIG1_path()
    
    def get_CONFIG2(self):
        return self.path_service_instance.get_CONFIG2_path()
    
    def get_CASES(self):
        return self.path_service_instance.get_CASES_path()
    
    def get_OBS(self):
        """
        Constructs the path to the observation file based on simulation parameters.

        Returns:
            str: Path to the observation file.
        """
        # Obtain simulation parameters
        sim_name = self.mdk2_sim_extent_service_instance.get_SIM_NAME()
        
        day = self.mdk2_sim_date_service_instance.get_day()
        month = self.mdk2_sim_date_service_instance.get_month()
        year = self.mdk2_sim_date_service_instance.get_year()
        hour = self.mdk2_sim_date_service_instance.get_hour()
        minutes = self.mdk2_sim_date_service_instance.get_minutes()
        
        # Construct the path to the observation file using obtained parameters
        return os.path.join(self.path_service_instance.get_OBS_path(), f"{sim_name}", f"observations_20{year}_{month}_{day}_{hour}{minutes}")
    
    def get_DAYS_GROUP(self):
        return self.path_service_instance.get_DAYS_GROUP_path()
    
    def get_OUT_FOLDER(self):
        return self.path_service_instance.get_OUT_FOLDER_path()
    
    def get_MEDSLIK_OUT_DIR(self):
        """
        Constructs the path to the MEDSLIK output directory based on simulation parameters.

        Returns:
            str: Path to the MEDSLIK output directory.
        """
        # Obtain simulation parameters
        sim_name = self.mdk2_sim_extent_service_instance.get_SIM_NAME()
        
        day = self.mdk2_sim_date_service_instance.get_day()
        month = self.mdk2_sim_date_service_instance.get_month()
        year = self.mdk2_sim_date_service_instance.get_year()
        hour = self.mdk2_sim_date_service_instance.get_hour()
        minutes = self.mdk2_sim_date_service_instance.get_minutes()

        # Construct the path to the MEDSLIK output directory using obtained parameters
        return os.path.join(self.path_service_instance.get_MEDSLIK_OUT_DIR_path(), f"MDK_SIM_20{year}_{month}_{day}_{hour}{minutes}_{sim_name}")