# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

class RunException(Exception):
    """ Custom exception to handle errors during MEDSLIK II model run """
    
    def __init__(self, message=f"Error during MEDSLIK-II run: {ValueError}"):
        self.message = message
        super().__init__(self.message)