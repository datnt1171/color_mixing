# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 11:30:49 2024

@author: KT1
"""

import pandas as pd
import psycopg2

conn = psycopg2.connect(database="dashboard", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()

cur.execute("""DROP TABLE dim_order""")
cur.execute("""DROP TABLE dim_sales""")
conn.commit()

cur.execute("""CREATE TABLE dim_order(
            order_date date,
            order_code text,
            ct_date date,
            factory_code text,
            factory_name text,
            currency text,
            exchange_rate float,
            tax_type text,
            department text,
            salesman text,
            dk_price text,
            note text,
            prepay_rate text,
            payment_registration_code text,
            payment_registration_name text,
            address text,
            total_quantity float,
            total_package float,
            numerical_order int,
            product_code text,
            product_name text,
            qc text,
            warehouse_type text,
            order_quantity float,
            delivered_quantity float,
            order_package float,
            delivered_package float,
            unit text,
            price_quantity float,
            estimated_delivery_date date,
            actual_delivery_date date,
            unit_price text,
            ct_temp text,
            note_2 text,
            finish_code text)""")



cur.execute("""CREATE TABLE dim_sales(
            factory_code text,
            factory_name text,
            department text,
            salesman text,
            product_code text,
            product_name text,
            qc text,
            date date,
            finish_code text,
            delivery_code text,
            order_code text,
            warehouse_type text,
            lot_code text,
            invoice_code text,
            factory_order_code text,
            total_quantity float,
            total_package float,
            unit text,
            unit_package text,
            price_quantity float,
            unit_price text,
            currency text,
            exchange_rate float,
            tax_type int,
            transfer_rate float,
            revenue_tw float,
            revenue_vn float)""")


def insert_data(df_data, table_name):
    """
    Inserts data from a DataFrame into a specified PostgreSQL table.

    Parameters:
    df_data (pd.DataFrame): DataFrame containing the data to insert.
    conn (psycopg2 connection): Active connection to the PostgreSQL database.
    table_name (str): The name of the table to insert data into.
    """
    try:
        # Get the column names from the DataFrame
        columns = list(df_data.columns)

        # Create the SQL insert query dynamically based on column names
        insert_query = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(columns))});
        """

        # Convert the DataFrame to a list of tuples (for batch insert)
        data = [tuple(row[1:]) for row in df_data.itertuples()]

        # Execute the batch insert
        cur.executemany(insert_query, data)
        conn.commit()

        print("Data inserted successfully!")
    except Exception as e:
        conn.rollback()  # Rollback in case of any error
        print(f"An error occurred: {e}")

df_order = pd.read_csv(r'D:\VL1251\python\dashboard\df_order_prune.csv')
insert_data(df_order, "dim_order")

df_delivery = pd.read_csv(r'D:\VL1251\python\dashboard\df_sales_prune.csv')
insert_data(df_delivery, "dim_sales")


#CREATE dim_date
start_date = '2000-01-01'
end_date = '2050-12-31'
date_range = pd.date_range(start=start_date, end=end_date)


dim_date = pd.DataFrame({
    'date': date_range,
    'year': date_range.year,
    'month': date_range.month,
    'month_name': date_range.strftime('%B'),
    'day': date_range.day,
    'day_of_week': date_range.dayofweek,
    'day_name': date_range.strftime('%A'),
    'week_of_year': date_range.isocalendar().week,
    'quarter': date_range.quarter,
    'is_weekend': date_range.dayofweek >= 5,  # 5 and 6 are Saturday and Sunday
})

dim_date['week_of_year'] = dim_date['week_of_year'].astype(int) # Convert Uint to int
cur.execute("""CREATE TABLE dim_date(
            date date primary key,
            year int,
            month int,
            month_name text,
            day int,
            day_of_week int,
            day_name text,
            week_of_year int,
            quarter int,
            is_weekend boolean)""")


insert_data(dim_date, "dim_date")


conn.close()
