import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, RobustScaler

# Загрузка данных
df = pd.read_csv('D:\\Program Files (x86)\\Kudinov2\\lab1\\heart_failure_clinical_records_dataset.csv')
df = df.drop(columns=['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking', 'time', 'DEATH_EVENT'])

features = df.columns

# Функция для построения гистограмм
def plot_histograms(data, title):
    n_bins = 20
    fig, axs = plt.subplots(2, 3, figsize=(12, 8))
    fig.suptitle(title)
    for i, ax in enumerate(axs.flatten()):
        ax.hist(data[:, i], bins=n_bins)
        ax.set_title(features[i])
    plt.tight_layout()
    plt.show()

# Исходные данные
data = df.to_numpy(dtype='float')
plot_histograms(data, 'Original Data')

# 1. MinMaxScaler
scaler_minmax = MinMaxScaler()
data_minmax = scaler_minmax.fit_transform(data)
plot_histograms(data_minmax, 'MinMaxScaler Data')

print("MinMaxScaler - Min values:")
print(pd.DataFrame(scaler_minmax.data_min_, index=features, columns=['Min Values']))
print("\nMinMaxScaler - Max values:")
print(pd.DataFrame(scaler_minmax.data_max_, index=features, columns=['Max Values']))

# 2. MaxAbsScaler
scaler_maxabs = MaxAbsScaler()
data_maxabs = scaler_maxabs.fit_transform(data)
plot_histograms(data_maxabs, 'MaxAbsScaler Data')

# 3. RobustScaler
scaler_robust = RobustScaler()
data_robust = scaler_robust.fit_transform(data)
plot_histograms(data_robust, 'RobustScaler Data')

# 4. Функция для приведения к диапазону [-5, 10]
def scale_to_range(data, min_val=-5, max_val=10):
    scaler = MinMaxScaler(feature_range=(min_val, max_val))
    return scaler.fit_transform(data)

data_custom_range = scale_to_range(data, -5, 10)
plot_histograms(data_custom_range, 'Custom Range [-5, 10] Data')
