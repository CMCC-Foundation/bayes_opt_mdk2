# ---------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Marco Mariano De Carlo, Gabriele Accarino
# ---------------------------------------------------------

import re
import subprocess
import pandas as pd
import os

from src.controller.PathController import PathController
from src.exception.UpdateConfigException import UpdateConfigException

class ExecutionServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
                
        self.path_controller_instance = PathController()
        self.update_config_exception_instance = UpdateConfigException()
    

    @staticmethod
    def update_config2_impl(config_dict, src, dst):
        """
        Update the configuration with the specified Bayesian Optimization values by handling exceptions

        Parameters:
            config_dict (dict): A dictionary containing key-value pairs for configuration updates.
            src (str): The source configuration file path serving as a template.
            dst (str): The destination configuration file path to store the updated configuration.
            dec_precision (int): The number of decimal places to round numeric values.

        Raises:
            UpdateConfigException: If an error occurs during the configuration update.
        """
        try:
            with open(dst, 'w') as config2:
                with open(src, 'r') as f:

                    for i,line in enumerate(f.readlines()):
                        splitted_line = line.split(' ')

                        if splitted_line[0].replace('.','',1).isdigit():
                            nspaces = re.findall(r'\s+', line)
                            cnt = 0 

                            for k,v in config_dict.items():
                                #print(k, v, type(v))
                                if (k in line) & (cnt == 0):
                                    #new_line = f"{v:.{dec_precision}f}{nspaces[0]}{k}\n"
                                    #new_line = f'{round(v, int(dec_precision))}{nspaces[0]}{k}\n'
                                    #new_line = f'{round(float(v), int(dec_precision))}{nspaces[0]}{k}\n'
                                    new_line = f'{v}{nspaces[0]}{k}\n'
                                    config2.write(str(new_line))
                                    cnt += 1
                                
                            if(cnt == 0):
                                config2.write(line)
                        else:
                            config2.write(line)
        except Exception as e:
            raise UpdateConfigException(f"Error during configuration update: {str(e)}")
    
    """
    Compile the MEDSLIK-II model using a specific script by handling exceptions
    """
    def compile_model(self):
        try:
            print('> Compile MEDSLIK-II (v3.01) ...')
            subprocess.run([f'cd {self.path_controller_instance.get_MEDSLIK_RUN()}; sh MODEL_SRC/compile.sh; cd {self.path_controller_instance.get_ROOT()}'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True, check=True)
            return "Compilation successfully completed"
        except subprocess.CalledProcessError as e:
            # TODO: si può togliere il print
            print(f"Error while compiling MEDSLIK-II: {e}")
            return f"Error while compiling MEDSLIK-II: {e}"
        except Exception as e:
            print(f"An error occurred while compiling MEDSLIK-II: {e}")
            return f"An error occurred while compiling MEDSLIK-II: {e}"
    
    """
    Runs the MEDSLIK-II model using a specific script by handling exceptions
    """
    def run_model(self):
        try:
            # subprocess.run([f'cd {self.path_controller_instance.get_MEDSLIK_RUN()}; sh RUN.sh'],shell=True,check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run([f'cd {self.path_controller_instance.get_MEDSLIK_RUN()}; sh RUN.sh'],shell=True,check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "Execution successfully completed"
        except subprocess.CalledProcessError as e:
            print(f"Error while running MEDSLIK-II: {e}")
            return f"Error while running MEDSLIK-II: {e}"
        except Exception as e:
            print(f"An error occurred during the execution of MEDSLIK-II: {e}")
            return f"An error occurred during the execution of MEDSLIK-II: {e}"
        
    def save_best_detection_impl(self, value):
        max_fss = pd.read_csv(self.path_controller_instance.get_simulation_result_file(
            self.path_controller_instance.get_sim_result_dir()), 
                              sep=',')['Metric'].max()
        
        if value > max_fss or pd.isna(max_fss):
            self.path_controller_instance.copy_detection_directories_with_content(
                self.path_controller_instance.get_sim_result_dir(), 
                f"{os.path.join(self.path_controller_instance.get_sim_result_dir(), 'best_detections')}",
                "detection_")