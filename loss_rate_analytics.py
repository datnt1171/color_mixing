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
            html.H1('Loss rate Analytics Dashboard')
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
            html.Title("Loss_rate% by package size"),
            dcc.Graph(figure={}, id='bar_loss_rate_analytic')
        ], width=3),

        dbc.Col([
            html.Title("Actual quantity by package size"),
            dcc.Graph(figure={}, id='donut_quantity_analytic')
        ], width=3)
    ]),

    dbc.Row([
        dbc.Col([
            html.Title("Loss quantity by package size"),
            dcc.Graph(figure={}, id='bar_avg_loss_quantity_analytic')
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Title("Total loss quantity by pakage size"),
            dcc.Graph(figure={}, id='bar_sum_loss_quantity_analytic')
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Title("Data selected from ERP"),
            dash_table.DataTable(id='table_data_analytic', page_size=6),
        ], width=12)
    ])

])

@callback(
    [Output(component_id='bar_loss_rate_analytic', component_property='figure'),
      Output(component_id='donut_quantity_analytic', component_property='figure'),
      Output(component_id='bar_avg_loss_quantity_analytic', component_property='figure'),
      Output(component_id='bar_sum_loss_quantity_analytic', component_property='figure'),
      Output(component_id='table_data_analytic', component_property='data')
      ],
    
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

    # Bar chart - loss rate
    df_loss_rate = dff.groupby('qc').agg({'actual_quantity':'sum',
                                          'loss_quantity':'sum'}
                                          ).reset_index()
    df_loss_rate['loss_rate'] = df_loss_rate['loss_quantity'] / df_loss_rate['actual_quantity'] * 100
    df_loss_rate['loss_rate'] = df_loss_rate['loss_rate'].round(2)
    fig_loss_rate = px.bar(df_loss_rate, x='qc', y='loss_rate', color='qc', text='loss_rate')
    fig_loss_rate.update_traces(textposition='outside', textfont_size=12, textangle=0)
    
    # Donut chart - sum of actual quantity
    fig_quantity = px.pie(dff, values='actual_quantity', names='qc')
    fig_quantity.update_traces(textposition='outside', textinfo='percent+label', hole=.6)
    
    # Histogram - average loss quantity
    fig_avg_loss_quantity = px.histogram(dff, x='qc', y='actual_quantity', histfunc='avg', color='qc')
    fig_avg_loss_quantity.update_traces(textposition='outside', textfont_size=12, textangle=0)
    
    # Histogram - sum loss quantity
    fig_sum_loss_quantity = px.histogram(dff, x='qc', y='actual_quantity', histfunc='sum', color='qc')
    fig_sum_loss_quantity.update_traces(textposition='outside', textfont_size=12, textangle=0)
    
    return fig_loss_rate, fig_quantity, fig_avg_loss_quantity, fig_sum_loss_quantity, table_data
