import dash
from dash import html, dcc, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


import psycopg2


conn = psycopg2.connect(database="dashboard", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()
dash.register_page(__name__, path="/warehouse_weekly")
# Get data
cur.execute("""SELECT order_date, factory_code, order_quantity
            FROM dim_order
            WHERE order_date >='2024-01-01'""")

order_data = cur.fetchall()
column_names = [description[0] for description in cur.description]
df_order = pd.DataFrame(data = order_data, columns = column_names)

df_order['order_date'] = pd.to_datetime(df_order['order_date'])
df_order = df_order[~df_order['factory_code'].isin(['PM','QA','RD','SKS','TV'])]

cur.execute("""SELECT date, factory_code, total_quantity
            FROM dim_sales
            WHERE date between '2024-01-01' AND '2024-06-30'""")

sales_data = cur.fetchall()
column_names = [description[0] for description in cur.description]
df_sales = pd.DataFrame(data = sales_data, columns = column_names)


# Preprocessing
## Sales
df_sales['date'] = pd.to_datetime(df_sales['date'])
df_order['month'] = df_order['order_date'].dt.month
df_sales = df_sales[~df_sales['factory_code'].isin(['PM','QA','RD','SKS','TV'])]

df_order_remain = df_order[df_order['factory_code']!='30673']
df_order_timber = df_order[df_order['factory_code']=='30673']

df_order_remain_grouped = df_order_remain.groupby('month').agg({'order_quantity':'sum'}).reset_index()
df_order_timber_grouped = df_order_timber.groupby('month').agg({'order_quantity':'sum'}).reset_index()

## Order
df_order['order_date'] = pd.to_datetime(df_order['order_date'])
df_sales['month'] = df_sales['date'].dt.month
df_order = df_order[~df_order['factory_code'].isin(['PM','QA','RD','SKS','TV'])]

df_sales_remain = df_sales[df_sales['factory_code']!='30673']
df_sales_timber = df_sales[df_sales['factory_code']=='30673']

df_sales_remain_grouped = df_sales_remain.groupby('month').agg({'total_quantity':'sum'}).reset_index()
df_sales_timber_grouped = df_sales_timber.groupby('month').agg({'total_quantity':'sum'}).reset_index()


# Merge for plotting
df = df_sales_remain_grouped.merge(df_sales_timber_grouped, on='month')
df = df.merge(df_order_remain_grouped, on='month')
df = df.merge(df_order_timber_grouped, on='month')
df.columns = ['month','sales_quantity','sales_quantity_timber','order_quantity','order_quantity_timber']

df_sales = df[['month','sales_quantity','sales_quantity_timber']]
df_order = df[['month','order_quantity','order_quantity_timber']]

df_sales.set_index('month', inplace=True)
df_order.set_index('month', inplace=True)


df = pd.concat(
    [df_sales, df_order],
    axis=1,
    keys=["Sales", "Order"]
)

fig = go.Figure(
    layout=go.Layout(
        height=720,
        width=1280,
        barmode="relative",
        yaxis_showticklabels=False,
        yaxis_showgrid=False,
        yaxis_range=[0, df.groupby(axis=1, level=0).sum().max().max() * 1.5],
       # Secondary y-axis overlayed on the primary one and not visible
        yaxis2=go.layout.YAxis(
            visible=True,
            matches="y",
            overlaying="y",
            anchor="x",
        ),
        font=dict(size=24),
        legend_x=0,
        legend_y=1,
        legend_orientation="h",
        hovermode="x",
        margin=dict(b=0,t=10,l=0,r=10)
    )
)

# Define some colors for the product, revenue pairs
colors = {
    "Sales": {
        "sales_quantity": "#F28F1D",
        "sales_quantity_timber": "#F6C619",
    },
    "Order": {
        "order_quantity": "#2B6045",
        "order_quantity_timber": "#5EB88A",
    }
}

# Add the traces
for i, t in enumerate(colors):
    for j, col in enumerate(df[t].columns):
        if (df[t][col] == 0).all():
            continue
        fig.add_bar(
            x=df.index,
            y=df[t][col],
            # Set the right yaxis depending on the selected product (from enumerate)
            yaxis=f"y{i + 1}",
            # Offset the bar trace, offset needs to match the width
            # For categorical traces, each category is spaced by 1
            offsetgroup=str(i),
            offset=(i - 1) * 1/3,
            width=1/3,
            legendgroup=t,
            legendgrouptitle_text=t,
            name=col,
            marker_color=colors[t][col],
            marker_line=dict(width=2, color="#333"),
            hovertemplate="%{y}<extra></extra>"
        )





layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Warehouse Weekly Dashboard')
        ], width=12)
    ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            html.Title("Total loss quantity by pakage size"),
            dcc.Graph(figure=fig, id='bar_sum_loss_quantity_analytic')
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Title("Total loss quantity by pakage size"),
            dcc.Graph(figure=fig, id='bar_sum_loss_quantity_analytic')
        ], width=12)
    ]),
   
])

