#!/bin/bash
export FLASK_APP=$PWD/services/project/__init__.py
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate py38
python $PWD/services/pyapi/manage.py run
