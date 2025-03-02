import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt





df = pd.read_csv('C:\Kudinov2\lab2\glass.csv')
var_names = list(df.columns) #получение имен признаков
labels = df.to_numpy('int')[:,-1] #метки классов
data = df.to_numpy('float')[:,:-1] #описательные признаки
data = preprocessing.minmax_scale(data)

fig, axs = plt.subplots(2,4)
for i in range(data.shape[1]-1):
    axs[i // 4, i % 4].scatter(data[:,i],data[:,(i+1)],c=labels,cmap='hsv')
    axs[i // 4, i % 4].set_xlabel(var_names[i])
    axs[i // 4, i % 4].set_ylabel(var_names[i+1])
plt.show()

'''
Цвета на диаграмме соответствуют классам в датасете через цветовую палитру 'hsv', 
где каждый класс (метка) отображается в уникальном цвете.
'''