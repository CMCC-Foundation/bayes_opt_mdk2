#!/bin/bash
#BSUB -n 1
#BSUB -q s_short
#BSUB -P R000
#BSUB -J iMagine
#BSUB -o ./job.out
#BSUB -e ./job.err
#BSUB -R "rusage[mem=3G]"

ROOT="/work/cmcc/machine_learning/md31923/iMagine/bayes_opt_20240213_test"
SIM="/work/cmcc/machine_learning/md31923/iMagine/simulation/Medslik_II"
# SIM="/work/cmcc/machine_learning/md31923/iMagine"
OBS="/work/cmcc/machine_learning/md31923/iMagine/bayes_opt_20240213_test/use_case_observations/syria/observations_2021_08_23_1000/20210824-0810-SYR-PL-A-01-S3"
# OBS="/work/cmcc/machine_learning/md31923/iMagine/bayes_opt_20240213_test/use_case_observations/cyprus/20220831-0343-CYP-UO-B-01-S1"
# OBS="/work/cmcc/machine_learning/md31923/iMagine/bayes_opt_20240213_test/use_case_observations/palestine/20220413-1549-ISR-UO-B-01-S1"

# !conda run -p /work/asc/machine_learning/projects/iMagine/bayes_opt_workflow/env/mdk2_env \
export PYTHONPATH=$PYTHONPATH:$ROOT && \
export SIMPATH=$SIMPATH:$SIM && \
export OBSPATH=$OBSPATH:$OBS && \

python $ROOT/src/main/main.py \
--mode 0