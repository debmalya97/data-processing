import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import time
from datetime import datetime, date, time, timedelta


def sync(patient_ID,PSG_code):

    df = pd.read_excel('Perfect Notes and List of Recordings_20180416.xlsx', sheet_name='PSG_Actigraphy_merged')
    df['PSG Date '] = pd.to_datetime(df['PSG Date '], errors='coerce').dt.date
    df2 = df.set_index(['original ID', 'PSG code'])
    cols = ['PSG Date ', 'Recording Start Time ']
    res = df2.loc[(patient_ID,PSG_code), cols].values.tolist()
    PSG_date,recording_start_time = res[0]
    #print(recording_start_time,type(recording_start_time))
    
    recording_start_time = recording_start_time.strftime("%H:%M:%S")
    #print(recording_start_time,type(recording_start_time))
    
    recording_start_time=datetime.strptime(recording_start_time, '%H:%M:%S')    
    #print(recording_start_time,type(recording_start_time))
    
    
    df3=pd.read_csv('perfect_stacked.csv')
    df3['Date'] =  pd.to_datetime(df3['Date'],format='%m/%d/%Y').dt.date
        
    cond =  (df3['identity'] == patient_ID) 
    cond2 = (df3['Date'] == PSG_date)
    
    
    # series of time differences
    min_time_diff = abs(df3.loc[cond & cond2 ]['Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S')-recording_start_time))
    #print(min_time_diff)
    
    
    # return the row with the minimum time difference
    actigraphy_matched_time = df3.loc[min_time_diff.idxmin()]['Time']
    #print(actigraphy_matched_time)      
    time_difference= min_time_diff[min_time_diff.idxmin()].components.seconds
    #print(time_difference)
    
    out=pd.DataFrame([[patient_ID,recording_start_time.strftime('%H:%M:%S'),PSG_date,actigraphy_matched_time,PSG_code,1,time_difference]],columns=['id','PSG_start_time','PSG_Date','actigraphy_matched_time','PSG_value','epoch','time_diff(secs)'])
    print(out)
    
    
    
    
    
print(sync('197_$',487))
    

