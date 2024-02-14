# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.service.ConfigService import ConfigService

class MDK2SimDate:

    def __init__(self, day: str, month: str, year: str, 
                 hour: str, minutes: str, config_service: ConfigService):
        """ Initialize class with specified parameters """
        
        self._day = day
        self._month = month
        self._year = year
        self._hour = hour
        self._minutes = minutes
        self._config_service = config_service
        
    """
    Getter and setter methods to return or set values related to the class
    """

    @property
    def get_day(self):
        return self._day
    
    @get_day.setter
    def set_day(self, value):
        self._day = value

    @property
    def get_month(self):
        return self._month
    
    @get_month.setter
    def set_month(self, value):
        self._month = value

    @property
    def get_year(self):
        return self._year
    
    @get_year.setter
    def set_year(self, value):
        self._year = value

    @property
    def get_hour(self):
        return self._hour
    
    @get_hour.setter
    def set_hour(self, value):
        self._hour = value

    @property
    def get_minutes(self):
        return self._minutes
    
    @get_minutes.setter
    def set_minutes(self, value):
        self._minutes = value
        
    @property
    def get_config_service(self):
        return self._config_service
    
    @get_config_service.setter
    def set_config_service(self, value):
        self._config_service = value
