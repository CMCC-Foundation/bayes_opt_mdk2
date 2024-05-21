# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.PathServiceImpl import PathServiceImpl

class PathService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.path_service_impl_instance = PathServiceImpl()
        
    """
    Recalls the implementation method to obtain the attributes present in the class by handling the exceptions
    """
    
    def get_ROOT_path(self):
        try:
            root = self.path_service_impl_instance.get_ROOT_impl()
            return root
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_MEDSLIK_FOLDER_path(self):
        try:
            med_folder = self.path_service_impl_instance.get_MEDSLIK_FOLDER_impl()
            return med_folder
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_WORKFLOW_CONFIG_path(self):
        try:
            workflow_config = self.path_service_impl_instance.get_WORKFLOW_CONFIG_impl()
            return workflow_config
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_CONFIG2_TEMPLATE_path(self):
        try:
            config2_template = self.path_service_impl_instance.get_CONFIG2_TEMPLATE_impl()
            return config2_template
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_MEDSLIK_RUN_path(self):
        try:
            med_run = self.path_service_impl_instance.get_MEDSLIK_RUN_impl()
            return med_run
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_MEDSLIK_MODEL_SRC_path(self):
        try:
            med_model_src = self.path_service_impl_instance.get_MEDSLIK_MODEL_SRC_impl()
            return med_model_src
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_CONFIG1_path(self):
        try:
            config1 = self.path_service_impl_instance.get_CONFIG1_impl()
            return config1
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
    
    def get_CONFIG2_path(self):
        try:
            config2 = self.path_service_impl_instance.get_CONFIG2_impl()
            return config2
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_CASES_path(self):
        try:
            cases = self.path_service_impl_instance.get_CASES_impl()
            return cases
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_OBS_path(self):
        try:
            obs = self.path_service_impl_instance.get_OBS_impl()
            return obs
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None

    def get_DAYS_GROUP_path(self):
        try:
            obs = self.path_service_impl_instance.get_DAYS_GROUP_impl()
            return obs
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None

    def get_OUT_FOLDER_path(self):
        try:
            obs = self.path_service_impl_instance.get_OUT_FOLDER_impl()
            return obs
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None       
        
    def get_MEDSLIK_OUT_DIR_path(self):
        try:
            obs = self.path_service_impl_instance.get_MEDSLIK_OUT_DIR_impl()
            return obs
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None       
        
    def get_GSHHS_DATA_path(self):
        try:
            data = self.path_service_impl_instance.get_GSHHS_DATA_impl()
            return data
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def copy_detection_directories_with_content_service(self, source_path, destination_path, prefix):
        try:
            return self.path_service_impl_instance.copy_detection_directories_with_content_impl(source_path, destination_path, prefix)
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None           
        
    def remove_old_detection_directories_service(self, source_path, prefix):
        try:
            return self.path_service_impl_instance.remove_old_detection_directories_impl(source_path, prefix)
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None   