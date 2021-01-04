#!/bin/bash
export FLASK_APP=$PWD/services/pyapi/project/__init__.py
export FLASK_DEBUG=1
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate py38
python $PWD/services/pyapi/manage.py run
