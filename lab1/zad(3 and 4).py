import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

df = pd.read_csv('D:\Program Files (x86)\Kudinov2\lab1\heart_failure_clinical_records_dataset.csv')
df = df.drop(columns=['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking', 'time', 'DEATH_EVENT'])


data = df.to_numpy(dtype='float32')


scaler = preprocessing.StandardScaler().fit(data[:150, :])
data_scaled = scaler.transform(data)


means_before = np.mean(data, axis=0)
stds_before = np.std(data, axis=0)


means_after = np.mean(data_scaled, axis=0)
stds_after = np.std(data_scaled, axis=0)

columns = df.columns
print("Информация ДО стандартизации:")
for i in range(len(columns)):
    print(f"{columns[i]}: мат. ожидание = {means_before[i]:.2f}, СКО = {stds_before[i]:.2f}")

print("\nИнформация ПОСЛЕ стандартизации:")
for i in range(len(columns)):
    print(f"{columns[i]}: мат. ожидание = {means_after[i]:.2f}, СКО = {stds_after[i]:.2f}")


n_bins = 20
fig, axs = plt.subplots(2, 3, figsize=(10, 8))
axs[0, 0].hist(data_scaled[:, 0], bins=n_bins)
axs[0, 0].set_title('age')
axs[0, 1].hist(data_scaled[:, 1], bins=n_bins)
axs[0, 1].set_title('creatinine_phosphokinase')
axs[0, 2].hist(data_scaled[:, 2], bins=n_bins)
axs[0, 2].set_title('ejection_fraction')
axs[1, 0].hist(data_scaled[:, 3], bins=n_bins)
axs[1, 0].set_title('platelets')
axs[1, 1].hist(data_scaled[:, 4], bins=n_bins)
axs[1, 1].set_title('serum_creatinine')
axs[1, 2].hist(data_scaled[:, 5], bins=n_bins)
axs[1, 2].set_title('serum_sodium')

plt.tight_layout()
plt.show()

'''
До стандартизации исходные данные имеют разные масштабы и единицы измерения, некоторые признаки имеют сильный разброс значений.

После стандартизации среднее значение каждого признака стало около 0 . Стандартное отклонение (СКО) каждого признака стало равным 1.

До стандартизации:

Среднее и СКО имеют разные значения для каждого признака.

После стандартизации:

Среднее (мат. ожидание) ≈ 0
СКО ≈ 1'''