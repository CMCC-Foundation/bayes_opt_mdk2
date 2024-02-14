# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.dto.MDK2SimParamsDTO import MDK2SimParamsDTO

class MDK2SimParamsServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
                
        self.mdk2_sim_params_dto_instance = MDK2SimParamsDTO()

    """
    Get useful parameters using the appropriate instances
    """
    
    def get_config_keys_impl(self):
        return self.mdk2_sim_params_dto_instance.get_k()
    
    def get_particles_value_impl(self):
        return self.mdk2_sim_params_dto_instance.get_vparticles()
    
    def get_sim_params_keys_values_dict_impl(self):
        return dict(zip(self.mdk2_sim_params_dto_instance.get_k(), self.mdk2_sim_params_dto_instance.get_v()))
        
    def get_particles_key_value_dict_impl(self):
        return {str(self.mdk2_sim_params_dto_instance.get_kparticles()): int(self.mdk2_sim_params_dto_instance.get_vparticles())}
    
    def get_sim_params_kv_dict_impl(self):
        return dict(zip(self.mdk2_sim_params_dto_instance.get_k(), self.mdk2_sim_params_dto_instance.get_v()))