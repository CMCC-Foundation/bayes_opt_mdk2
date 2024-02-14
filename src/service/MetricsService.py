# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.serviceImpl.MetricsServiceImpl import MetricsServiceImpl

class MetricsService:
    
    def __init__(self):
        """ Initialize the requested service instance """
        
        self.metrics_service_impl_instance = MetricsServiceImpl()
        
    def erre_sbl_2021_service(self, a, b, c, d):
            try:
                return self.metrics_service_impl_instance.esse_sbl_2021_service_impl(a, b, c, d)
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
        
    def fbias_sbl_2021_service(self, a, b, c, d):
        try:
            return self.metrics_service_impl_instance.fbias_sbl_2021_service_impl(a, b, c, d)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def barrelToTonnes_service(self, oil_density):
        try:
            return self.metrics_service_impl_instance.barrelToTonnes_service_impl(oil_density)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_surface_parcels_service(self, fname, time_index):
        try:
            return self.metrics_service_impl_instance.get_surface_parcels_service_impl(fname, time_index)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def make_poly_grid_service(self, xmin, xmax, ymin, ymax, cell_size, crs):
        try:
            return self.metrics_service_impl_instance.make_poly_grid_service_impl(xmin, xmax, ymin, ymax, cell_size, crs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_obs_date_service(self, observation_shp):
        try:
            return self.metrics_service_impl_instance.get_obs_date_service_impl(observation_shp)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_mdksim_date_service(self):
        try:
            return self.metrics_service_impl_instance.get_mdksim_date_service_impl()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def find_nearest_service(self, array, value):
        try:
            return self.metrics_service_impl_instance.find_nearest_service_impl(array, value)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def compute_sin_fss_service(self, simulation_folder, observation_shp, output_folder):
        try:
            return self.metrics_service_impl_instance.compute_sin_fss(simulation_folder, observation_shp, output_folder)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_sim_date_service(self, yy, mm, dd, hh):
        try:
            return self.metrics_service_impl_instance.get_sim_date_service_impl(yy, mm, dd, hh)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_slick_date_service(self, slick_id):
        try:
            return self.metrics_service_impl_instance.get_slick_date_service_impl(slick_id)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def compute_multi_fss_service(self):
        try:
            return self.metrics_service_impl_instance.compute_multi_fss_service_impl()
        except Exception as e:
            print(f"Compute Multi FSS, An error occurred: {e}")
            return None