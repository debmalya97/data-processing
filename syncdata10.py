import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import time
import datetime
from datetime import datetime,timedelta
import os

currentdir="E:\\ist2\\PSG all text files"

def get_PSG_file(PSG_code):
        
    
    for root, dirs, files in os.walk(currentdir):
        for name in files:
            if ((name==str(PSG_code)+"ExportedBuxton_SummaryData.edf") or (name==str(PSG_code)+"ExportedBuxton_SummaryData.TXT")):
                print(name,PSG_code)
                
                return(root,name)
                
                
                

def sync(patient_ID,PSG_code):
    #print(patient_ID)
    df = pd.read_csv('perfectnotes.csv')
    df['PSG Date '] = pd.to_datetime(df['PSG Date '], errors='coerce').dt.date
    #df2 = df.set_index(['identity (updated ID in actigraphy)'])
    df2 = df.set_index(['identity (updated ID in actigraphy)', 'PSG code'])
    cols = ['PSG Date ', 'Recording Start Time ']
    res = df2.loc[(patient_ID,PSG_code), cols].values.tolist()
    
    #print(len(res),type(res))    
    PSG_date,recording_start_time = res
    #print(PSG_date,type(recording_start_time))
       
    #recording_start_time = recording_start_time.strftime("%H:%M:%S")
       
    recording_start_time=datetime.strptime(recording_start_time, '%H:%M:%S')    
          
    df3=pd.read_csv('perfect_stacked.csv')
    #df4=df3.loc[df3['identity'] == '434']
    #print(df4)
    #df4.to_csv("434.csv")
    
    df3['Date'] =  pd.to_datetime(df3['Date'],format='%m/%d/%Y').dt.date
              
    cond =  (df3['identity'] == patient_ID) 
    cond2 = (df3['Date'] == PSG_date)
       
    # series of time differences
    min_time_diff = abs(df3.loc[cond & cond2 ]['Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S')-recording_start_time))
    #print(min_time_diff)              
    actigraphy_matched_time = df3.loc[min_time_diff.idxmin()]['Time']
    
    actigraphy_matched_time=datetime.strptime(actigraphy_matched_time, '%H:%M:%S')
    
    df3['Time'] =  pd.to_datetime(df3['Time'], format='%H:%M:%S')
    
    
    df4=df3.loc[(df3['identity']==patient_ID) & (df3['Date'] == PSG_date) & (df3['Time'] >=actigraphy_matched_time )]
    
             
    time_difference= min_time_diff[min_time_diff.idxmin()].components.seconds
    if actigraphy_matched_time>recording_start_time:
        actigraphy_sync_time=actigraphy_matched_time-timedelta(seconds=time_difference)
    elif actigraphy_matched_time<recording_start_time:
        actigraphy_sync_time=actigraphy_matched_time+timedelta(seconds=time_difference)
    else:
        actigraphy_sync_time=actigraphy_matched_time
        
    
             
    
    out=pd.DataFrame([[recording_start_time.strftime('%H:%M:%S'),actigraphy_matched_time.strftime('%H:%M:%S'),PSG_code,time_difference,actigraphy_sync_time.strftime('%H:%M:%S')]],columns=['PSG_start_time','actigraphy_matched_time','PSG_value','time_diff(secs)','sync_time'])
           
    ############calculation after the first time is detected######################
    cnt=0
    dataframe
    while :
        recording_start_time+=timedelta(seconds=30)
        actigraphy_sync_time+=timedelta(seconds=30)
        actigraphy_matched_time+=timedelta(seconds=30)
        
        
        out=out.append(pd.DataFrame([[recording_start_time.strftime('%H:%M:%S'),actigraphy_matched_time.strftime('%H:%M:%S'),PSG_code,time_difference,actigraphy_sync_time.strftime('%H:%M:%S')]],columns=['PSG_start_time','actigraphy_matched_time','PSG_value','time_diff(secs)','sync_time']))
        if :
            break
    
   
    out=out.reset_index()    
    df4=df4.reset_index()
    print("hello")
    '''
    def get_PSG_file(PSG_code):
        
        currentdir="E:\\ist2\\PSG all text files"
        for root, dirs, files in os.walk(currentdir):
            for name in files:
                if ((name==str(PSG_code)+"ExportedBuxton_SummaryData.edf") or (name==str(PSG_code)+"ExportedBuxton_SummaryData.TXT")):
                #print(name,patient_ID)
                
                    data= pd.read_csv(os.path.join(root, name),sep=",")
        
                    df6 = pd.concat([df4, out], axis=1)
                    df6.drop(['index', 'Epoch','Time','epoch'], axis=1, inplace=True)
                    df7=pd.concat([df6,data],join = 'inner', axis=1)
                    df7.to_csv(patient_ID+".csv")
                    print(patient_ID,name)
                
    '''
    file_root,file_name=get_PSG_file(PSG_code)
    
    data= pd.read_csv(os.path.join(file_root,file_name),sep=",")
        
    df6 = pd.concat([df4, out], axis=1)
    df6.drop(['index', 'Epoch','Time','epoch'], axis=1, inplace=True)
    df7=pd.concat([df6,data],join = 'inner', axis=1)
    df7.to_csv(patient_ID+".csv")
    print(patient_ID,name)
                
    
    
    
  
    

#main funtion
 
df = pd.read_csv('perfectnotes.csv')
#print(df)
for a,b in zip(df['identity (updated ID in actigraphy)'],df['PSG code']):#
    print(a,b)
    sync(a,b)
    
    
    

