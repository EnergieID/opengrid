# -*- coding: utf-8 -*-
"""
One-time script to consolidate all existing data and convert to UTC time and 
save one csv file per day.  Right after running this script, the opengrid VM 
should have been converted to UTC time!!!!!!!!



Created on Sat Jul 12 01:13:24 2014

@author: roel
"""

import os, sys
import inspect
import numpy as np
import matplotlib.pyplot as plt
import pytz
import datetime as dt

script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# add the path to opengrid to sys.path
sys.path.append(os.path.join(script_dir, os.pardir, os.pardir))
from opengrid.library import houseprint
from opengrid.library import fluksoapi

# script settings ############################################################
path_to_data = os.path.abspath('/home/roel/data/work/opengrid/work')

# get all sensors
hp = houseprint.load_houseprint_from_file('hp_anonymous.pkl')
sensors = []
for flukso_id, d in hp.fluksosensors.items():
    for sensor_id, s in d.items():
        # sensor_id is 1-6, s is {}
        try:
            sensors.append(s['Sensor'])
        except:
            pass

print("{} sensors found".format(len(sensors)))
        
for sensor in ['1e1e43f5edb4d5e43ab721c391410cde']:
    
    # create a single csv
    csv=fluksoapi.consolidate(folder=path_to_data, sensor=sensor)

    # load csv into dataframe
    df = fluksoapi.load_csv(csv)

    # convert to UTC
    edt=pytz.timezone('US/Eastern')
    df.index = df.index.tz_localize(edt)
    df.index = df.index.tz_convert('UTC')

    # save single csv file per day
    # first, create the datetimes for each day
    days=df.resample(rule='D').index
    for i in range(len(days)-1):
        df_day = df.ix[days[i]:days[i+1]]
        df_day = df_day.resample(rule='T')
        if not df_day.isnull().all()[1]:
            fluksoapi.save_csv(df_day, csvpath=os.path.join(path_to_data, 'daily'), 
                               fileNamePrefix='_'.join([flukso_id, sensor]))
        

    