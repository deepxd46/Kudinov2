from sklearn.decomposition import PCA, FactorAnalysis
import matplotlib.pyplot as plt
from sklearn import preprocessing
import pandas as pd

# Загрузка данных
df = pd.read_csv(r'C:\Kudinov2\lab2\glass.csv')  # Использование raw-строки
data = df.to_numpy()[:, :-1].astype(float)  # Описательные признаки, преобразование в float
labels = df.to_numpy()[:, -1].astype(int)  # Метки классов, преобразование в int

# Масштабирование данных
data = preprocessing.minmax_scale(data)

# 1. Понижение размерности с использованием PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(data)

# 2. Понижение размерности с использованием FactorAnalysis
fa = FactorAnalysis(n_components=2)
fa_data = fa.fit_transform(data)

# 3. Диаграмма рассеяния после PCA
plt.scatter(pca_data[:, 0], pca_data[:, 1], c=labels, cmap='hsv')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA')
plt.show()

# 4. Диаграмма рассеяния после FactorAnalysis
plt.scatter(fa_data[:, 0], fa_data[:, 1], c=labels, cmap='hsv')
plt.xlabel('FA1')
plt.ylabel('FA2')
plt.title('Factor Analysis')
plt.show()

# 5. Сравнение объясненной дисперсии для PCA
print("Объясненная дисперсия для PCA:", pca.explained_variance_ratio_)

# Для FactorAnalysis логарифм правдоподобия
print("Log-likelihood для FactorAnalysis:", fa.score(data))
