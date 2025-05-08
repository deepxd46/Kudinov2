import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB, BernoulliNB
from sklearn.preprocessing import MinMaxScaler

# 1. Загрузка и подготовка данных
data = pd.read_csv(r'C:\Kudinov2\lab7\iris.data', header=None)
print(f"Загружено данных: {data.shape[0]} записей, {data.shape[1]} колонок")
print("\nПервые 5 строк данных:")
print(data.head(), end='\n\n')

# 2. Разделение на признаки и метки
X = data.iloc[:, :4].to_numpy()
labels = data.iloc[:, 4].to_numpy()
print(f"Размерность признаков (X): {X.shape}")
print(f"Первые 5 меток: {labels[:5]}")

# 3. Преобразование меток
le = preprocessing.LabelEncoder()
Y = le.fit_transform(labels)
print("\nСоответствие классов и чисел:", dict(zip(le.classes_, le.transform(le.classes_))))
print(f"Первые 5 преобразованных меток: {Y[:5]}")

# 4. Первоначальное разделение данных
ZACHETKA_ID = 12345  # НОМЕР ЗАЧЕТНОЙ КНИЖКИ ЗДЕСЬ!
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, 
    test_size=0.5, 
    random_state=ZACHETKA_ID
)
print("\n" + "="*50)
print(f"Обучающая выборка: {X_train.shape[0]} записей")
print(f"Тестовая выборка: {X_test.shape[0]} записей")

# 5. Гауссовский наивный Байес
def task_gnb():
    print("\n" + "="*50)
    print("Задание 1-2: GaussianNB")
    
    gnb = GaussianNB()
    y_pred = gnb.fit(X_train, y_train).predict(X_test)
    errors = (y_test != y_pred).sum()
    
    print(f"Неправильно классифицировано: {errors} ({errors/len(y_test)*100:.1f}%)")
    print("\nАтрибуты классификатора:")
    print(f"Количество классов: {gnb.classes_}")
    print(f"Вероятности классов: {gnb.class_prior_}")
    print(f"Средние признаки (theta_):\n{gnb.theta_}")
    print(f"Дисперсии признаков (sigma_):\n{gnb.var_}")
    
    accuracy = gnb.score(X_test, y_test)
    print(f"\nТочность классификации: {accuracy:.4f}")

# 6. График зависимости от размера выборки
def task_plot():
    print("\n" + "="*50)
    print("Задание 3: Анализ зависимости от размера выборки")
    
    test_sizes = np.arange(0.05, 0.96, 0.05)
    error_rates = []
    accuracies = []
    
    for size in test_sizes:
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, Y,
            test_size=size,
            random_state=ZACHETKA_ID
        )
        model = GaussianNB().fit(X_tr, y_tr)
        y_pr = model.predict(X_te)
        error_rates.append((y_te != y_pr).mean())
        accuracies.append(model.score(X_te, y_te))
    
    plt.figure(figsize=(12, 6))
    plt.plot(test_sizes, error_rates, 'r--', label='Доля ошибок')
    plt.plot(test_sizes, accuracies, 'b-', label='Точность')
    plt.xlabel('Доля тестовой выборки', fontsize=12)
    plt.ylabel('Значение метрики', fontsize=12)
    plt.title(f'Зависимость метрик от размера выборки (random_state={ZACHETKA_ID})', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()

# 7. Сравнение методов
def task_compare():
    print("\n" + "="*50)
    print("Задание 4: Сравнение методов Naive Bayes")
    
    # Масштабирование для MultinomialNB и BernoulliNB
    scaler = MinMaxScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        'GaussianNB': GaussianNB(),
        'MultinomialNB': MultinomialNB(),
        'ComplementNB': ComplementNB(),
        'BernoulliNB': BernoulliNB(binarize=0.5)
    }
    
    results = []
    for name, model in models.items():
        if name in ['MultinomialNB', 'BernoulliNB']:
            X_tr = X_train_scaled
            X_te = X_test_scaled
        else:
            X_tr = X_train
            X_te = X_test
            
        model.fit(X_tr, y_train)
        acc = model.score(X_te, y_test)
        results.append((name, acc))
    
    print("\nРезультаты классификации:")
    for name, acc in results:
        print(f"{name:<15}: {acc:.4f}")
    
    print("\nОсобенности методов:")
    print("1. GaussianNB: Предполагает нормальное распределение признаков")
    print("2. MultinomialNB: Оптимален для дискретных счетчиков (например, TF-IDF)")
    print("3. ComplementNB: Модификация MultinomialNB для несбалансированных данных")
    print("4. BernoulliNB: Работает с бинарными признаками (0/1)")


task_gnb()
task_plot()
task_compare()