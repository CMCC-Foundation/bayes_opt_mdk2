# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import sys
import argparse
import warnings
warnings.filterwarnings('ignore')

from src.service.BayOptBoundsService import BayOptBoundsService
from src.service.BayOptSetupService import BayOptSetupService
from src.service.MDK2SimParamsService import MDK2SimParamsService

from src.controller.WorkflowController import WorkflowController

"""
Checks whether simulation parameters and Bayesian optimization parameters match,
if they do not match, raises an exception
"""
def check_parameters_match(sim_params, parameters_bound):
    if sorted(sim_params) != sorted(parameters_bound):
        raise ValueError('A mismatch between Medslik-II and the Bayesian Optimization configuration parameters was encountered in the config file.')

"""
Checks whether the number of particles is within the limits,
if it is not greater, raises an exception
"""
def check_particles_number(nparticles):
    if nparticles <= 571:
        raise ValueError('Increase the number of simulated particles')

def main(args):
    """ Initializes several instances of services and controllers """
    bay_opt_bounds_service_instance = BayOptBoundsService()
    bay_opt_setup_service_instance = BayOptSetupService()
    mdk2_sim_params_service_instance = MDK2SimParamsService()

    workflow_controller_instance = WorkflowController()

    """ Get the parameters needed to execute the workflow """
    sim_params = mdk2_sim_params_service_instance.get_sim_params_keys_values_dict()
    nparticles = mdk2_sim_params_service_instance.get_particles_value()
    parameters_bound = bay_opt_bounds_service_instance.get_parameter_bounds_dict()
    random_state = None if bay_opt_setup_service_instance.get_random_state() == 'None' else int(bay_opt_setup_service_instance.get_random_state())
    verbose = bay_opt_setup_service_instance.get_verbose()
    
    try:
        """
        Perform parameter and particle number checks
        """
        check_parameters_match(sim_params.keys(), parameters_bound.keys())
            
        check_particles_number(nparticles)
        
        """
        Check the type of execution via the workflow controller
        """
        print("> Check Mode")
        workflow_controller_instance.check_execution_type(args.mode)

        """
        Perform configuration and workflow execution
        """
        workflow_controller_instance.setup(args.mode)
        workflow_controller_instance.run(args.mode, parameters_bound, random_state, verbose)
    
    # TODO: da sostituire con eccezione personalizzata
    except Exception as e:
        print(f"Error during execution (Check main.py): {e}")
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        prog=r'''
                        ███╗   ███╗███████╗██████╗ ███████╗██╗     ██╗██╗  ██╗        ██╗██╗
                        ████╗ ████║██╔════╝██╔══██╗██╔════╝██║     ██║██║ ██╔╝        ██║██║
                        ██╔████╔██║█████╗  ██║  ██║███████╗██║     ██║█████╔╝         ██║██║
                        ██║╚██╔╝██║██╔══╝  ██║  ██║╚════██║██║     ██║██╔═██╗         ██║██║
                        ██║ ╚═╝ ██║███████╗██████╔╝███████║███████╗██║██║  ██╗███████╗██║██║
                        ╚═╝     ╚═╝╚══════╝╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝
        ''',
        description='BAY OPT MEDSLIKII',
        epilog="Thanks for using BAY_OPT_MDKII! :)",
    )

    parser.add_argument('--mode', '-m', type=int, help='For MEDSLIK II with BO: Bay_Opt or for a MDKII single run: Single_Run')
    #parser.add_argument('--config', '-c', help='Path to config file (*.toml format)')
    parser.add_argument('--version', '-v', action='version', version='v1.0-dev')
    args = parser.parse_args()

    print('\n\n\n')
    print(parser.prog)
    print('\n\n\n')
    
    main(args)