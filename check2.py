import os
import pandas as pd
patient_ID="502"
currentdir="E:\\ist2\\PSG all text files"
data= pd.read_csv("502ExportedBuxton_SummaryData.txt",sep=",")
print(data)

for root, dirs, files in os.walk(currentdir):
    for name in files:
        #print(name)
        if ((name==patient_ID+"ExportedBuxton_SummaryData.edf") or (name==patient_ID+"ExportedBuxton_SummaryData.TXT")):
            data= pd.read_csv(name,sep=",")
            print(df)
            
           