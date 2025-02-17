import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

# Загрузка данных
df = pd.read_csv('D:\Program Files (x86)\Kudinov2\lab1\heart_failure_clinical_records_dataset.csv')
df = df.drop(columns=['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking', 'time', 'DEATH_EVENT'])
data = df.to_numpy(dtype='float')

# 1. Приведение данных к равномерному распределению
quantile_transformer = preprocessing.QuantileTransformer(n_quantiles=100, random_state=0)
data_quantile_scaled = quantile_transformer.fit_transform(data)

# 2. Гистограммы - исходные данные
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle('Исходные данные')
columns = df.columns
for i, ax in enumerate(axs.flatten()):
    ax.hist(data[:, i], bins=20)
    ax.set_title(columns[i])
plt.tight_layout()
plt.show()

# Гистограммы - равномерное распределение
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle('QuantileTransformer (равномерное распределение)')
for i, ax in enumerate(axs.flatten()):
    ax.hist(data_quantile_scaled[:, i], bins=20)
    ax.set_title(columns[i])
plt.tight_layout()
plt.show()

# 3. Влияние параметра n_quantiles
print("Параметр n_quantiles определяет количество квантилей, используемых для преобразования. Увеличение значения делает преобразование более точным, но может привести к переобучению на небольших данных и увеличению времени выполнения.")

# 4. Приведение к нормальному распределению
quantile_transformer_normal = preprocessing.QuantileTransformer(n_quantiles=100, output_distribution='normal', random_state=0)
data_quantile_normal = quantile_transformer_normal.fit_transform(data)

# 5. Гистограммы - нормальное распределение
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle('QuantileTransformer (нормальное распределение)')
for i, ax in enumerate(axs.flatten()):
    ax.hist(data_quantile_normal[:, i], bins=20)
    ax.set_title(columns[i])
plt.tight_layout()
plt.show()

# 6. PowerTransformer
power_transformer = preprocessing.PowerTransformer(method='yeo-johnson')
data_power_transformed = power_transformer.fit_transform(data)

# Гистограммы - PowerTransformer
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle('PowerTransformer (нормальное распределение)')
for i, ax in enumerate(axs.flatten()):
    ax.hist(data_power_transformed[:, i], bins=20)
    ax.set_title(columns[i])
plt.tight_layout()
plt.show()
