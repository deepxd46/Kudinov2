import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

# Чтение данных из CSV
all_data = pd.read_csv(r'C:\Kudinov2\lab4\groceries - groceries.csv')

# Список товаров для анализа
items = ['whole milk', 'yogurt', 'soda', 'tropical fruit', 'shopping bags',
         'sausage', 'whipped/sour cream', 'rolls/buns', 'other vegetables', 'root vegetables',
         'pork', 'bottled water', 'pastry', 'citrus fruit', 'canned beer', 'bottled beer']

# Преобразуем данные в numpy массив
np_data = all_data.to_numpy()

# Преобразуем данные в список строк, где каждая строка содержит только товары из списка
np_data = [[elem for elem in row[1:] if isinstance(elem, str) and elem in items] for row in np_data]

# Фильтруем транзакции, оставив только те, длина которых больше 1
np_data = [row for row in np_data if len(row) > 1]

# Шаг 1: Преобразуем данные с использованием TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(np_data).transform(np_data)
data = pd.DataFrame(te_ary, columns=te.columns_)

# Шаг 2: Получаем частые наборы с использованием FPGrowth
result = fpgrowth(data, min_support=0.05, use_colnames=True)
print("\nЧастые наборы товаров:")
print(result)

# Шаг 3: Проведение ассоциативного анализа с минимальным порогом 0.3
rules = association_rules(result, min_threshold=0.3)
print("\nАссоциативные правила:")
print(rules)

# Шаг 4: Объяснение 
# - antecedents: товары, которые предсказывают другие товары
# - consequents: товары, которые предсказываются другими товарами
# - support: доля транзакций, содержащих ассоциированные товары
# - confidence: вероятность того, что второй товар появится в транзакции, если первый товар уже есть
# - lift: метрика, оценивающая, насколько сильно ассоциация между товарами выше случайной вероятности

# Шаг 5: Построение ассоциативных правил для различных метрик
rules_confidence = association_rules(result, min_threshold=0.3, metric='confidence')
rules_lift = association_rules(result, min_threshold=0.3, metric='lift')
rules_support = association_rules(result, min_threshold=0.3, metric='support')

print("\nПравила на основе confidence:")
print(rules_confidence)
print("\nПравила на основе lift:")
print(rules_lift)
print("\nПравила на основе support:")
print(rules_support)

# Шаг 6: Рассчитаем среднее, медиану и СКО для каждой метрики
print("\nСредние значения метрик:")
print("Среднее для confidence:", rules_confidence['confidence'].mean())
print("Среднее для lift:", rules_lift['lift'].mean())
print("Среднее для support:", rules_support['support'].mean())

print("\nМедианы метрик:")
print("Медиана для confidence:", rules_confidence['confidence'].median())
print("Медиана для lift:", rules_lift['lift'].median())
print("Медиана для support:", rules_support['support'].median())

print("\nСКО для метрик:")
print("СКО для confidence:", rules_confidence['confidence'].std())
print("СКО для lift:", rules_lift['lift'].std())
print("СКО для support:", rules_support['support'].std())

# Шаг 7: Построение графа для ассоциативных правил
G = nx.DiGraph()

# Добавляем вершины и ребра
for index, row in rules_confidence.iterrows():
    antecedent = list(row['antecedents'])[0]  # Берем только один элемент
    consequent = list(row['consequents'])[0]
    support = row['support']
    confidence = row['confidence']
    
    # Добавляем ребро от antecedent к consequent с аттрибутами support и confidence
    G.add_edge(antecedent, consequent, weight=support, confidence=confidence)

# Отображаем граф
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.15, iterations=20)
labels = nx.get_edge_attributes(G, 'confidence')
weights = nx.get_edge_attributes(G, 'weight')

nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1.5, alpha=0.7, edge_color='gray')
nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.title('Граф ассоциативных правил с confidence и support')
plt.show()

# Шаг 8: Анализ полученного графа
# Граф позволяет увидеть, какие товары часто покупаются вместе. Толщина ребра отображает уровень поддержки (support),
# а подпись на ребре — это уверенность (confidence). Этот граф помогает понять, какие товары имеют сильные ассоциации.

# Шаг 9: Предложения по визуализации
# Для более детализированного анализа можно использовать:
# - Гистограмму для отображения самых популярных товаров.
# - Тепловую карту для отображения частоты покупки разных комбинаций товаров.
# - Круговую диаграмму для визуализации частых наборов товаров.
