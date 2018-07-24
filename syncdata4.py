import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import time
from datetime import datetime, date, time, timedelta

def sync(patient_ID,PSG_code): 

    df = pd.read_excel('Perfect Notes and List of Recordings_20180416.xlsx', sheet_name='PSG_Actigraphy_merged') 
    df['PSG Date '] = pd.to_datetime(df['PSG Date '], errors='coerce').dt.date 
    df['Recording Start Time '] = pd.to_datetime(df['Recording Start Time '].astype(str), errors='coerce') 
    df['Recording Start Time '] = pd.to_timedelta(df['Recording Start Time '].dt.strftime('%H:%M:%S')) 

    df2 = df.set_index(['original ID', 'PSG code']) 
    cols = ['PSG Date ', 'Recording Start Time '] 
    res = df2.loc[(patient_ID,PSG_code), cols].values.tolist() 
    PSG_date,recording_start_time = res[0] 
    print(recording_start_time,type(recording_start_time)) 

    df3=pd.read_csv('perfect_stacked.csv') 
    df3['Date'] = pd.to_datetime(df3['Date'],format='%m/%d/%Y').dt.date 
    df3['Time'] = pd.to_timedelta(pd.to_datetime(df3['Time'],format='%H:%M:%S')) 

    cond = (df3['identity'] == patient_ID) 
    cond2 = (df3['Date'] == PSG_date) 

    a=df3['Time'].iloc[0] 
    print(a,type(a)) 
    print(recording_start_time,type(recording_start_time)) 

    # series of time differences 
    min_time_diff = abs(df3.loc[cond & cond2, 'Time']) - recording_start_time 
    print(min_time_diff) 

    # return the row with the minimum time difference 
    out = df3.loc[min_time_diff.idxmin()] 

    out['difference'] = min_time_diff[min_time_diff.idxmin()] 
    print(out) 
    
print(sync('197_$',487))
        