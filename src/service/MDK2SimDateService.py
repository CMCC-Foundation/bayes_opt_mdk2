# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.MDK2SimDateServiceImpl import MDK2SimDateServiceImpl

class MDK2SimDateService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.mdk2_sim_date_service_impl_instance = MDK2SimDateServiceImpl()
        
    """
    Recalls the implementation method to obtain the attributes present in the class by handling the exceptions
    """
    
    def get_sim_date_params_dict(self):
        try:
            sim_date = self.mdk2_sim_date_service_impl_instance.get_sim_date_params_dict_impl()
            return sim_date
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_day(self):
        try:
            return self.mdk2_sim_date_service_impl_instance.get_day_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_month(self):
        try:
            return self.mdk2_sim_date_service_impl_instance.get_month_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_year(self):
        try:
            return self.mdk2_sim_date_service_impl_instance.get_year_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_hour(self):
        try:
            return self.mdk2_sim_date_service_impl_instance.get_hour_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
        
    def get_minutes(self):
        try:
            return self.mdk2_sim_date_service_impl_instance.get_miutes_impl()
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None        