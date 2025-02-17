import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import KBinsDiscretizer

# Загрузка данных
df = pd.read_csv('D:\Program Files (x86)\Kudinov2\lab1\heart_failure_clinical_records_dataset.csv')
df = df.drop(columns=['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking', 'time', 'DEATH_EVENT'])

# Дискретизация признаков
n_bins = [3, 4, 3, 10, 2, 4]
columns = df.columns

kbins = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='uniform')
discretized_data = kbins.fit_transform(df)

# Построение гистограмм
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle('Гистограммы дискретизированных признаков')

for i, ax in enumerate(axs.ravel()):
    ax.hist(discretized_data[:, i], bins=n_bins[i], edgecolor='black')
    ax.set_title(columns[i])

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()

# Вывод диапазонов интервалов
for i, col in enumerate(columns):
    print(f"{col} - диапазоны интервалов: {kbins.bin_edges_[i]}")