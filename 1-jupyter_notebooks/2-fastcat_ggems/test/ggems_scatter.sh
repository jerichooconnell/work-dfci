#!/bin/bash

cd /home/jericho/1-Workspace/1-jupyter_notebooks/2-fastcat_ggems/test 

python /home/jericho/Software/fastcat/fastcat/ggems_scatter_script.py /home/jericho/1-Workspace/1-jupyter_notebooks/2-fastcat_ggems/test/ggems_1e09_121kVp.pkl --angle 0 --number 0 --flood_field True
python /home/jericho/Software/fastcat/fastcat/ggems_scatter_script.py /home/jericho/1-Workspace/1-jupyter_notebooks/2-fastcat_ggems/test/ggems_1e09_121kVp.pkl --angle 0.0 --number 0
python /home/jericho/Software/fastcat/fastcat/ggems_scatter_script.py /home/jericho/1-Workspace/1-jupyter_notebooks/2-fastcat_ggems/test/ggems_1e09_121kVp.pkl --angle 6.283185307179586 --number 1
