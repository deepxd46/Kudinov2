import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

# Загрузка данных
data = pd.read_csv(r'C:\Kudinov2\lab7\iris.data', header=None)
print(f"Загружено данных: {data.shape[0]} записей, {data.shape[1]} колонок")
print("\nПервые 5 строк данных:")
print(data.head(), end='\n\n')

# Разделение на данные и метки
X = data.iloc[:, :4].to_numpy()
labels = data.iloc[:, 4].to_numpy()
print(f"Размерность признаков (X): {X.shape}")
print(f"Первые 5 меток: {labels[:5]}")

# Преобразование текстовых меток в числовые
le = preprocessing.LabelEncoder()
Y = le.fit_transform(labels)
print("\nСоответствие классов и чисел:", dict(zip(le.classes_, le.transform(le.classes_))))
print(f"Первые 5 преобразованных меток: {Y[:5]}")

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(
    X, Y,
    test_size=0.5,
    random_state=42
)
print("\n" + "="*50)
print(f"Обучающая выборка: {X_train.shape[0]} записей")
print(f"Тестовая выборка: {X_test.shape[0]} записей")
print("\nПримеры первых 3 записей:")
print("Признаки (X_train):\n", X_train[:3])
print("Метки (y_train):", y_train[:3])