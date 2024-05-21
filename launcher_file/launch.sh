#!/bin/bash
#BSUB -n 1
#BSUB -q s_long
#BSUB -P R000
#BSUB -J iMagine
#BSUB -o ./job.out
#BSUB -e ./job.err
#BSUB -R "rusage[mem=1G]"

ROOT="/work/cmcc/machine_learning/md31923/iMagine/bayes_opt_mdk2"
SIM="/work/cmcc/machine_learning/md31923/iMagine/simulation/Medslik_II"
OBS="/work/cmcc/machine_learning/md31923/iMagine/bayes_opt_mdk2/use_case_observations/syria/observations_2021_08_23_1000/20210824-1533-SYR-PL-B-01-S1"

# !conda run -p /work/asc/machine_learning/projects/iMagine/bayes_opt_workflow/env/mdk2_env \
export PYTHONPATH=$PYTHONPATH:$ROOT && \
export SIMPATH=$SIMPATH:$SIM && \
export OBSPATH=$OBSPATH:$OBS && \

python $ROOT/src/main/main.py \
--mode 0
