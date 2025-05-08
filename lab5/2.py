import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import random
import math

# =============================================
# 1. Иерархическая кластеризация для Iris данных
# =============================================

# Загрузка данных
try:
    data = pd.read_csv(r'C:\Kudinov2\lab5\iris.data', header=None)
    no_labeled_data = data.iloc[:, :4].values
except FileNotFoundError:
    print("Ошибка: Файл не найден. Проверьте путь к файлу.")
    exit()

# Кластеризация
hier = AgglomerativeClustering(n_clusters=3, linkage='average')
hier_labels = hier.fit_predict(no_labeled_data)

# =============================================
# 2. Визуализация результатов для Iris
# =============================================

features = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
pairs = [(0, 1), (1, 2), (2, 3)]
colors = ['#FF0000', '#00FF00', '#0000FF']

fig, axs = plt.subplots(1, 3, figsize=(18, 5))
for i, (x, y) in enumerate(pairs):
    for cluster in range(3):
        mask = hier_labels == cluster
        axs[i].scatter(
            no_labeled_data[mask, x], 
            no_labeled_data[mask, y],
            c=colors[cluster],
            s=30,
            label=f'Cluster {cluster+1}',
            alpha=0.6
        )
    axs[i].set_xlabel(features[x])
    axs[i].set_ylabel(features[y])
    axs[i].set_title(f'{features[x]} vs {features[y]}')
plt.tight_layout()
plt.show()

# Отличия от K-means:
# - Не требует задания числа кластеров априори (но мы его задали)
# - Строит иерархию кластеров
# - Более устойчив к шумам
# - Может находить кластеры произвольной формы

# =============================================
# 3. Исследование разных размеров кластеров
# =============================================

plt.figure(figsize=(15, 10))
for n_clusters in range(2, 6):
    hier = AgglomerativeClustering(n_clusters=n_clusters, linkage='average')
    labels = hier.fit_predict(no_labeled_data)
    
    plt.subplot(2, 2, n_clusters-1)
    plt.scatter(no_labeled_data[:, 2], no_labeled_data[:, 3], c=labels, cmap='viridis')
    plt.title(f'n_clusters = {n_clusters}')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')
plt.tight_layout()
plt.show()

# =============================================
# 4. Построение дендрограммы
# =============================================

# Для ускорения возьмем подвыборку
np.random.seed(42)
indices = np.random.choice(no_labeled_data.shape[0], 50, replace=False)
data_sample = no_labeled_data[indices]

plt.figure(figsize=(12, 6))
linked = linkage(data_sample, 'average')
dendrogram(linked, truncate_mode='level', p=6)
plt.title('Дендрограмма (уровень 6)')
plt.xlabel('Индекс образца')
plt.ylabel('Расстояние')
plt.show()

# =============================================
# 5-7. Генерация данных и кластеризация колец
# =============================================

# Генерация данных
np.random.seed(42)
data1 = np.zeros([250,2])
for i in range(250):
    r = random.uniform(1, 3)
    a = random.uniform(0, 2 * math.pi)
    data1[i,0] = r * math.sin(a)
    data1[i,1] = r * math.cos(a)

data2 = np.zeros([500,2])
for i in range(500):
    r = random.uniform(5, 9)
    a = random.uniform(0, 2 * math.pi)
    data2[i,0] = r * math.sin(a)
    data2[i,1] = r * math.cos(a)

data = np.vstack((data1, data2))

# Кластеризация
hier_ring = AgglomerativeClustering(n_clusters=2, linkage='ward')
ring_labels = hier_ring.fit_predict(data)

# Визуализация
plt.figure(figsize=(8, 6))
plt.scatter(data[ring_labels == 0, 0], data[ring_labels == 0, 1], 
            c='red', s=30, alpha=0.5, label='Cluster 1')
plt.scatter(data[ring_labels == 1, 0], data[ring_labels == 1, 1], 
            c='blue', s=30, alpha=0.5, label='Cluster 2')
plt.title('Кластеризация двух колец (ward linkage)')
plt.legend()
plt.show()

# =============================================
# 8. Исследование разных типов связи (linkage)
# =============================================

linkage_types = ['ward', 'complete', 'average', 'single']

plt.figure(figsize=(15, 10))
for i, linkage in enumerate(linkage_types, 1):
    hier = AgglomerativeClustering(n_clusters=2, linkage=linkage)
    labels = hier.fit_predict(data)
    
    plt.subplot(2, 2, i)
    plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='rainbow', s=30, alpha=0.6)
    plt.title(f'Linkage type: {linkage}')
plt.tight_layout()
plt.show()

"""
Анализ результатов для колец:
1. Ward linkage - дает наилучшее разделение колец
2. Complete linkage - также хорошо справляется
3. Average linkage - частичное смешение кластеров
4. Single linkage - полностью ошибочное разделение

Лучшие типы связей для колец:
- Ward: минимизирует дисперсию внутри кластеров
- Complete: учитывает максимальные расстояния
Не подходят:
- Average и Single: чувствительны к локальным структурам
"""