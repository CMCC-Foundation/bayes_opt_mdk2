# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.MDK2SimCoordsServiceImpl import MDK2SimCoordsServiceImpl

class MDK2SimCoordsService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.mdk2_sim_coords_service_impl_instance = MDK2SimCoordsServiceImpl()
    
    """
    Recalls the method to obtain the simulation coordinate parameters from the specific implementation
    by handling its exceptions
    """
           
    def get_sim_coords_params_dict(self):
        try:
            sim_coords = self.mdk2_sim_coords_service_impl_instance.get_sim_coords_params_dict_impl()
            return sim_coords
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_lat_degree(self):
        try:
            return self.mdk2_sim_coords_service_impl_instance.get_lat_degree_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_lat_minutes(self):
        try:
            return self.mdk2_sim_coords_service_impl_instance.get_lat_minutes_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_lon_degree(self):
        try:
            return self.mdk2_sim_coords_service_impl_instance.get_lon_degree_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_lon_minutes(self):
        try:
            return self.mdk2_sim_coords_service_impl_instance.get_lon_minutes_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_delta(self):
        try:
            return self.mdk2_sim_coords_service_impl_instance.get_delta_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None