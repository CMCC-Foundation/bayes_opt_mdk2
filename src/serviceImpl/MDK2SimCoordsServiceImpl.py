# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.dto.MDK2SimCoordsDTO import MDK2SimCoordsDTO
from src.dao.MDK2SimCoordsRepo import MDK2SimCoordsRepo

class MDK2SimCoordsServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
                
        self.mdk2_sim_coords_dto_service = MDK2SimCoordsDTO()
        self.mdk2_sim_coords_dao_service = MDK2SimCoordsRepo()
        
    """
    Get useful parameters using the appropriate instances
    """
    
    def get_sim_coords_params_dict_impl(self):
        return self.mdk2_sim_coords_dao_service.get_all_params()
    
    def get_lat_degree_impl(self):
        return self.mdk2_sim_coords_dto_service.get_lat_degree()
    
    def get_lat_minutes_impl(self):
        return self.mdk2_sim_coords_dto_service.get_lat_minutes()
    
    def get_lon_degree_impl(self):
        return self.mdk2_sim_coords_dto_service.get_lon_degree()
    
    def get_lon_minutes_impl(self):
        return self.mdk2_sim_coords_dto_service.get_lon_minutes()
    
    def get_delta_impl(self):
        return self.mdk2_sim_coords_dto_service.get_delta()   