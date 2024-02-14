# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.service.ConfigService import ConfigService

class Workflow:
    
    def __init__(self, eval_metric: str, sim_extent:dict, sim_date:dict,
                 sim_coords:dict, sim_params:dict, sim_data_format:dict,
                 sim_particles:dict, init_points:int, n_iter:int, 
                 parameters_bound:dict, random_state: int, decimal_precision: int,
                 verbose:int, config_service: ConfigService):
        """ Initialize class with specified parameters """
        
        self.eval_metric = eval_metric
        self.sim_extent = sim_extent
        self.sim_date = sim_date
        self.sim_coords = sim_coords
        self.sim_params = sim_params
        self.sim_data_format = sim_data_format
        self.sim_particles = sim_particles
        self.init_points = init_points
        self.n_iter = n_iter
        self.parameters_bound = parameters_bound
        self.random_state = random_state 
        self.decimal_precision = decimal_precision
        self.verbose = verbose
        self.config_service = config_service
        
    """
    Getter and setter methods to return or set values related to the class
    """

    @property
    def get_eval_metric(self):
        return self.eval_metric
    
    @eval_metric.setter
    def set_eval_metric(self, value):
        self.eval_metric = value

    @property
    def get_sim_extent(self):
        return self.sim_extent
    
    @sim_extent.setter
    def set_sim_extent(self, value):
        self.sim_extent = value
        
    @property
    def get_sim_date(self):
        return self.sim_date
    
    @sim_date.setter
    def set_sim_date(self, value):
        self.sim_date = value
        
    @property
    def get_sim_coords(self):
        return self.sim_coords
    
    @sim_coords.setter
    def set_sim_coords(self, value):
        self.sim_coords = value
        
    @property
    def get_sim_params(self):
        return self.sim_params
    
    @sim_params.setter
    def set_sim_params(self, value):
        self.sim_params = value
    
    @property
    def get_sim_data_format(self):
        return self.sim_data_format
    
    @sim_data_format.setter
    def set_sim_data_format(self, value):
        self.sim_data_format = value
        
    @property
    def get_sim_particles(self):
        return self.sim_particles
    
    @sim_particles.setter
    def set_sim_particles(self, value):
        self.sim_particles = value
        
    @property
    def get_init_points(self):
        return self.init_points
    
    @init_points.setter
    def set_init_points(self, value):
        self.init_points = value
        
    @property
    def get_n_iter(self):
        return self.n_iter
    
    @n_iter.setter
    def set_n_iter(self, value):
        self.n_iter = value
        
    @property
    def get_parameters_bound(self):
        return self.parameters_bound
    
    @parameters_bound.setter
    def set_parameters_bound(self, value):
        self.parameters_bound = value
        
    @property
    def get_random_state(self):
        return self.random_state
    
    @random_state.setter
    def set_random_state(self, value):
        self.random_state = value
    
    @property
    def get_decimal_precision(self):
        return self.decimal_precision
    
    @decimal_precision.setter
    def set_decimal_precision(self, value):
        self.decimal_precision = value
    
    @property
    def get_verbose(self):
        return self.verbose
    
    @verbose.setter
    def set_verbose(self, value):
        self.verbose = value