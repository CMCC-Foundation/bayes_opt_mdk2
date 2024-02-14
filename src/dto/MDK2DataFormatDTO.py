# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.domain.MDK2DataFormat import MDK2DataFormat
from src.service.ConfigService import ConfigService

class MDK2DataFormatDTO:
    
    def __init__(self):
        """ Initialize the MDK2DataFormat instance using the values obtained from the configuration file """
        
        self.config_service = ConfigService()
        
        self.mdk2_data_format_instance = MDK2DataFormat(
            data_type = self.config_service.get_config_value('medslik2.data_format.type'),
            time_resolution = self.config_service.get_config_value('medslik2.data_format.time_res'),
            process_files = self.config_service.get_config_value('medslik2.data_format.process_files'),
            config_service = self.config_service
        )
        
    """
    Getter and setter methods for returning or setting parameter values by calling terms defined in the model class 
    while handling exceptions
    """
        
    def get_data_type(self):
        try:
            return self.mdk2_data_format_instance.get_data_type
        except (TypeError, KeyError):
            return None
        
    def get_time_resolution(self):
        try:
            return self.mdk2_data_format_instance.get_time_resolution
        except (TypeError, KeyError):
            return None
        
    def get_process_files(self):
        try:
            return self.mdk2_data_format_instance.get_process_files
        except (TypeError, KeyError):
            return None