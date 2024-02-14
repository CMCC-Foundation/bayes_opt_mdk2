# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

class WrongConfigurationException(Exception):
    """ Custom exception to handle generic errors in configuration choice """
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)