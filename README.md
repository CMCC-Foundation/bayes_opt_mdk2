# Bayesian Optimization Workflow for Medslik-II (bayes_opt_mdk2)

Bayesian Optimization Workflow for the Medslik-II Mathematical Model, used for simulations of Oil Spill Events.

## Description

This tool allows you to initiate a workflow based on Bayesian Optimization to perform Oil Spill Event simulations using the Medslik-II model. The goal is to optimize the model's initial parameters in an informed, physically consistent manner without requiring specific domain knowledge.

## Features

The optimization process improves the Oil Spill simulation results by maximizing a metric of choice between:

- **Fraction Skill Score (FSS)**
- **Overlay**

To use the tool, you need to configure the model by modifying the `/simulation_setup_file/workflow_config.toml` file according to the chosen event. If you wish to compare the simulation result with a past event, you need to provide the path of the observation to be compared, along with the paths for the workflow and the output folder.

## Configuration

In the `/simulation_setup_file/workflow_config.toml` file, besides specifying the characteristics of the simulation, it is important to define the number of "probe" and "exploration" iterations you wish to perform.

### Example configuration for `simulation_setup_file/workflow_config.toml`

```toml
[bayesian_optimization]
b = [[0.0, 0.05], [0.0, 15.0], [0.0, 20.0]]

[bayesian_optimization.setup]
eval_metric = "FSS" # or "overlay"
init_points = 3
n_iter = 7
random_state = "None"
decimal_precision = 2
verbose = 2

[medslik2.sim_extent]
SIM_NAME = "syria"
sim_length = "0008"
duration = "0000"
spillrate = "00027.78"
age = "0"
grid_size = "150.0"
oil_api = 28.0
oil_volume = 2000.0
number_slick = 151

[medslik2.sim_date]
day = "24"
month = "08"
year = "21"
hour = "08"
minutes = "10"

[medslik2.sim_coords]
lat_degree = 35
lat_minutes = 15.6
lon_degree = 35
lon_minutes = 54.6
delta = 1

[medslik2.sim_params]
k = ["Wind correction (Drift Factor)", "Horizontal Diffusivity"]
v = [0.01, 10.26]
kparticles = "No of parcels used to model diffusion and dispersion"
vparticles = 90000

[medslik2.data_format]
type = "analysis"
time_res = "day"
process_files = "True"
```

## Execution Modes
The tool supports two different execution modes:

1. **Optimization with Bayes Opt (Mode 0)**
   - This mode uses Bayesian optimization to optimize the model's initial parameters.

2. **Simulation without Bayes Opt (Mode 1)**
   - This mode performs a simulation using the provided initial parameters without applying Bayesian optimization.

## Example of Execution
To run the tool, use the following bash script:

```
ROOT="/work/cmcc/machine_learning/md31923/iMagine/bayes_opt_mdk2"
SIM="/work/cmcc/machine_learning/md31923/iMagine/simulation/Medslik_II"
OBS="/work/cmcc/machine_learning/md31923/iMagine/bayes_opt_mdk2/use_case_observations/syria/observations_2021_08_23_1000/20210824-1533-SYR-PL-B-01-S1"

export PYTHONPATH=$PYTHONPATH:$ROOT && \
export SIMPATH=$SIMPATH:$SIM && \
export OBSPATH=$OBSPATH:$OBS && \

python $ROOT/src/main/main.py \
--mode <mode>
```

Replace `<mode>` with `0` for Bayesian optimization or `1` for simple simulation.

# Istruzioni per l'Uso
1. **Configure the Model**: Modify the `config.toml` file with the parameters of the event to be simulated.
2. **Provide Necessary Paths**: If you want to compare with a past event, make sure to provide the path to the observation.
3. **Start the Optimization or Simulation Process**: Run the appropriate command to start the desired workflow.
