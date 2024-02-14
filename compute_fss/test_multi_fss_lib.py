from datetime import  *
import os
import shutil
import sys

sys.path.append("/work/asc/machine_learning/projects/iMagine/bayes_opt")
from src.controller.PathController import PathController

path_controller_instance = PathController()

def get_sim_date(yy, mm, dd, hh):
    return date(2000+int(yy),int(mm),int(dd)).toordinal()+ float(hh)/24.

def get_slick_date(slick_id):
    return date(int(slick_id[0:4]),int(slick_id[4:6]),int(slick_id[6:8])).toordinal() + float(slick_id[9:11])/24.

def set_out_folder(parent, obs):

    out_folder = path_controller_instance.get_detection_dir() # Path.OUT_FOLDER
    detection_folder = path_controller_instance.get_OBS() + str(obs) # Path.DETECTION_FOLDER + str(obs)

# per RS
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
        print(out_folder)

    if os.path.exists(detection_folder):
        shutil.rmtree(detection_folder)
        os.mkdir(detection_folder)
    else:
        os.mkdir(detection_folder)
        print(detection_folder)
        
    return out_folder, detection_folder