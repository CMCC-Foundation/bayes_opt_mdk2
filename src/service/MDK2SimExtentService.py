# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.MDK2SimExtentServiceImpl import MDK2SimExtentServiceImpl

class MDK2SimExtentService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.mdk2_sim_extent_service_impl_instance = MDK2SimExtentServiceImpl()
        
    """
    Recalls the implementation method to obtain the attributes present in the class by handling the exceptions
    """
    
    def get_sim_extent_params_dict(self):
        try:
            sim_extent = self.mdk2_sim_extent_service_impl_instance.get_sim_extent_params_dict_impl()
            return sim_extent
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_SIM_NAME(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_SIM_NAME_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_sim_lenght(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_sim_lenght_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
            
    def get_duration(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_duration_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_spill_rate(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_spill_rate_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_age(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_age_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_grid_size(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_grid_size_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
    
    def get_oil_api(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_oil_api_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_oil_volume(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_oil_volume_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_number_slick(self):
        try:
            return self.mdk2_sim_extent_service_impl_instance.get_number_slick_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None                        