# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

class Path:
    
    def __init__(self, ROOT:str, MEDSLIK_FOLDER:str, WORKFLOW_CONFIG:str, CONFIG2_TEMPLATE:str, 
                 MEDSLIK_RUN:str, MEDSLIK_MODEL_SRC:str, CONFIG1:str, CONFIG2:str, CASES:str, 
                 OBS:str, DAYS_GROUP:str, OUT_FOLDER:str, MEDSLIK_OUT_DIR:str):
        """ Initialize class with specified parameters """
        
        self._ROOT = ROOT
        self._MEDSLIK_FOLDER = MEDSLIK_FOLDER
        self._WORKFLOW_CONFIG = WORKFLOW_CONFIG
        #CONFIG1_TEMPLATE = os.path.join(ROOT, 'data/template/config1.txt')
        self._CONFIG2_TEMPLATE = CONFIG2_TEMPLATE
        self._MEDSLIK_RUN = MEDSLIK_RUN
        #GEN_SIM_DATA = os.path.join(MEDSLIK_FOLDER, 'gen_mdk2_sim.py')
        self._MEDSLIK_MODEL_SRC = MEDSLIK_MODEL_SRC
        self._CONFIG1 = CONFIG1
        self._CONFIG2 = CONFIG2
        self._CASES = CASES
        self._OBS = OBS
        self._DAYS_GROUP = DAYS_GROUP
        self._OUT_FOLDER = OUT_FOLDER
        self._MEDSLIK_OUT_DIR = MEDSLIK_OUT_DIR
        
    """ Getter and setter methods to return or set values related to the class """
    
    @property
    def get_ROOT(self):
        return self._ROOT

    @get_ROOT.setter
    def set_ROOT(self, value):
        self._ROOT = value

    @property
    def get_MEDSLIK_FOLDER(self):
        return self._MEDSLIK_FOLDER

    @get_MEDSLIK_FOLDER.setter
    def set_MEDSLIK_FOLDER(self, value):
        self._MEDSLIK_FOLDER = value

    @property
    def get_WORKFLOW_CONFIG(self):
        return self._WORKFLOW_CONFIG

    @get_WORKFLOW_CONFIG.setter
    def set_WORKFLOW_CONFIG(self, value):
        self._WORKFLOW_CONFIG = value
        
    @property
    def get_CONFIG2_TEMPLATE(self):
        return self._CONFIG2_TEMPLATE
    
    @get_CONFIG2_TEMPLATE.setter
    def set_CONFIG2_TEMPLATE(self, value):
        self._CONFIG2_TEMPLATE = value

    @property
    def get_MEDSLIK_RUN(self):
        return self._MEDSLIK_RUN

    @get_MEDSLIK_RUN.setter
    def set_MEDSLIK_RUN(self, value):
        self._MEDSLIK_RUN = value

    @property
    def get_MEDSLIK_MODEL_SRC(self):
        return self._MEDSLIK_MODEL_SRC

    @get_MEDSLIK_MODEL_SRC.setter
    def set_MEDSLIK_MODEL_SRC(self, value):
        self._MEDSLIK_MODEL_SRC = value

    @property
    def get_CONFIG1(self):
        return self._CONFIG1

    @get_CONFIG1.setter
    def set_CONFIG1(self, value):
        self._CONFIG1 = value

    @property
    def get_CONFIG2(self):
        return self._CONFIG2

    @get_CONFIG2.setter
    def set_CONFIG2(self, value):
        self._CONFIG2 = value

    @property
    def get_CASES(self):
        return self._CASES

    @get_CASES.setter
    def set_CASES(self, value):
        self._CASES = value

    @property
    def get_OBS(self):
        return self._OBS

    @get_OBS.setter
    def set_OBS(self, value):
        self._OBS = value
        
    @property
    def get_DAYS_GROUP(self):
        return self._DAYS_GROUP
    
    @get_DAYS_GROUP.setter
    def set_DAYS_GROUP(self, value):
        self._DAYS_GROUP = value
        
    @property
    def get_OUT_FOLDER(self):
        return self._OUT_FOLDER
    
    @get_OUT_FOLDER.setter
    def set_OUT_FOLDER(self, value):
        self._OUT_FOLDER = value
        
    @property
    def get_MEDSLIK_OUT_DIR(self):
        return self._MEDSLIK_OUT_DIR
    
    @get_MEDSLIK_OUT_DIR.setter
    def set_MEDSLIK_OUT_DIR(self, value):
        self._MEDSLIK_OUT_DIR = value