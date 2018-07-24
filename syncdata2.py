import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import time
from datetime import datetime, date, time, timedelta

 
#df = pd.read_excel('Perfect Notes and List of Recordings_20180416.xlsx', sheet_name='PSG_Actigraphy_merged')


def sync(patient_ID,PSG_code):

    df = pd.read_excel('Perfect Notes and List of Recordings_20180416.xlsx', sheet_name='PSG_Actigraphy_merged')
    #print(list(df))
    #print(df['PSG Date '])
    #a=df['PSG Date '].iloc[0]
    #print(a,type(a))
    #pd.to_datetime(df['PSG Date '].astype(str), format='%Y-%m-%d %H:%M:%S')
    ##pd.to_datetime(df['PSG Date '].astype(str), format='%Y-%m-%d', errors='coerce')
    #df['PSG Date '] = df['PSG Date '].dt.date
    #a=df['PSG Date '].iloc[0]
    #print(a,type(a))
    #%m-%d-%y %H:%M:%S
    #a=df['PSG Date '].iloc[0]
    #print(a,type(a))
    #2014-07-30 00:00:00
    
    #df["PSG Date "] = df["PSG Date "].dt.strftime("%d/%m/%Y")
    #df['PSG Date '] =  pd.to_datetime(df['PSG Date '], format='%Y-%m-%-d %H:%M:%S')
    
    #df['PSG Date '] = df['PSG Date '].apply(lambda x: x.date())
    #df2 = df.set_index(['original ID', 'PSG code'])
    #cols = ['PSG Date ', 'Recording Start Time ']
    #res = df2.loc[(patient_ID,PSG_code), cols].values.tolist()
    #PSG_date,recording_start_time = res[0]
    #print(type(patient_ID))
    #print(type(recording_start_time))
    #print(patient_ID,type(patient_ID))
    #print(recording_start_time,type(recording_start_time))
    #print(PSG_date,type(PSG_date))
    '''
    df3=pd.read_csv('perfect_stacked.csv')
    a=df3['Time'].iloc[0]
    print(a,type(a))
    b=df3['Date'].iloc[0]
    print(b,type(b))
    PSG_date = datetime.strptime(PSG_date, '%m/%d/%Y')
    print(PSG_date)
    '''
    df3=pd.read_csv('perfect_stacked.csv')
    #a=df3['Date'].iloc[0]
    #print(type(a))
    #print(type(PSG_date))
    #delta = timedelta(hours=21, minutes=21, seconds=21)
    
    #print(recording_start_time)
    #print(type(recording_start_time))
    #print(a)
    #print(abs(datetime.strptime(a, '%H:%M:%S').time()- recording_start_time))
    #print(abs(datetime.combine(date.min, a) - datetime.combine(date.min, beginning)))
    #df4=df3.loc[df3['identity'] == '197_$']
    #print(df4)
    ##df4.to_csv('hello.csv')
    #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    df3['Date'] =  pd.to_datetime(df3['Date'],format='%m/%d/%Y').dt.date
    df3['Time'] =  pd.to_datetime(df3['Time'],format='%H:%M:%S').dt.time
    a=df3['Date'].iloc[0]
    print(a,type(a))
    '''
    cond =  (df3['identity'] == patient_ID) 
    cond2 = (df3['Date'] == PSG_date)
    
    #print(cond)
    #print(cond2)
    #td = datetime.strptime(recording_start_time, '%H:%M:%S')
    #td = datetime.strptime(recording_start_time, '%H:%M:%S')
    print(df3[df3.loc[cond & cond2]['Time']])
    # series of time differnces
    #min_time_diff = abs(df.loc[cond & cond2]['time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S') - td))
    min_time_diff = abs(df3.loc[cond & cond2 ]['Time'].apply(lambda x: x-recording_start_time))
    print(min_time_diff)
    
    # return the row with the minimum time difference
    out = df3.loc[min_time_diff.idxmin()]

    out['difference'] = min_time_diff[min_time_diff.idxmin()].components.seconds
    print(out)
    return(out)
    '''
    
    
print(sync('197_$',487))
    

