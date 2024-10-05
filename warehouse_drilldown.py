# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:06:45 2024

@author: KT1
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

import psycopg2



# Get data

dash.register_page(__name__, path="/warehouse_drilldown")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Color-Mixing Weekly Report')
        ], width=12)
    ], justify="center"),
    
    
    dbc.Row([
        dbc.Col([
            html.Title("Select Day Range"),
            # Add DatePickerRange
            dcc.RangeSlider(1, 31, 1, value=[1, 7], id='day_slicer'),
        ], width=8),
        dbc.Col([
            html.Title("Select Time Level"),
            dbc.RadioItems(
            id="radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Year", "value": "year"},
                {"label": "Month", "value": "month"},
                {"label": "Week of Year", "value": "week_of_year"},
                {"label": "Date", "value": "date"},
            ],
            value="month",
        )
            ])
        
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Title("Loss rate"),
            dcc.Graph(figure={}, id='line_sales')
        ], width=12)
    ]),

])

@callback(
    [Output('line_sales', 'figure')],
    [Input('day_slicer', 'value'),
     Input('radios','value')]
)

def update_line(day_slicer_value, radios_value):
    
    conn = psycopg2.connect(database="dashboard", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
    cur = conn.cursor()
    cur.execute("""SELECT dim_sales.date, factory_code, total_quantity, day, year, month, week_of_year, day_name
            FROM dim_sales JOIN dim_date
            ON dim_sales.date = dim_date.date
            """)


    sales_data = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    df_sales = pd.DataFrame(data = sales_data, columns = column_names)
    
    df_sales['date'] = pd.to_datetime(df_sales['date'])
    df_sales = df_sales[df_sales['date']>='2024-01-01']
    
    df_sales = df_sales[(df_sales['day']>=day_slicer_value[0]) & (df_sales['day']<=day_slicer_value[1])]
    df_sales_month = df_sales.groupby(radios_value).agg({'total_quantity':'sum'}).reset_index()
    fig = px.line(df_sales_month, x=radios_value,y='total_quantity', text='total_quantity')
    return [fig]


