import pandas as pd
import numpy as np
df = pd.read_csv('C:\Kudinov2\lab2\glass.csv')
var_names = list(df.columns) #получение имен признаков
labels = df.to_numpy('int')[:,-1] #метки классов
data = df.to_numpy('float')[:,:-1] #описательные признаки