import pandas as pd
import numpy as np

# Фиксируем seed для воспроизводимости
np.random.seed(42)

# 1. Таблица клиентов
n_clients = 50
clients_data = {
    'client_id': range(1, n_clients + 1),
    'client_name': [f'Клиент_{i}' for i in range(1, n_clients + 1)],
    'city': np.random.choice(['Москва', 'СПб', 'Казань', 'Новосибирск', 'Екатеринбург'], n_clients),
    'registration_date': pd.date_range(start='2023-01-01', periods=n_clients, freq='7D')
}
df_clients = pd.DataFrame(clients_data)

# 2. Таблица товаров
products_data = {
    'product_id': range(1, 21),
    'product_name': [
        'iPhone 14', 'MacBook Air', 'AirPods Pro', 'iPad Mini', 'Apple Watch',
        'Samsung S23', 'Galaxy Tab', 'Galaxy Buds', 'Xiaomi 13', 'Redmi Note',
        'Sony WH-1000', 'JBL Charge', 'Bose QC45', 'Canon EOS', 'Nikon Z5',
        'DJI Mini', 'GoPro Hero', 'Kindle', 'PS5', 'Nintendo Switch'
    ],
    'category': np.random.choice(['Смартфоны', 'Ноутбуки', 'Аудио', 'Планшеты', 'Игры', 'Фото'], 20),
    'price': np.random.randint(5000, 150000, 20)
}
df_products = pd.DataFrame(products_data)

# 3. Таблица заказов
n_orders = 500
orders_data = {
    'order_id': range(1, n_orders + 1),
    'client_id': np.random.choice(df_clients['client_id'], n_orders),
    'product_id': np.random.choice(df_products['product_id'], n_orders),
    'quantity': np.random.randint(1, 4, n_orders),
    'order_date': pd.date_range(start='2024-01-01', periods=n_orders, freq='6h').strftime('%Y-%m-%d')
}
df_orders = pd.DataFrame(orders_data)


print(f"Клиентов: {len(df_clients)}")
print(f"Товаров: {len(df_products)}")
print(f"Заказов: {len(df_orders)}")




print(df_clients)
print(df_products)
print(df_orders)

'''
Задача 1: Объединение данных и расчет выручки 
Объедини таблицы 
df_orders, df_products и df_clients в один DataFrame. 
Добавь колонку revenue, которая равна произведению price на quantity. 
'''
df_merge = pd.merge(df_orders,df_clients, how = "inner", on = 'client_id')
df_tables = pd.merge(df_merge,df_products, how = 'inner', on = 'product_id')
df_tables['revenue'] = df_tables['quantity'] * df_tables['price']
print(df_tables.columns)
'''
Задача 2: Выручка по категориям 
Посчитай общую выручку по каждой категории товаров. 
Отсортируй результат по убыванию выручки. 
'''
df_total_revenue = df_tables.groupby('category')['revenue'].sum()
print(df_total_revenue.sort_values(ascending = False))
'''
Задача 3: Топ-5 клиентов 
Найди топ-5 клиентов по сумме покупок. 
Выведи таблицу с колонками: имя клиента, город, общая сумма покупок. 
'''
df_best_clients = df_tables.groupby(['client_name','city'])['revenue'].sum().nlargest(5)
print(df_best_clients)
'''
Задача 4: Динамика среднего чека 
Посчитай средний чек и количество заказов по месяцам. 
Выведи таблицу с колонками: месяц, средний чек, количество заказов. 
'''
df_tables['month'] = pd.to_datetime(df_tables['order_date']).dt.to_period('M')
df_count_avg = df_tables.groupby('month').agg(
    average_check = ('revenue','mean'),
    count_orders = ('order_id','count')
)
print(df_count_avg)

'''
Задача 5: Сводная таблица 
Построй сводную таблицу: 
По строкам — города клиентов 
По столбцам — категории товаров 
В ячейках — общая выручка Заполни пропуски нулями'''

df_pivot = pd.pivot_table(df_tables,values = 'revenue',index='city',columns='category',aggfunc='sum',fill_value=0)
print(df_pivot)
