export PYWPS_CFG=/usr/people/mihajlov/PyWPS-pywps-3.2.2/pywps/pywps.cfg
export PYWPS_PROCESSES=/usr/people/mihajlov/python/clipc/prov
export PYWPS_TEMPLATES=/usr/people/mihajlov/PyWPS-pywps-3.2.2/pywps/Templates
#export NCARG_ROOT="/home/wps/software/install" 
#export PORTAL_SCRIPTS=/home/wps/pywps/scripts/
export POF_OUTPUT_URL=http://127.0.0.1
export POF_OUTPUT_PATH=/usr/people/mihajlov/python/clipc/prov
#export LD_LIBRARY_PATH=/home/wps/software/install/lib:$LD_LIBRARY_PATH
#export PATH=/home/wps/software/install/bin:$PATH
#export MPLCONFIGDIR=/home/wps/tmp/
#. /home/wps/pywps/wps-virtenv/bin/activate
#export PYTHONPATH=/usr/lib64/python2.6/site-packages/:$PYTHONPATH
export PYTHONPATH=/usr/people/mihajlov/PyWPS-pywps-3.2.2/:$PYTHONPATH
export PYTHONPATH=$PYWPS_PROCESSES:$PYTHONPATH
export PYTHONPATH=/usr/people/mihajlov/python/clipc/prov/:$PYTHONPATH

python knmi.wps.py

