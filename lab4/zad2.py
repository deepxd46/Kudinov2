import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth

# Чтение данных из CSV
all_data = pd.read_csv(r'C:\Kudinov2\lab4\groceries - groceries.csv')

# Преобразуем данные в numpy массив
np_data = all_data.to_numpy()

# Преобразуем данные в список строк, где каждая строка содержит товары
np_data = [[elem for elem in row[1:] if isinstance(elem, str)] for row in np_data]

# Шаг 1: Преобразование данных с использованием TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(np_data).transform(np_data)
data = pd.DataFrame(te_ary, columns=te.columns_)

# Шаг 2: Проведение анализа с использованием FPGrowth при уровне поддержки 0.03
result_fpgrowth = fpgrowth(data, min_support=0.03, use_colnames=True)
print("Результаты для FPGrowth:")
print(result_fpgrowth)

# Шаг 3: Анализ минимальных и максимальных значений для уровня поддержки для набора из 1, 2 и т.д. объектов
result_fpgrowth['length'] = result_fpgrowth['itemsets'].apply(lambda x: len(x))
min_support_fpgrowth = result_fpgrowth.groupby('length')['support'].min()
max_support_fpgrowth = result_fpgrowth.groupby('length')['support'].max()

print("\nМинимальное значение уровня поддержки по количеству элементов:")
print(min_support_fpgrowth)
print("\nМаксимальное значение уровня поддержки по количеству элементов:")
print(max_support_fpgrowth)

# Шаг 4: Преобразуем набор данных, чтобы он содержал ограниченный набор товаров
items = ['whole milk', 'yogurt', 'soda', 'tropical fruit', 'shopping bags',
         'sausage', 'whipped/sour cream', 'rolls/buns', 'other vegetables', 'root vegetables',
         'pork', 'bottled water', 'pastry', 'citrus fruit', 'canned beer', 'bottled beer']

# Преобразуем данные, оставив только товары из списка
np_data = all_data.to_numpy()
np_data = [[elem for elem in row[1:] if isinstance(elem, str) and elem in items] for row in np_data]

# Преобразование данных с использованием TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(np_data).transform(np_data)
data_reduced = pd.DataFrame(te_ary, columns=te.columns_)

# Шаг 5: Анализ с использованием FPGrowth для нового набора данных
result_reduced_fpgrowth = fpgrowth(data_reduced, min_support=0.03, use_colnames=True)
print("\nРезультаты для FPGrowth с ограниченным набором товаров:")
print(result_reduced_fpgrowth)

# Шаг 6: Построим гистограмму для каждого товара (Топ 10 товаров)
item_counts = data.sum()
sorted_item_counts = item_counts.sort_values(ascending=False)
top_10_items = sorted_item_counts.head(10)

# Строим гистограмму
plt.figure(figsize=(10, 6))
top_10_items.plot(kind='bar', color='skyblue')
plt.title('Топ 10 самых часто встречаемых товаров')
plt.xlabel('Товары')
plt.ylabel('Частота')
plt.xticks(rotation=45)
plt.show()

# Шаг 7: Построим график изменения количества получаемых правил от уровня поддержки
support_values = np.arange(0.01, 0.1, 0.01)
rules_count_fpgrowth = []

for support in support_values:
    result_fpgrowth = fpgrowth(data_reduced, min_support=support, use_colnames=True)
    rules_count_fpgrowth.append(len(result_fpgrowth))

# Строим график
plt.figure(figsize=(10, 6))
plt.plot(support_values, rules_count_fpgrowth, label='FPGrowth', marker='o')
plt.xlabel('Минимальная поддержка')
plt.ylabel('Количество правил')
plt.title('Изменение количества правил в зависимости от уровня поддержки')
plt.legend()
plt.grid(True)
plt.show()



'''
При ограничении данных товарами из выбранного списка, количество частых наборов и правил будет уменьшаться.

Товары, не входящие в этот список, больше не будут участвовать в анализе, 
что приведет к менее разнообразным результатам.

В FPGrowth можно ожидать меньшее количество ассоциативных правил, 
поскольку в данных меньше объектов и ограничен выбор товаров.

График демонстрирует, что при увеличении уровня поддержки количество получаемых правил уменьшается. 
Это отражает более строгие требования к частоте появления наборов товаров и помогает выявить более значимые и 
частые ассоциативные связи в данных.

'''