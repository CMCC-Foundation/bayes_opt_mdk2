# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.MDK2DataFormatServiceImpl import MDK2DataFormatServiceImpl

class MDK2DataFormatService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.mdk2_data_format_service_impl_instance = MDK2DataFormatServiceImpl()
    
    """
    Recalls the method to obtain the simulation coordinate parameters from the specific implementation
    by handling its exceptions
    """   
    def get_data_format_params_dict(self):
        try:
            sim_coords = self.mdk2_data_format_service_impl_instance.get_data_format_params_dict_impl()
            return sim_coords
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    """
    Recalls the implementation method to obtain the attributes present in the class by handling the exceptions
    """
        
    def get_data_type(self):
        try:
            return self.mdk2_data_format_service_impl_instance.get_data_type_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None      
        
    def get_time_resolution(self):
        try:
            return self.mdk2_data_format_service_impl_instance.get_time_resolution_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None      
        
    def get_process_files(self):
        try:
            return self.mdk2_data_format_service_impl_instance.get_process_files_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None   