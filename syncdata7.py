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
    
    actigraphy_matched_time = df3.loc[min_time_diff.idxmin()]['Time']
    
    actigraphy_matched_time=datetime.strptime(actigraphy_matched_time, '%H:%M:%S')
    #print(actigraphy_matched_time,type(actigraphy_matched_time))    
    #df3['Time'] = pd.to_timedelta(df3['Time'])
    df3['Time'] =  pd.to_datetime(df3['Time'], format='%H:%M:%S')
    #a=df3['Time'].iloc[0] 
    #print(a,type(a))
    
    df4=df3.loc[(df3['identity']==patient_ID) & (df3['Date'] == PSG_date) & (df3['Time'] >=actigraphy_matched_time )]
    #df3['Time'] = pd.to_timedelta(df3['Time'])
    #df3['Date'] = pd.to_datetime(df3['Date'])
    #row = df3.loc[df3['Time']==actigraphy_matched_time]
    #df5=df3.loc[(df3['identity']==patient_ID) & (df3['Date'] == row['Date'].values[0]) & (df3['Time']> row['Time'].values[0])]
    #df4.to_csv("debmalya.csv")
    
    
    
    #print(actigraphy_matched_time,type(actigraphy_matched_time))
    #print(actigraphy_matched_time,type(actigraphy_matched_time))      
    time_difference= min_time_diff[min_time_diff.idxmin()].components.seconds
    if time_difference>0:
        actigraphy_sync_time=actigraphy_matched_time-timedelta(seconds=time_difference)
    else:
        actigraphy_sync_time=actigraphy_matched_time+timdelta(seconds=time_difference)
        
    
    #print(time_difference)
    epoch_value=1     
    #print(actigraphy_matched_time,type(actigraphy_matched_time))
    
    out=pd.DataFrame([[recording_start_time.strftime('%H:%M:%S'),actigraphy_matched_time.strftime('%H:%M:%S'),PSG_code,epoch_value,time_difference,actigraphy_sync_time.strftime('%H:%M:%S')]],columns=['PSG_start_time','actigraphy_matched_time','PSG_value','epoch','time_diff(secs)','sync_time'])
    
    
    
    ############calculation after the first time is detected######################
    while actigraphy_matched_time!='23:59:30':
        recording_start_time+=timedelta(seconds=30)
        actigraphy_sync_time+=timedelta(seconds=30)
        actigraphy_matched_time+=timedelta(seconds=30)
        
        epoch_value+=1
        out=out.append(pd.DataFrame([[recording_start_time.strftime('%H:%M:%S'),actigraphy_matched_time.strftime('%H:%M:%S'),PSG_code,epoch_value,time_difference,actigraphy_sync_time.strftime('%H:%M:%S')]],columns=['PSG_start_time','actigraphy_matched_time','PSG_value','epoch','time_diff(secs)','sync_time']))
        if actigraphy_matched_time.strftime('%H:%M:%S')=='23:59:30':
            break
    
    #df2['time'] = df1.time
#df2['matched_time'] = df2.matched_time
    #out.to_csv("dev.csv")
    #df4_T=df4.T
    #out_T=out.T
    out=out.reset_index()
    #out.to_csv("1.csv")
    df4=df4.reset_index()
    #df4.to_csv("2.csv")
    #df5=df4_T.join(out_T)
    #df6=df5.T
    #column_name_out=list(out)
    #df4[c] = df1[cols_to_copy]
    #df5=pd.concat([df4,out], ignore_index=True,axis=1)
    #data=pd.read_csv('487ExportedBuxton_Summary.Data')
    #df6=pd.append([df4,out],axis=1)
    #df6=df4.combine_first(out)
    #df6 = pd.merge(df4, out)
    #print(out.index.is_unique)    
    df6 = pd.concat([df4, out], axis=1)
    #df6 = pd.merge(df4,out, on=['identity','Date']) 
    #df4[column_name_out] = out
    
    df6.to_csv("final2.csv")
    
    
print(sync('197_$',487))
    

