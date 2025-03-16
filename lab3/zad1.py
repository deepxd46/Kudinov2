import pandas as pd
import numpy as np

all_data = pd.read_csv('C:\Kudinov2\lab3\dataset_group.csv',header=None)

unique_id = list(set(all_data[1]))
print(len(unique_id)) #Выведем количество id

items = list(set(all_data[2]))
print(len(items)) #Выведем количество товаров

dataset = [[elem for elem in all_data[all_data[1] == id][2] if elem in
items] for id in unique_id]
