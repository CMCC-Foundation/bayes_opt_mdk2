# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.dto.MDK2DataFormatDTO import MDK2DataFormatDTO
from src.dao.MDK2DataFormatRepo import MDK2DataFormatRepo

class MDK2DataFormatServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
        
        
        self.mdk2_data_format_dto_service = MDK2DataFormatDTO()
        self.mdk2_data_format_dao_service = MDK2DataFormatRepo()
        
    """
    Get useful parameters using the appropriate instances
    """
    
    def get_data_format_params_dict_impl(self):
        return self.mdk2_data_format_dao_service.get_all_params()
    
    def get_data_type_impl(self):
        return self.mdk2_data_format_dto_service.get_data_type()
    
    def get_time_resolution_impl(self):
        return self.mdk2_data_format_dto_service.get_time_resolution()
    
    def get_process_files_impl(self):
        return self.mdk2_data_format_dto_service.get_process_files()