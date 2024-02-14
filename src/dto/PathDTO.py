# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import os

from src.domain.Path import Path

class PathDTO:
    
    def __init__(self):
        """ Initialize the useful instances using the values obtained from the configuration file """

        self.ROOT = os.environ.get('PYTHONPATH').split(":")[1]
        # self.ROOT = '/work/asc/machine_learning/projects/iMagine/bayes_opt_20240214'
        self.MEDSLIK_FOLDER=os.path.join(self.ROOT, 'simulation/Medslik_II')
        # self.MEDSLIK_RUN = "/work/asc/machine_learning/projects/iMagine/MEDSLIK_II_2.02/RUN"
        self.MEDSLIK_RUN=os.path.join(self.MEDSLIK_FOLDER, 'MEDSLIK_II_3.01/RUN')
        self.WORKFLOW_CONFIG = os.path.join(self.ROOT, 'simulation_setup_file/workflow_config.toml')
        self.OUT_FOLDER = os.path.join(self.ROOT, 'MDKII_res/MDKII')
    
        self.path_instance = Path(
            ROOT = self.ROOT,
            MEDSLIK_FOLDER = self.MEDSLIK_FOLDER,
            WORKFLOW_CONFIG = self.WORKFLOW_CONFIG,
            CONFIG2_TEMPLATE = os.path.join(self.MEDSLIK_FOLDER, 'template/config2.txt'),
            MEDSLIK_RUN = self.MEDSLIK_RUN,
            MEDSLIK_MODEL_SRC = os.path.join(self.MEDSLIK_RUN, 'MODEL_SRC'),
            CONFIG1 = os.path.join(self.MEDSLIK_RUN, 'config1.txt'),
            CONFIG2 = os.path.join(self.MEDSLIK_RUN, 'config2.txt'),
            CASES = os.path.join(self.ROOT, 'use_cases'),
            OBS = os.path.join(self.ROOT, 'use_case_observations'),
            DAYS_GROUP = '/2021082*',
            OUT_FOLDER = self.OUT_FOLDER,
            # MEDSLIK_OUT_DIR = "/work/asc/machine_learning/projects/iMagine/MEDSLIK_II_2.02/OUT"
            MEDSLIK_OUT_DIR = os.path.join(self.MEDSLIK_FOLDER, 'MEDSLIK_II_3.01/OUT')
        )
        
    """
    Getter and setter methods for returning or setting parameter values by calling terms defined in the model class 
    while handling exceptions
    """
        
    def get_ROOT(self):
        try:
            return self.path_instance.get_ROOT
        except(TypeError, KeyError):
            return None
        
    def get_MEDSLIK_FOLDER(self):
        try:
            return self.path_instance.get_MEDSLIK_FOLDER
        except(TypeError, KeyError):
            return None
        
    def get_WORKFLOW_CONFIG(self):
        try:
            return self.path_instance.get_WORKFLOW_CONFIG
        except(TypeError, KeyError):
            return None
        
    def get_CONFIG2_TEMPLATE(self):
        try:
            return self.path_instance.get_CONFIG2_TEMPLATE
        except(TypeError, KeyError):
            return None
        
    def get_MEDSLIK_RUN(self):
        try:
            return self.path_instance.get_MEDSLIK_RUN
        except(TypeError, KeyError):
            return None
        
    def get_MEDSLIK_MODEL_SRC(self):
        try:
            return self.path_instance.get_MEDSLIK_MODEL_SRC
        except(TypeError, KeyError):
            return None
        
    def get_CONFIG1(self):
        try:
            return self.path_instance.get_CONFIG1
        except(TypeError, KeyError):
            return None
        
    def get_CONFIG2(self):
        try:
            return self.path_instance.get_CONFIG2
        except(TypeError, KeyError):
            return None
        
    def get_CASES(self):
        try:
            return self.path_instance.get_CASES
        except(TypeError, KeyError):
            return None
        
    def get_OBS(self):
        try:
            return self.path_instance.get_OBS
        except(TypeError, KeyError):
            return None
        
    def get_DAYS_GROUP(self):
        try:
            return self.path_instance.get_DAYS_GROUP
        except(TypeError, KeyError):
            return None
        
    def get_OUT_FOLDER(self):
        try:
            return self.path_instance.get_OUT_FOLDER
        except(TypeError, KeyError):
            return None
        
    def get_MEDSLIK_OUT_DIR(self):
        try:
            return self.path_instance.get_MEDSLIK_OUT_DIR
        except(TypeError, KeyError):
            return None        