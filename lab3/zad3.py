import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori


all_data = pd.read_csv('C:\Kudinov2\lab3\dataset_group.csv', header=None)

# 2. Формирование списка уникальных идентификаторов транзакций и товаров
unique_id = list(set(all_data[1]))
items = list(set(all_data[2]))

# 3. Формирование датасета в виде списка транзакций
dataset = [[elem for elem in all_data[all_data[1] == id][2] if elem in items] for id in unique_id]

# 4. One-hot encoding с использованием TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)

# 5. Применение алгоритма Apriori с min_support=0.3
results = apriori(df, min_support=0.3, use_colnames=True)
results['length'] = results['itemsets'].apply(lambda x: len(x))
print(results)

# 6. Ограничение максимального размера набора единицей
results = apriori(df, min_support=0.3, use_colnames=True, max_len=1)
print(results)

# 7. Вывод только наборов размера 2 и их количество
results = apriori(df, min_support=0.3, use_colnames=True)
results['length'] = results['itemsets'].apply(lambda x: len(x))
results = results[results['length'] == 2]
print(results)
print('\nCount of result itemsets = ', len(results))

# 8. Построение графика зависимости количества наборов от уровня поддержки
supports = np.arange(0.05, 1.0, 0.01)
counts = []
for s in supports:
    res = apriori(df, min_support=s, use_colnames=True)
    counts.append(len(res))

plt.plot(supports, counts, marker='o')
plt.xlabel('Уровень поддержки')
plt.ylabel('Количество наборов')
plt.title('Зависимость количества наборов от уровня поддержки')
plt.grid()
plt.show()

# 9. Определение уровней поддержки, при которых перестают генерироваться наборы
for s in supports:
    res = apriori(df, min_support=s, use_colnames=True)
    if res.empty:
        print(f'При уровне поддержки {s} наборы перестали генерироваться')
        break

# 10. Создание нового датасета из элементов, попадающих в наборы размера 1 при min_support=0.38
results = apriori(df, min_support=0.38, use_colnames=True, max_len=1)
new_items = [list(elem)[0] for elem in results['itemsets']]
new_dataset = [[elem for elem in all_data[all_data[1] == id][2] if elem in new_items] for id in unique_id]

# 11. Приведение нового датасета к one-hot encoding
te = TransactionEncoder()
te_ary = te.fit(new_dataset).transform(new_dataset)
new_df = pd.DataFrame(te_ary, columns=te.columns_)

# 12. Анализ нового датасета при min_support=0.3
new_results = apriori(new_df, min_support=0.3, use_colnames=True)
print(new_results)

# 13. Анализ нового датасета при min_support=0.15, фильтрация по 'yogurt' и 'waffles'
new_results = apriori(new_df, min_support=0.15, use_colnames=True)
new_results['length'] = new_results['itemsets'].apply(lambda x: len(x))
filtered_results = new_results[(new_results['length'] > 1) & (new_results['itemsets'].apply(lambda x: 'yogurt' in x or 'waffles' in x))]
print(filtered_results)

# 14. Создание датасета из элементов, не вошедших в новый датасет
remaining_items = list(set(items) - set(new_items))
remaining_dataset = [[elem for elem in all_data[all_data[1] == id][2] if elem in remaining_items] for id in unique_id]
te_ary = te.fit(remaining_dataset).transform(remaining_dataset)
remaining_df = pd.DataFrame(te_ary, columns=te.columns_)

# 15. Анализ оставшегося датасета
remaining_results = apriori(remaining_df, min_support=0.3, use_colnames=True)
print(remaining_results)

# 16. Фильтрация наборов, где хотя бы два элемента начинаются на 's'
def starts_with_s(itemset):
    return sum([1 for item in itemset if item.startswith('s')]) >= 2

filtered_results_s = new_results[new_results['itemsets'].apply(starts_with_s)]
print(filtered_results_s)

# 17. Вывод наборов с min_support от 0.1 до 0.25
for s in np.arange(0.1, 0.26, 0.01):
    res = apriori(new_df, min_support=s, use_colnames=True)
    print(f'Уровень поддержки: {s}, количество наборов: {len(res)}')