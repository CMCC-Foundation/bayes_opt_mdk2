# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import os
import shutil

from src.dto.PathDTO import PathDTO

class PathServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
        
        self.path_dto_instance = PathDTO()
        
    """
    Get useful parameters using the appropriate instances
    """
    
    def get_ROOT_impl(self):
        return self.path_dto_instance.get_ROOT()
    
    def get_MEDSLIK_FOLDER_impl(self):
        return self.path_dto_instance.get_MEDSLIK_FOLDER()
    
    def get_WORKFLOW_CONFIG_impl(self):
        return self.path_dto_instance.get_WORKFLOW_CONFIG()
    
    def get_CONFIG2_TEMPLATE_impl(self):
        return self.path_dto_instance.get_CONFIG2_TEMPLATE()
    
    def get_MEDSLIK_RUN_impl(self):
        return self.path_dto_instance.get_MEDSLIK_RUN()
    
    def get_MEDSLIK_MODEL_SRC_impl(self):
        return self.path_dto_instance.get_MEDSLIK_MODEL_SRC()
    
    def get_CONFIG1_impl(self):
        return self.path_dto_instance.get_CONFIG1()
    
    def get_CONFIG2_impl(self):
        return self.path_dto_instance.get_CONFIG2()
    
    def get_CASES_impl(self):
        return self.path_dto_instance.get_CASES()
    
    def get_OBS_impl(self):
        return self.path_dto_instance.get_OBS()
    
    def get_DAYS_GROUP_impl(self):
        return self.path_dto_instance.get_DAYS_GROUP()
    
    def get_OUT_FOLDER_impl(self):
        return self.path_dto_instance.get_OUT_FOLDER()
    
    def get_MEDSLIK_OUT_DIR_impl(self):        
        return self.path_dto_instance.get_MEDSLIK_OUT_DIR()
    
    def get_GSHHS_DATA_impl(self):
        return self.path_dto_instance.get_GSHHS_DATA()
    
    def copy_detection_directories_with_content_impl(self, source_path, destination_path, prefix):
        # Ensure that the destination directory exists
        os.makedirs(destination_path, exist_ok=True)

        # Iterate through all directories in the source directory
        for root, dirs, files in os.walk(source_path):
            # Filter directories to include only those starting with the desired prefix
            dirs[:] = [d for d in dirs if d.startswith(prefix)]

            for directory_name in dirs:
                # Construct the full path of the source directory
                source_directory_path = os.path.join(root, directory_name)
                
                # Remove the source path from the destination path to get a relative path
                relative_path = os.path.relpath(source_directory_path, source_path)
                destination_directory_path = os.path.join(destination_path, relative_path)

                # Copy the source directory with all its content to the destination
                shutil.copytree(source_directory_path, destination_directory_path, dirs_exist_ok=True)
    
    def remove_old_detection_directories_impl(self, source_path, prefix):
        # Iterate through all directories in the source directory
        for root, dirs, files in os.walk(source_path):
            # Filter directories to include only those starting with the desired prefix
            dirs[:] = [d for d in dirs if d.startswith(prefix)]

            for directory_name in dirs:
                directory_path = os.path.join(root, directory_name)
                # Remove the directory along with its contents
                shutil.rmtree(directory_path)