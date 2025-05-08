import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import pairwise_distances_argmin

# Шаг 1: Загрузка данных
try:
    data = pd.read_csv(r'C:\Kudinov2\lab5\iris.data', header=None)
    no_labeled_data = data.iloc[:, :4].values
except FileNotFoundError:
    print("Ошибка: Файл не найден. Проверьте путь к файлу.")
    exit()

# Шаг 2: Кластеризация K-средних
kmeans = KMeans(init='k-means++', n_clusters=3, n_init=15)
kmeans.fit(no_labeled_data)
kmeans_centers = kmeans.cluster_centers_
kmeans_labels = pairwise_distances_argmin(no_labeled_data, kmeans_centers)

# Шаг 3: Визуализация попарных признаков
features = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
pairs = [(0, 1), (1, 2), (2, 3)]
colors = ['#4EACC5', '#FF9C34', '#4E9A06']

fig, axs = plt.subplots(1, 3, figsize=(18, 5))
for i, (x, y) in enumerate(pairs):
    for cluster in range(3):
        mask = kmeans_labels == cluster
        axs[i].scatter(
            no_labeled_data[mask, x], 
            no_labeled_data[mask, y],
            c=colors[cluster],
            s=30,
            label=f'Cluster {cluster+1}'
        )
        axs[i].scatter(
            kmeans_centers[cluster, x],
            kmeans_centers[cluster, y],
            c='red',
            s=200,
            marker='X',
            edgecolor='k'
        )
    axs[i].set_xlabel(features[x])
    axs[i].set_ylabel(features[y])
    axs[i].set_title(f'{features[x]} vs {features[y]}')
plt.tight_layout()
plt.show()

# Шаг 4: PCA визуализация
pca = PCA(n_components=2)
data_pca = pca.fit_transform(no_labeled_data)

# Создание meshgrid для областей
x_min, x_max = data_pca[:, 0].min() - 1, data_pca[:, 0].max() + 1
y_min, y_max = data_pca[:, 1].min() - 1, data_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))

# Предсказание для всей области
Z = kmeans.predict(pca.inverse_transform(np.c_[xx.ravel(), yy.ravel()]))
Z = Z.reshape(xx.shape)

plt.figure(figsize=(10, 6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap='viridis')
plt.scatter(data_pca[:, 0], data_pca[:, 1], c=kmeans_labels, cmap='viridis', s=50, edgecolor='k')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Кластеры в PCA пространстве')
plt.colorbar()
plt.show()

# Шаг 5: Исследование параметра init
plt.figure(figsize=(15, 5))

# Случайная инициализация
plt.subplot(121)
kmeans_random = KMeans(init='random', n_clusters=3, n_init=1).fit(no_labeled_data)
plt.scatter(data_pca[:, 0], data_pca[:, 1], c=kmeans_random.labels_, cmap='viridis')
plt.title('Random initialization')

# Ручная инициализация
plt.subplot(122)
manual_centers = np.array([[5.0, 3.4, 1.5, 0.2], [6.0, 2.9, 4.5, 1.5], [7.0, 3.2, 6.0, 2.0]])
kmeans_manual = KMeans(init=manual_centers, n_clusters=3, n_init=1).fit(no_labeled_data)
plt.scatter(data_pca[:, 0], data_pca[:, 1], c=kmeans_manual.labels_, cmap='viridis')
plt.title('Manual initialization')
plt.show()

# Шаг 6: Метод локтя
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, n_init=15).fit(no_labeled_data)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertia, marker='o', linestyle='--')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.xticks(range(1, 11))
plt.grid(True)
plt.show()

# Шаг 7: Пакетная кластеризация
mbk = MiniBatchKMeans(n_clusters=3, n_init=15, batch_size=100)
mbk_labels = mbk.fit_predict(no_labeled_data)

# Сравнение кластеров
disagree = (kmeans_labels != mbk_labels)
plt.figure(figsize=(8, 6))
plt.scatter(data_pca[:, 0], data_pca[:, 1], c=disagree, cmap='cool', s=50)
plt.title('Точки с разными метками кластеров\nмежду обычным и пакетным K-means')
plt.colorbar(label='Различие кластеров (1 = разные)')
plt.show()