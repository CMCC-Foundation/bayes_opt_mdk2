# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

from src.service.ConfigService import ConfigService

class BayOptSetup:
    
    def __init__(self, eval_metric: str, init_points: int, n_iter: int,
                 random_state: str, decimal_precision: int, verbose: int, 
                 config_service = ConfigService): 
        """ Initialize class with specified parameters """
        
        self._eval_metric = eval_metric
        self._init_points = init_points
        self._n_iter = n_iter
        self._random_state = random_state
        self._decimal_precision = decimal_precision
        self._verbose = verbose
        self._config_service = config_service
        
    """
    Getter and setter methods to return or set values related to the class
    """

    @property
    def get_eval_metric(self):
        return self._eval_metric

    @get_eval_metric.setter
    def set_eval_metric(self, value):
        self._eval_metric = value

    @property
    def get_init_points(self):
        return self._init_points

    @get_init_points.setter
    def set_init_points(self, value):
        self._init_points = value

    @property
    def get_n_iter(self):
        return self._n_iter

    @get_n_iter.setter
    def set_n_iter(self, value):
        self._n_iter = value

    @property
    def get_random_state(self):
        return self._random_state

    @get_random_state.setter
    def set_random_state(self, value):
        self._random_state = value

    @property
    def get_decimal_precision(self):
        return self._decimal_precision

    @get_decimal_precision.setter
    def set_decimal_precision(self, value):
        self._decimal_precision = value

    @property
    def get_verbose(self):
        return self._verbose

    @get_verbose.setter
    def set_verbose(self, value):
        self._verbose = value

    @property
    def get_config_service(self):
        return self._config_service

    @get_config_service.setter
    def set_config_service(self, value):
        self._config_service = value