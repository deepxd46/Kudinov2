import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder

all_data = pd.read_csv('C:\Kudinov2\lab3\dataset_group.csv',header=None)

unique_id = list(set(all_data[1]))
print(len(unique_id)) #Выведем количество id

items = list(set(all_data[2]))
print(len(items)) #Выведем количество товаров

dataset = [[elem for elem in all_data[all_data[1] == id][2] if elem in
items] for id in unique_id]

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
print(df)

'''
Строки (индексы): Каждая строка соответствует одной транзакции или одному идентификатору из unique_id. 
Порядок строк определяется порядком элементов в списке unique_id, который формируется из множества 
(поэтому порядок может быть произвольным).
Столбцы: Каждый столбец соответствует отдельному уникальному товару из items. Названия столбцов — это сами товары.
Ячейки:
True: Если в данной транзакции (строке) присутствует соответствующий товар (столбец).
False: Если товара в транзакции нет.
'''