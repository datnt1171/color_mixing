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
            html.H1('Color-Mixing Weekly Report')
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
            html.Title("Sum of Actual Quantity (Kg)"),
            dcc.Graph(figure={}, id='bar_actual_quantity_week')
        ], width=3),

        dbc.Col([
            html.Title("Number of batches produced"),
            dcc.Graph(figure={}, id='bar_production_batch_week')
        ], width=3)
    ]),

    dbc.Row([
        dbc.Col([
            html.Title("Loss rate"),
            dcc.Graph(figure={}, id='bar_loss_rate_week')
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Title("Data selected from ERP"),
            dash_table.DataTable(id='table_data_week', page_size=6),
        ], width=12)
    ])

])

@callback(
    [Output(component_id='bar_actual_quantity_week', component_property='figure'),
     Output(component_id='bar_production_batch_week', component_property='figure'),
     Output(component_id='bar_loss_rate_week', component_property='figure'),
     Output(component_id='table_data_week', component_property='data')],
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

    # Create bar chart for actual quantity
    fig_actual = px.histogram(dff, x='paint_type', y='actual_quantity', histfunc='sum', 
                              color='paint_type',text_auto=True)
    fig_actual.update_traces(textposition='outside', textfont_size=12, textangle=0)
    
    fig_num_batch = px.histogram(dff, x='paint_type', y='paint_type', histfunc='count', 
                                 color='paint_type',text_auto=True)
    fig_num_batch.update_traces(textposition='outside', textfont_size=12, textangle=0)
    
    dff_loss = dff.groupby('paint_type').agg({'actual_quantity':'sum',
                                              'loss_quantity':'sum'}
                                             ).reset_index()
    dff_loss['loss_rate'] = dff_loss['loss_quantity'] / dff_loss['actual_quantity'] * 100
    dff_loss['loss_rate'] = dff_loss['loss_rate'].round(2)
    fig_loss_rate = px.bar(dff_loss, x='paint_type',y='loss_rate', color='paint_type', text='loss_rate')
    fig_loss_rate.update_traces(textposition='outside', textfont_size=12, textangle=0)
    return fig_actual, fig_num_batch, fig_loss_rate, table_data