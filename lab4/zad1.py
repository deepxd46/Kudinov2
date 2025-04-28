import pandas as pd
from collections import Counter

# Чтение данных из CSV
all_data = pd.read_csv(r'C:\Kudinov2\lab4\groceries - groceries.csv')
print(all_data)

# Преобразование данных в numpy массив
np_data = all_data.to_numpy()

# Преобразование данных в список строк
np_data = [[elem for elem in row[1:] if isinstance(elem, str)] for row in np_data]

# все товары в один список
all_items = []
for row in np_data:
    all_items.extend(row)

# Подсчитываем количество каждого товара
item_counts = Counter(all_items)

# Выводим результаты
for item, count in item_counts.items():
    print(f'{item}: {count}')
