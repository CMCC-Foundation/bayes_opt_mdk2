# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.dto.MDK2SimExtentDTO import MDK2SimExtentDTO
from src.dao.MDK2SimExtentRepo import MDK2SimExtentRepo

class MDK2SimExtentServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
                
        self.mdk2_sim_extent_dto_service = MDK2SimExtentDTO()
        self.mdk2_sim_extent_dao_service = MDK2SimExtentRepo()

    """
    Get useful parameters using the appropriate instances
    """
    
    def get_sim_extent_params_dict_impl(self):
        return self.mdk2_sim_extent_dao_service.get_all_params()
    
    def get_SIM_NAME_impl(self):
        return self.mdk2_sim_extent_dto_service.get_SIM_NAME()
    
    def get_sim_lenght_impl(self):
        return self.mdk2_sim_extent_dto_service.get_sim_length()
    
    def get_duration_impl(self):
        return self.mdk2_sim_extent_dto_service.get_duration()
    
    def get_spill_rate_impl(self):
        return self.mdk2_sim_extent_dto_service.get_spillrate()
    
    def get_age_impl(self):
        return self.mdk2_sim_extent_dto_service.get_age()
    
    def get_grid_size_impl(self):
        return self.mdk2_sim_extent_dto_service.get_grid_size()
    
    def get_oil_api_impl(self):
        return self.mdk2_sim_extent_dto_service.get_oil_api()
    
    def get_oil_volume_impl(self):
        return self.mdk2_sim_extent_dto_service.get_oil_volume()
    
    def get_number_slick_impl(self):
        return self.mdk2_sim_extent_dto_service.get_number_slick()
