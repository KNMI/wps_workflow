export PYWPS_CFG=/usr/people/mihajlov/pywps-pywps-3.2.5/pywps/pywps.cfg
export PYWPS_PROCESSES=/usr/people/mihajlov/python/clipc/prov
export PYWPS_TEMPLATES=/usr/people/mihajlov/pywps-pywps-3.2.5/pywps/Templates
export POF_OUTPUT_URL=http://127.0.0.1
export POF_OUTPUT_PATH=/usr/people/mihajlov/python/clipc/prov
export PYTHONPATH=/usr/people/mihajlov/pywps-pywps-3.2.5/:$PYTHONPATH
export PYTHONPATH=$PYWPS_PROCESSES:$PYTHONPATH
export PYTHONPATH=/usr/people/mihajlov/python/clipc/prov/:$PYTHONPATH

python knmi.wps.py

