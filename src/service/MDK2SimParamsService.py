# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# --------------------------------------------------------

from src.serviceImpl.MDK2SimParamsServiceImpl import MDK2SimParamsServiceImpl

class MDK2SimParamsService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.mdk2_sim_params_service_impl_instance = MDK2SimParamsServiceImpl()
         
    """
    Recalls the implementation method to obtain the attributes present in the class by handling the exceptions
    """     
    
    def get_config_keys(self):
        try:
            k = self.mdk2_sim_params_service_impl_instance.get_config_keys_impl()
            return k
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None          
        
    def get_config_values(self):
        try:
            v = self.mdk2_sim_params_service_impl_instance.get_config_values_impl()
            return v
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None        

    def get_particles_value(self):
        try:
            vparticles = self.mdk2_sim_params_service_impl_instance.get_particles_value_impl()
            return vparticles
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None          
        
    def get_sim_params_keys_values_dict(self):
        try:
            sim_params = self.mdk2_sim_params_service_impl_instance.get_sim_params_keys_values_dict_impl()
            return sim_params
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_particles_key_value_dict(self):
        try:
            sim_params_key = self.mdk2_sim_params_service_impl_instance.get_particles_key_value_dict_impl()
            return sim_params_key
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_sim_params_kv_dict(self):
        try:
            sim_params_kv = self.mdk2_sim_params_service_impl_instance.get_sim_params_kv_dict_impl()
            return sim_params_kv
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
