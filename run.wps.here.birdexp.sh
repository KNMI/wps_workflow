export PYWPS_CFG=/home/spinuso/PyWPS-pywps-3.2.2/pywps/pywps.cfg
export PYWPS_PROCESSES=/home/spinuso/wps_workflow-master/
export PYWPS_TEMPLATES=/home/spinuso/PyWPS-pywps-3.2.2/pywps/Templates
#export NCARG_ROOT="/home/wps/software/install" 
#export PORTAL_SCRIPTS=/home/wps/pywps/scripts/
export POF_OUTPUT_URL=http://127.0.0.1
export POF_OUTPUT_PATH=/home/spinuso/python/wps_workflow-master/
#export LD_LIBRARY_PATH=/home/wps/software/install/lib:$LD_LIBRARY_PATH
#export PATH=/home/wps/software/install/bin:$PATH
#export MPLCONFIGDIR=/home/wps/tmp/
#. /home/wps/pywps/wps-virtenv/bin/activate
#export PYTHONPATH=/usr/lib64/python2.6/site-packages/:$PYTHONPATH
export PYTHONPATH=/home/spinuso/PyWPS-pywps-3.2.2/:$PYTHONPATH
export PYTHONPATH=$PYWPS_PROCESSES:$PYTHONPATH
export PYTHONPATH=/home/spinuso/wps_workflow-master/:$PYTHONPATH

python knmi.wps.py

