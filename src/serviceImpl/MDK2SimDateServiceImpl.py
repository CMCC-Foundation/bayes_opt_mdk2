# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.dto.MDK2SimDateDTO import MDK2SimDateDTO
from src.dao.MDK2SimDateRepo import MDK2SimDateRepo

class MDK2SimDateServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
                
        self.mdk2_sim_date_dto_service = MDK2SimDateDTO()
        self.mdk2_sim_date_dao_service = MDK2SimDateRepo()
    
    """
    Get useful parameters using the appropriate instances
    """
    
    def get_sim_date_params_dict_impl(self):
        return self.mdk2_sim_date_dao_service.get_all_params()
    
    def get_day_impl(self):
        return self.mdk2_sim_date_dto_service.get_day()
    
    def get_month_impl(self):
        return self.mdk2_sim_date_dto_service.get_month()
    
    def get_year_impl(self):
        return self.mdk2_sim_date_dto_service.get_year()
    
    def get_hour_impl(self):
        return self.mdk2_sim_date_dto_service.get_hour()
    
    def get_miutes_impl(self):
        return self.mdk2_sim_date_dto_service.get_minutes()