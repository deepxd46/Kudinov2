import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('D:\Program Files (x86)\Kudinov2\lab1\heart_failure_clinical_records_dataset.csv')
df = df.drop(columns =['anaemia','diabetes','high_blood_pressure','sex','smoking','time','DEATH_EVENT'])


n_bins = 20
fig, axs = plt.subplots(2,3)
axs[0, 0].hist(df['age'].values, bins = n_bins)
axs[0, 0].set_title('age')
axs[0, 1].hist(df['creatinine_phosphokinase'].values, bins = n_bins)
axs[0, 1].set_title('creatinine_phosphokinase')
axs[0, 2].hist(df['ejection_fraction'].values, bins = n_bins)
axs[0, 2].set_title('ejection_fraction')
axs[1, 0].hist(df['platelets'].values, bins = n_bins)
axs[1, 0].set_title('platelets')
axs[1, 1].hist(df['serum_creatinine'].values, bins = n_bins)
axs[1, 1].set_title('serum_creatinine')
axs[1, 2].hist(df['serum_sodium'].values, bins = n_bins)
axs[1, 2].set_title('serum_sodium')
plt.show()

data = df.to_numpy(dtype='float')
print(data)

'''
age :

Диапазон: ~40–95 лет
Наибольшее количество наблюдений: около 60 лет

creatinine_phosphokinase :

Диапазон: ~20–8000
Наибольшая концентрация: около 100–200

ejection_fraction :

Диапазон: ~15–80
Наибольшее количество наблюдений: около 35

platelets :

Диапазон: ~100000–600000
Наибольшее количество наблюдений: около 250000

serum_creatinine :

Диапазон: ~0.5–9.0
Наибольшее количество наблюдений: около 1.0

serum_sodium :

Диапазон: ~110–150
Наибольшее количество наблюдений: около 140
'''