from __future__ import print_function
import os
import json
from .observer import _Tracker
from .event import Events
from .util import Colours

"""
import sys
sys.path.append("/work/asc/machine_learning/projects/iMagine/bayes_opt/src")

from controller.PathController import PathController

path_controller_instance = PathController()
"""

#result_dir = Path.OUT_FOLDER
#result_file = Path.RESULT_FILE_BO
#global_result = Path.WORKFLOW_FOLDER + Path.FINAL_FSS_RESULT_FILE

def _get_default_logger(verbose, is_constrained):
    return ScreenLogger(verbose=verbose, is_constrained=is_constrained)


class ScreenLogger(_Tracker):
    _default_cell_size = 20
    _default_precision = 4
    _default_text_lenght = 20

    def __init__(self, verbose=2, is_constrained=False):
        self._verbose = verbose
        self._is_constrained = is_constrained
        self._header_length = None
        super(ScreenLogger, self).__init__()

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, v):
        self._verbose = v

    @property
    def is_constrained(self):
        return self._is_constrained

    def _format_number(self, x):
        if isinstance(x, int):
                s = "{x:<{s}}".format(
                    x=x,
                    s=self._default_cell_size,
                )
        else:
            s = "{x:<{s}.{p}}".format(
                x=x,
                s=self._default_cell_size,
                p=self._default_precision,
            )

        if len(s) > self._default_cell_size:
            if "." in s:
                return s[:self._default_cell_size]
            else:
                return s[:self._default_cell_size - 3] + "..."
        return s

    def _format_text(self, x):
        if isinstance(x, int):
                s = "{x:<{s}}".format(
                    x=x,
                    s=self._default_cell_size,
                )
        else:
            s = "{x:<{s}.{p}}".format(
                x=x,
                s=self._default_cell_size,
                p=self._default_text_lenght,
            )

        if len(s) > self._default_cell_size:
            if "." in s:
                return s[:self._default_cell_size]
            else:
                return s[:self._default_cell_size - 3] + "..."
        return s

    def _format_bool(self, x):
        if 5 > self._default_cell_size:
            if x == True:
                x_ = 'T'
            elif x == False:
                x_ = 'F'
        else:
            x_ = str(x)
        s = "{x:<{s}}".format(
            x=x_,
            s=self._default_cell_size,
        )
        return s

    def _format_key(self, key):
        s = "{key:^{s}}".format(
            key=key,
            s=self._default_cell_size
        )
        if len(s) > self._default_cell_size:
            #return s[:self._default_cell_size - 3] + "..."
            return s[:self._default_cell_size]
        return s

    def _step(self, instance, colour=Colours.black):
        res = instance.res[-1]
        cells = []

        cells.append(self._format_number(self._iterations + 1))
        cells.append(self._format_number(res["target"]))
        if self._is_constrained:
            cells.append(self._format_bool(res["allowed"]))


        for key in instance.space.keys:
            cells.append(self._format_number(res["params"][key]))

        #line = "| " + " | ".join(cells) + " |"
        new_line = ",".join(cells)
            
        #with open(result_file, 'a') as f:
        #    f.write('\n')
        #    f.write(new_line)

        #with open(global_result, 'a') as f:
        #    f.write('\n')
        #    f.write(new_line)

        return "| " + " | ".join(map(colour, cells)) + " |"

    def _header(self, instance):
        cells = []
        #cells.append(self._format_key("iter"))
        #cells.append(self._format_key("target"))
        cells.append(self._format_text("iter"))
        cells.append(self._format_text("target"))

        if self._is_constrained:
            cells.append(self._format_key("allowed"))

        for key in instance.space.keys:
            cells.append(self._format_text(key))

        line = "| " + " | ".join(cells) + " |"
        new_line = ",".join(cells)
        self._header_length = len(line)

        # Potrei togliere controllo
        #print('out_folder : ' + Path.OUT_FOLDER)
        #if not os.path.isdir(Path.OUT_FOLDER):
        #    os.mkdir(Path.OUT_FOLDER)

        #with open(result_file, 'w') as f:
        #    f.write(new_line)

        #with open(global_result, 'w') as f:
        #    f.write(new_line)

        return line + "\n" + ("-" * self._header_length)

    def _is_new_max(self, instance):
        if instance.max is None:
            # During constrained optimization, there might not be a maximum
            # value since the optimizer might've not encountered any points
            # that fulfill the constraints.
            return False
        if self._previous_max is None:
            self._previous_max = instance.max["target"]
        return instance.max["target"] > self._previous_max

    def update(self, event, instance):
        if event == Events.OPTIMIZATION_START:
            line = self._header(instance) + "\n"
        elif event == Events.OPTIMIZATION_STEP:
            is_new_max = self._is_new_max(instance)
            if self._verbose == 1 and not is_new_max:
                line = ""
            else:
                colour = Colours.purple if is_new_max else Colours.black
                line = self._step(instance, colour=colour) + "\n"
            """
            if is_new_max:
                path_controller_instance.copy_detection_directories_with_content(path_controller_instance.get_sim_result_dir(), 
                                                                                 f"{os.path.join(path_controller_instance.get_sim_result_dir(), 'best_detections')}",
                                                                                 "detection_")
                path_controller_instance.remove_old_detection_directories(path_controller_instance.get_sim_result_dir(), "detection_")
            """    
            
        elif event == Events.OPTIMIZATION_END:
            line = "=" * self._header_length + "\n"

        if self._verbose:
            print(line, end="")
        self._update_tracker(event, instance)


class JSONLogger(_Tracker):
    def __init__(self, path, reset=True):


        self._path = path
        if reset:
            try:
                os.remove(self._path)
            except OSError:
                pass
        super(JSONLogger, self).__init__()

    def update(self, event, instance):
        if event == Events.OPTIMIZATION_STEP:
            data = dict(instance.res[-1])

            now, time_elapsed, time_delta = self._time_metrics()
            data["datetime"] = {
                "datetime": now,
                "elapsed": time_elapsed,
                "delta": time_delta,
            }

            if "allowed" in data: # fix: github.com/fmfn/BayesianOptimization/issues/361
                data["allowed"] = bool(data["allowed"])

            with open(self._path, "a") as f:
                f.write(json.dumps(data) + "\n")

        self._update_tracker(event, instance)
