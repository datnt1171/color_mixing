# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 11:03:46 2024

@author: KT1
"""

import dash
from dash import html, dcc, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

df = pd.read_excel(r'color_mixing.xlsx')


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Color-Mixing Daily Report')
        ], width=12)
    ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            html.Title("Select Date Range"),
            # Add DatePickerRange
            dcc.DatePickerRange(
            id='date-picker-range',
            start_date_placeholder_text='Start date',
            end_date_placeholder_text='End date'
            )
        ], width=8)
    ]),
   

    dbc.Row([
        dbc.Col([
            html.Title("Loss rate"),
            dcc.Graph(figure={}, id='line_loss_rate_date')
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Title("Loss rate"),
            dcc.Graph(figure={}, id='bar_loss_rate_category')
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Title("Data selected from ERP"),
            dash_table.DataTable(id='table_data_date', page_size=6),
        ], width=12)
    ])

])

@callback(
    [Output(component_id='line_loss_rate_date', component_property='figure'),
     Output(component_id='bar_loss_rate_category', component_property='figure'),
     Output(component_id='table_data_date', component_property='data')],
    [Input(component_id='date-picker-range', component_property='start_date'),
     Input(component_id='date-picker-range', component_property='end_date')]
)

def update_content(start_date, end_date):
    # Filter by selected date range
    if start_date and end_date:
        dff = df[(df['start_date'] >= start_date) & (df['start_date'] <= end_date)]
    else:
        dff = df.copy()
    # Update the data for the table
    table_data = dff.to_dict('records')

    # Line chart - loss rate
    df_loss_rate = dff.groupby('start_date').agg({'actual_quantity':'sum',
                                          'loss_quantity':'sum'}
                                          ).reset_index()
    df_loss_rate['loss_rate'] = df_loss_rate['loss_quantity'] / df_loss_rate['actual_quantity'] * 100
    df_loss_rate['loss_rate'] = df_loss_rate['loss_rate'].round(2)
    fig_loss_rate_date = px.line(df_loss_rate, x='start_date', y='loss_rate')
    # Add average line
    average_value = df_loss_rate['loss_quantity'].sum() / df_loss_rate['actual_quantity'].sum() * 100
    fig_loss_rate_date.add_shape(
    type="line",
    x0=df_loss_rate['start_date'].min(),  # Starting x position (min date)
    x1=df_loss_rate['start_date'].max(),  # Ending x position (max date)
    y0=average_value,     # The y-value for the line (average)
    y1=average_value,     # The y-value for the line (average)
    line=dict(color="Red", width=2, dash="dash"),  # Customize the line style
)
    # Bar chart - Loss rate
    df_loss_rate_category = dff.groupby('category').agg({'actual_quantity':'sum',
                                          'loss_quantity':'sum'}
                                          ).reset_index()
    df_loss_rate_category['loss_rate'] = df_loss_rate_category['loss_quantity'] / df_loss_rate_category['actual_quantity'] * 100
    df_loss_rate_category['loss_rate'] = df_loss_rate_category['loss_rate'].round(2)
    fig_loss_rate_category = px.bar(df_loss_rate_category, x='category', y='loss_rate')
    fig_loss_rate_category.update_traces(textposition='outside', textfont_size=12, textangle=0)

    return fig_loss_rate_date, fig_loss_rate_category, table_data