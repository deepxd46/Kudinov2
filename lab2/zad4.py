import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA, KernelPCA, SparsePCA

# Загрузка данных
df = pd.read_csv('C:\Kudinov2\lab2\glass.csv')
var_names = list(df.columns)  # Получение имен признаков
labels = df.to_numpy('int')[:, -1]  # Метки классов
data = df.to_numpy('float')[:, :-1]  # Описательные признаки

# Масштабирование данных
data = preprocessing.minmax_scale(data)

# 1. Понижение размерности до 2 с использованием PCA
pca = PCA(n_components=2)
pca_data = pca.fit(data).transform(data)

# 2. Вывод объясненной дисперсии и собственных чисел
print("Объясненная дисперсия:", pca.explained_variance_ratio_)
print("Собственные числа:", pca.singular_values_)

# 3. Диаграмма рассеяния после PCA
plt.scatter(pca_data[:, 0], pca_data[:, 1], c=labels, cmap='hsv')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Scatter plot after PCA')
plt.show()

# 4. Определение количества компонент, которые объясняют не менее 85% дисперсии
pca_full = PCA()
pca_full.fit(data)
cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)

n_components_85 = np.argmax(cumulative_variance >= 0.85) + 1
print(f'Количество компонент, объясняющих не менее 85% дисперсии: {n_components_85}')

# 5. Восстановление данных с использованием inverse_transform
reconstructed_data = pca.inverse_transform(pca_data)

# Сравнение восстановленных данных с исходными
print("Исходные данные (первые 5 строк):", data[:5])
print("Восстановленные данные (первые 5 строк):", reconstructed_data[:5])

# 6. Исследование метода PCA при различных параметрах svd_solver
pca_auto = PCA(n_components=2, svd_solver='auto')
pca_full_solver = PCA(n_components=2, svd_solver='full')
pca_arpack = PCA(n_components=2, svd_solver='arpack')
pca_randomized = PCA(n_components=2, svd_solver='randomized')

# Фиттинг моделей
pca_auto.fit(data)
pca_full_solver.fit(data)
pca_arpack.fit(data)
pca_randomized.fit(data)

# Печать объясненной дисперсии для различных методов
print("Объясненная дисперсия (auto):", pca_auto.explained_variance_ratio_)
print("Объясненная дисперсия (full):", pca_full_solver.explained_variance_ratio_)
print("Объясненная дисперсия (arpack):", pca_arpack.explained_variance_ratio_)
print("Объясненная дисперсия (randomized):", pca_randomized.explained_variance_ratio_)

# 7. Исследование KernelPCA с различными ядрами
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
for kernel in kernels:
    kpca = KernelPCA(n_components=2, kernel=kernel)
    kpca_data = kpca.fit_transform(data)
    
    print(f"KernelPCA с ядром {kernel} - Объясненная дисперсия:")
    print(kpca.alphas_)

    # Диаграмма рассеяния после KernelPCA
    plt.scatter(kpca_data[:, 0], kpca_data[:, 1], c=labels, cmap='hsv')
    plt.xlabel(f'{kernel} - PC1')
    plt.ylabel(f'{kernel} - PC2')
    plt.title(f'Scatter plot after KernelPCA with {kernel} kernel')
    plt.show()

# 8. Определение параметров, при которых KernelPCA работает как PCA (с ядром 'linear')
kpca_linear = KernelPCA(n_components=2, kernel='linear')
kpca_data_linear = kpca_linear.fit_transform(data)

# Сравнение результатов KernelPCA с PCA
print("Объясненная дисперсия для PCA с ядром linear:")
print(kpca_linear.alphas_)

# 9. Исследование SparsePCA
sparse_pca = SparsePCA(n_components=2)
sparse_pca_data = sparse_pca.fit_transform(data)

print("Объясненная дисперсия для SparsePCA:")
print(sparse_pca.explained_variance_ratio_)

# Диаграмма рассеяния после SparsePCA
plt.scatter(sparse_pca_data[:, 0], sparse_pca_data[:, 1], c=labels, cmap='hsv')
plt.xlabel('SparsePC1')
plt.ylabel('SparsePC2')
plt.title('Scatter plot after SparsePCA')
plt.show()
