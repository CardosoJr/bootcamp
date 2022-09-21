import time
import importlib

import dash
from dash import dcc
from dash import html
import numpy as np
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from yahooquery import Ticker
import pandas as pd
from datetime import datetime, date
from plotly.subplots import make_subplots

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Primeiro Dashboard"
server = app.server


STOCK_OPTIONS = ['TSLA', 'AAPL', 'MSFT', 'AMZN', 'GOOG']
COLORS  = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']

# Fix sidebar to the left side
SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0,
    "width": "16rem", "padding": "2rem 1rem", "background-color": "#f8f9fa",
}

# Place main content on the right
CONTENT_STYLE = {
    "margin-left": "18rem", "margin-right": "2rem",
    "padding": "2rem 1rem", "display": "inline-block"}

sidebar = html.Div(
    [
        html.H3('Select Stocks for Comparison.'),
        html.Hr(),
        html.Div( 
            className ='div-user-controls',
            children= [
                html.Div( 
                    className='div-for-stock-dropdown',
                    children=[ 
                        dcc.Dropdown(
                            id='selector_id',
                            options= {x:x for x in STOCK_OPTIONS},
                            multi=True, value=['TSLA'],
                            className='postselector'
                        ),
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            min_date_allowed=datetime(2020, 1, 1),
                            max_date_allowed=datetime(2022, 1, 1),
                            initial_visible_month=datetime(2021, 1, 1),
                            start_date=datetime(2021, 1, 1),
                            end_date=datetime(2021, 6, 1),
                            style={"margin-top": "50px"}
                        ),
                    ],
                ),
            ]
        )
    ],
    style=SIDEBAR_STYLE # Include style to fix position
)

content = html.Div(
    id="page-content", 
    children=[
        html.Div(
            className='div-for-text',
            children=[
                html.H2('NASDAQ Stock Prices'), 
                html.P('''Um dashboard de exemplo para acompanhar preços de ações''')
            ]
        ),
        html.Div(
            className='div-for-charts',
            children = [dcc.Graph( id='chart_id', config={'displayModeBar': False})]
        )
    ],
    style=CONTENT_STYLE # Include style to fix position
)


@app.callback( Output('chart_id', 'figure'),
    [
        Input('selector_id', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ])
def update_chart(selector_values, start_date, end_date):
    data = []
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    for ticker in selector_values:
        df = Ticker(ticker).history(start = start_date.strftime("%Y-%m-%d"), end = end_date.strftime("%Y-%m-%d"), interval = '1d').reset_index()
        data.append(df.rename(columns = {'adjclose' : ticker})[['date', ticker]])

    df = data[0]

    for i in range(1, len(data)):
        df = pd.merge(left = df, right = data[i], on = 'date')

    fig = go.Figure()
    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.065, shared_xaxes=True, subplot_titles = ['Price', 'Volatility', 'Returns'])

    for i, ticker in enumerate(selector_values):
        fig.add_trace(
            go.Scatter( x=df['date'], y=df[ticker], name=ticker, line = dict(color = COLORS[i]), legendgroup='group1'), 1, 1)

        fig.add_trace(
            go.Scatter( x=df['date'], y=df[ticker].rolling(14).std(), name=ticker,  legendgroup='group1', line = dict(color = COLORS[i]), showlegend=False), 2, 1)

        fig.add_trace(
            go.Scatter( x=df['date'], y=(1 + df[ticker].pct_change()).cumprod() - 1, name=ticker,  legendgroup='group1', line = dict(color = COLORS[i]), showlegend=False), 3, 1)
    
    fig.update_layout(
        template='seaborn', margin={'b': 15}, hovermode='x', autosize=True, width=1200, height = 750,
        title={'text': 'Car Company Adjusted Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
        xaxis1={
            'range': [df['date'].min(), df['date'].max()],
            'rangeslider_visible': False,
            'rangeselector': dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )},
        xaxis2_rangeslider_visible=False,
        xaxis3_rangeslider_visible=True,
        xaxis3_type="date",
        xaxis3_rangeslider_thickness =  0.04,
    )
    return fig


# Define the app
app.layout = html.Div([sidebar, content])


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
