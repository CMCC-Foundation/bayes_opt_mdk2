#!/bin/bash
#BSUB -n 1
#BSUB -q s_short
#BSUB -P R000
#BSUB -J iMagine
#BSUB -o ./job.out
#BSUB -e ./job.err
#BSUB -R "rusage[mem=1G]"

ROOT="/work/asc/machine_learning/projects/iMagine/bayes_opt_medslikII_workflow"

# !conda run -p /work/asc/machine_learning/projects/iMagine/bayes_opt_workflow/env/mdk2_env \
export PYTHONPATH=$PYTHONPATH:$ROOT && \
python $ROOT/src/main/main.py \
--mode 0