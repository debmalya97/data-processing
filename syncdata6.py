import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import time
import datetime
from datetime import datetime,timedelta


def sync(patient_ID,PSG_code):

    df = pd.read_excel('Perfect Notes and List of Recordings_20180416.xlsx', sheet_name='PSG_Actigraphy_merged')
    df['PSG Date '] = pd.to_datetime(df['PSG Date '], errors='coerce').dt.date
    df2 = df.set_index(['original ID', 'PSG code'])
    cols = ['PSG Date ', 'Recording Start Time ']
    res = df2.loc[(patient_ID,PSG_code), cols].values.tolist()
    print(type(res))
    
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
    df4=df3.loc[min_time_diff.idxmin()]
    actigraphy_matched_time = df3.loc[min_time_diff.idxmin()]['Time']
    
    actigraphy_matched_time=datetime.strptime(actigraphy_matched_time, '%H:%M:%S')
    print(actigraphy_matched_time,type(actigraphy_matched_time))    
    #df3['Time'] = pd.to_timedelta(df3['Time'])
    df3['Time'] =  pd.to_datetime(df3['Time'], format='%H:%M:%S')
    a=df3['Time'].iloc[0] 
    print(a,type(a))
    
    df5=df3.loc[(df3['identity']==patient_ID) & (df3['Date'] == PSG_date) & (df3['Time'] >=actigraphy_matched_time )]
    #df3['Time'] = pd.to_timedelta(df3['Time'])
    #df3['Date'] = pd.to_datetime(df3['Date'])
    #row = df3.loc[df3['Time']==actigraphy_matched_time]
    #df5=df3.loc[(df3['identity']==patient_ID) & (df3['Date'] == row['Date'].values[0]) & (df3['Time']> row['Time'].values[0])]
    df5.to_csv('hi.csv')
    
    '''
    actigraphy_matched_time=datetime.strptime(actigraphy_matched_time,'%H:%M:%S')
    #print(actigraphy_matched_time,type(actigraphy_matched_time))
    #print(actigraphy_matched_time,type(actigraphy_matched_time))      
    time_difference= min_time_diff[min_time_diff.idxmin()].components.seconds
    if time_difference>0:
        actigraphy_sync_time=actigraphy_matched_time-timedelta(seconds=time_difference)
    else:
        actigraphy_sync_time=actigraphy_matched_time+timdelta(seconds=time_difference)
        
    
    #print(time_difference)
    #epoch_value=1     
    #print(actigraphy_matched_time,type(actigraphy_matched_time))
    
    #out=pd.DataFrame([[patient_ID,recording_start_time.strftime('%H:%M:%S'),PSG_date,actigraphy_matched_time.strftime('%H:%M:%S'),PSG_code,epoch_value,time_difference,actigraphy_sync_time.strftime('%H:%M:%S')]],columns=['id','PSG_start_time','PSG_Date','actigraphy_matched_time','PSG_value','epoch','time_diff(secs)','sync_time'])
    
    
    
    ############calculation after the first time is detected######################
    while actigraphy_matched_time!='23:59:30':
        recording_start_time+=timedelta(seconds=30)
        actigraphy_sync_time+=timedelta(seconds=30)
        actigraphy_matched_time+=timedelta(seconds=30)
        
        epoch_value+=1
        out=out.append(pd.DataFrame([[patient_ID,recording_start_time.strftime('%H:%M:%S'),PSG_date,actigraphy_matched_time.strftime('%H:%M:%S'),PSG_code,epoch_value,time_difference,actigraphy_sync_time.strftime('%H:%M:%S')]],columns=['id','PSG_start_time','PSG_Date','actigraphy_matched_time','PSG_value','epoch','time_diff(secs)','sync_time']))
        if actigraphy_matched_time.strftime('%H:%M:%S')=='23:59:30':
            break
    
    
    
    out.to_csv('197_$.csv',index='False')
    '''
    
print(sync('197_$',487))
    

