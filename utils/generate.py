import os
import duckdb
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from faker import Faker


Faker.seed(42)
np.random.seed(42)


def generate_user(fake, i):
    f_name = fake.first_name()
    l_name = fake.last_name()
    email = (
        f_name.lower()
        + "."
        + l_name.lower()
        + fake.year()[2:]
        + "@"
        + fake.free_email_domain()
    )
    percent_of_empty_values = 0.05
    country_code = random.choices(
        ['US', 'CA', 'DE', 'FR', 'GB', 'IT', 'ES', fake.country_code()],
        [0.40, 0.20, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01]
    )[0]
    return {
        "id": i + 1,
        "first_name": f_name,
        "last_name": l_name if np.random.rand() < 1 - percent_of_empty_values else np.nan,
        "email": email,
        "created_at": fake.date_time_between(start_date='-5y'),
        "country_code": country_code,
    }


def generate_products():
    items = [
        ('Smartphones', 'iPhone', 799),
        ('Smartphones', 'Samsung Galaxy', 899),
        ('Smartphones', 'Google Pixel', 699),
        ('Laptops', 'MacBook Air', 1299),
        ('Laptops', 'MacBook Pro', 1999),
        ('Laptops', 'Dell XPS', 999),
        ('Laptops', 'Lenovo ThinkPad', 1399),
        ('Laptops', 'HP Spectre', 1199),
        ('Laptops', 'HP Envy', 899)
    ]
    return [{
        "id": i + 1,
        "name": item_name,
        "category": category,
        "price_usd": item_price * 1.0,
    } for i, (category, item_name, item_price) in enumerate(items)]


def generate_order_item(fake, order_id, product):
    return {
        "order_id": order_id,
        "product_id": product["id"],
        "quantity": 1,
        "price_usd": product["price_usd"],
    }


def generate_order(fake, i, total_users):
    order_id = i + 1
    product = np.random.choice(generate_products())
    items = [generate_order_item(fake, order_id, product) for _ in range(np.random.choice(np.arange(1, 2)))]
    order = {
        "id": i + 1,
        "purchased_at": fake.date_time_between(start_date='-3y'),
        "user_id": np.random.choice(np.arange(1, total_users + 1)),
        "total_price": sum([item["price_usd"] for item in items]),
    }

    return order, items




if __name__ == '__main__':
    NUM_RECORDS = 10000
    
    fake = Faker()

    print('Generating users...')
    users = [generate_user(fake, i) for i in tqdm(range(NUM_RECORDS))]
    df_users = pd.DataFrame(users)

    print('Generating products...')
    products = generate_products()
    df_products = pd.DataFrame(products)

    print('Generating orders...')
    orders = []
    order_items = []
    for i in tqdm(range(int(NUM_RECORDS * 0.35))):
        order, items = generate_order(fake, i, NUM_RECORDS)
        orders.append(order)
        order_items += items
    
    df_orders = pd.DataFrame(orders)
    df_order_items = pd.DataFrame(order_items)


    print('Saving data to DuckDB...')
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    parent_folder = os.path.dirname(current_folder)
    dbt_folder = os.path.join(parent_folder, 'dbtips')
    duckdb_file_path = os.path.join(dbt_folder, 'duck.db')

    con = duckdb.connect(duckdb_file_path)
    tables = ['df_users', 'df_products', 'df_orders', 'df_order_items']
    
    for table in tables:
        con.execute(f'''
            CREATE OR REPLACE TABLE {table[3:]} AS SELECT * FROM {table};
        ''')
    con.close()
