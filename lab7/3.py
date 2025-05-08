import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, tree
from sklearn.model_selection import train_test_split

# 1. Загрузка и подготовка данных
data = pd.read_csv(r'C:\Kudinov2\lab7\iris.data', header=None)
X = data.iloc[:, :4].to_numpy()
labels = data.iloc[:, 4].to_numpy()

le = preprocessing.LabelEncoder()
Y = le.fit_transform(labels)

# 2. Базовое разделение данных
ZACHETKA_ID = 12345  # НОМЕР ЗАЧЕТНОЙ КНИЖКИ
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, 
    test_size=0.5, 
    random_state=ZACHETKA_ID
)

def decision_tree_task():
    # 3. Базовая классификация деревом
    clf = tree.DecisionTreeClassifier(random_state=ZACHETKA_ID)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    # 4. Результаты классификации
    errors = (y_test != y_pred).sum()
    accuracy = clf.score(X_test, y_test)
    
    print(f"Неправильно классифицировано: {errors}")
    print(f"Точность классификации: {accuracy:.4f}")
    print(f"Количество листьев: {clf.get_n_leaves()}")
    print(f"Глубина дерева: {clf.get_depth()}")

    # 5. Визуализация дерева
    plt.figure(figsize=(20, 10))
    tree.plot_tree(clf, 
                   feature_names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
                   class_names=le.classes_,
                   filled=True, 
                   rounded=True)
    plt.title("Визуализация классифицирующего дерева")
    plt.show()

def tree_size_analysis():
    # 6. Анализ зависимости от размера выборки
    test_sizes = np.arange(0.05, 0.96, 0.05)
    metrics = {
        'errors': [],
        'accuracy': [],
        'leaves': [],
        'depth': []
    }

    for size in test_sizes:
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, Y, 
            test_size=size, 
            random_state=ZACHETKA_ID
        )
        clf = tree.DecisionTreeClassifier(random_state=ZACHETKA_ID)
        clf.fit(X_tr, y_tr)
        y_pr = clf.predict(X_te)
        
        metrics['errors'].append((y_te != y_pr).mean())
        metrics['accuracy'].append(clf.score(X_te, y_te))
        metrics['leaves'].append(clf.get_n_leaves())
        metrics['depth'].append(clf.get_depth())

    # Визуализация
    plt.figure(figsize=(15, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(test_sizes, metrics['errors'], 'r--')
    plt.title('Доля ошибок')
    
    plt.subplot(2, 2, 2)
    plt.plot(test_sizes, metrics['accuracy'], 'g-')
    plt.title('Точность')
    
    plt.subplot(2, 2, 3)
    plt.plot(test_sizes, metrics['leaves'], 'b:')
    plt.title('Количество листьев')
    
    plt.subplot(2, 2, 4)
    plt.plot(test_sizes, metrics['depth'], 'm-.')
    plt.title('Глубина дерева')
    
    plt.tight_layout()
    plt.show()

def tree_parameters_analysis():
    # 7. Анализ различных параметров
    parameters = {
        'criterion': ['gini', 'entropy'],
        'splitter': ['best', 'random'],
        'max_depth': [None, 2, 3, 4],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    results = []
    for criterion in parameters['criterion']:
        for splitter in parameters['splitter']:
            for max_depth in parameters['max_depth']:
                for min_samples_split in parameters['min_samples_split']:
                    for min_samples_leaf in parameters['min_samples_leaf']:
                        clf = tree.DecisionTreeClassifier(
                            criterion=criterion,
                            splitter=splitter,
                            max_depth=max_depth,
                            min_samples_split=min_samples_split,
                            min_samples_leaf=min_samples_leaf,
                            random_state=ZACHETKA_ID
                        )
                        clf.fit(X_train, y_train)
                        acc = clf.score(X_test, y_test)
                        results.append({
                            'params': f"{criterion}|{splitter}|{max_depth}|{min_samples_split}|{min_samples_leaf}",
                            'accuracy': acc,
                            'leaves': clf.get_n_leaves(),
                            'depth': clf.get_depth()
                        })

    # Вывод топ-5 параметров
    results.sort(key=lambda x: x['accuracy'], reverse=True)
    print("\nТоп-5 комбинаций параметров:")
    for i, res in enumerate(results[:5]):
        print(f"{i+1}. {res['params']}")
        print(f"Точность: {res['accuracy']:.4f}, Листья: {res['leaves']}, Глубина: {res['depth']}\n")

# Запуск задач
print("\n" + "="*50, "Базовый анализ дерева", "="*50)
decision_tree_task()

print("\n" + "="*50, "Анализ размера выборки", "="*50)
tree_size_analysis()

print("\n" + "="*50, "Анализ параметров", "="*50)
tree_parameters_analysis()