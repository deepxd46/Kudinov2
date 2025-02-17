import pandas as pd
import numpy as np
df = pd.read_csv('D:\Program Files (x86)\Kudinov2\lab1\heart_failure_clinical_records_dataset.csv')
df = df.drop(columns =['anaemia','diabetes','high_blood_pressure','sex','smoking','time','DEATH_EVENT'])
print(df) 