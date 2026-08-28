from data import *
from engine import *
from graph import *
from datetime import datetime as dt

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import numpy as np
import os

from dotenv import load_dotenv

load_dotenv()

from_date = ''
to_date = '2026-09-04'

if from_date == '':
    from_date = dt.today().strftime('%Y-%m-%d')
elif dt.strptime(from_date, '%Y-%m-%d') < dt.today():
    from_date = dt.today().strftime('%Y-%m-%d')
if to_date == '':
    to_date = dt.today().strftime('%Y-%m-%d')

qqq_ticker = 'QQQ'
spy_ticker = 'SPY'

strikes = 30

AssetData.auth_client(
        api_key = os.getenv("SCHWAB_API_KEY"),
        app_secret = os.getenv("SCHWAB_API_SECRET"),
        callback_url = os.getenv("SCHWAB_CALLBACK_URI")
        )

qqq_data = AssetData(qqq_ticker)
spy_data = AssetData(spy_ticker)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='main', style={'height': '90vh', 'width': '100%'}),
    dcc.Interval(
        id='interval-component',
        interval=3*1000,  # refresh every 60 seconds; adjust as needed
        n_intervals=0
    )
])

@app.callback(
    Output('main', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):

    dashboard = Dashboard(2, 2)

    qqq_call_quotes = qqq_data.fetch_data(
            start_date = from_date,
            end_date = to_date,
            strike_count = strikes,
            side = 'c'
    )
    qqq_put_quotes = qqq_data.fetch_data(
            start_date = from_date,
            end_date = to_date,
            strike_count = strikes,
            side = 'p'
    )

    qqq_spot_price = qqq_call_quotes['underlyingPrice']

    qqq_call_volume = get_data_pair(qqq_call_quotes, 'totalVolume', 'c', from_date, to_date)

    qqq_put_volume = get_data_pair(qqq_put_quotes, 'totalVolume', 'p', from_date, to_date) 

    qqq_call_open_interest = get_data_pair(qqq_call_quotes, 'openInterest', 'c', from_date, to_date, per_expiration=False)
    qqq_call_open_interest_calc = get_data_pair(qqq_call_quotes, 'openInterest', 'c', from_date, to_date, per_expiration=True)
    qqq_call_gamma = get_data_pair(qqq_call_quotes, 'gamma', 'c', from_date, to_date, per_expiration=True)
    qqq_call_delta = get_data_pair(qqq_call_quotes, 'delta', 'c', from_date, to_date, per_expiration=True)

    qqq_put_open_interest = get_data_pair(qqq_put_quotes, 'openInterest', 'p', from_date, to_date, per_expiration=False)
    qqq_put_open_interest_calc = get_data_pair(qqq_put_quotes, 'openInterest', 'p', from_date, to_date, per_expiration=True)
    qqq_put_gamma = get_data_pair(qqq_put_quotes, 'gamma', 'p', from_date, to_date, per_expiration=True)
    qqq_put_delta = get_data_pair(qqq_put_quotes, 'delta', 'p', from_date, to_date, per_expiration=True)

    qqq_net_gex = get_gamma_exposure(qqq_call_gamma, qqq_put_gamma, qqq_call_open_interest_calc, qqq_put_open_interest_calc, qqq_spot_price)
    qqq_net_dex = get_delta_exposure(qqq_call_delta, qqq_put_delta, qqq_call_open_interest_calc, qqq_put_open_interest_calc)

    dashboard.add_chart(
                y = list(qqq_net_gex.keys()),
                x = list(qqq_net_gex.values()),
                chart_type = 'bar',
                y_label = 'Strikes ($)',
                x_label = 'GEX ($M)',
                title = f'{qqq_ticker} Gamma Exposure by Strike',
                row = 1,
                col = 1,
                legend_label = 'Net',
                orientation = 'h',
                line = qqq_spot_price
    )

    dashboard.add_chart(
                y = list(qqq_net_dex.keys()),
                x = list(qqq_net_dex.values()),
                chart_type = 'bar',
                y_label = 'Strikes ($)',
                x_label = 'DEX ($M)',
                title = f'{qqq_ticker} Delta Exposure by Strike',
                row = 1,
                col = 2,
                legend_label = 'Net',
                orientation = 'h',
                line = qqq_spot_price
    )

    spy_call_quotes = spy_data.fetch_data(
            start_date = from_date,
            end_date = to_date,
            strike_count = strikes,
            side = 'c'
    )
    spy_put_quotes = spy_data.fetch_data(
            start_date = from_date,
            end_date = to_date,
            strike_count = strikes,
            side = 'p'
    )

    spy_spot_price = spy_call_quotes['underlyingPrice']

    spy_call_volume = get_data_pair(spy_call_quotes, 'totalVolume', 'c', from_date, to_date)

    spy_put_volume = get_data_pair(spy_put_quotes, 'totalVolume', 'p', from_date, to_date) 

    spy_call_open_interest = get_data_pair(spy_call_quotes, 'openInterest', 'c', from_date, to_date, per_expiration=False)
    spy_call_open_interest_calc = get_data_pair(spy_call_quotes, 'openInterest', 'c', from_date, to_date, per_expiration=True)
    spy_call_gamma = get_data_pair(spy_call_quotes, 'gamma', 'c', from_date, to_date, per_expiration=True)
    spy_call_delta = get_data_pair(spy_call_quotes, 'delta', 'c', from_date, to_date, per_expiration=True)

    spy_put_open_interest = get_data_pair(spy_put_quotes, 'openInterest', 'p', from_date, to_date, per_expiration=False)
    spy_put_open_interest_calc = get_data_pair(spy_put_quotes, 'openInterest', 'p', from_date, to_date, per_expiration=True)
    spy_put_gamma = get_data_pair(spy_put_quotes, 'gamma', 'p', from_date, to_date, per_expiration=True)
    spy_put_delta = get_data_pair(spy_put_quotes, 'delta', 'p', from_date, to_date, per_expiration=True)

    spy_net_gex = get_gamma_exposure(spy_call_gamma, spy_put_gamma, spy_call_open_interest_calc, spy_put_open_interest_calc, spy_spot_price)
    spy_net_dex = get_delta_exposure(spy_call_delta, spy_put_delta, spy_call_open_interest_calc, spy_put_open_interest_calc)

    dashboard.add_chart(
                y = list(spy_net_gex.keys()),
                x = list(spy_net_gex.values()),
                chart_type = 'bar',
                y_label = 'Strikes ($)',
                x_label = 'GEX ($M)',
                title = f'{spy_ticker} Gamma Exposure by Strike',
                row = 2,
                col = 1,
                legend_label = 'Net',
                orientation = 'h',
                line = spy_spot_price
    )

    dashboard.add_chart(
                y = list(spy_net_dex.keys()),
                x = list(spy_net_dex.values()),
                chart_type = 'bar',
                y_label = 'Strikes ($)',
                x_label = 'DEX ($M)',
                title = f'{spy_ticker} Delta Exposure by Strike',
                row = 2,
                col = 2,
                legend_label = 'Net',
                orientation = 'h',
                line = spy_spot_price
    )

    dashboard.fig.update_layout(
        plot_bgcolor='#1e1e1e',   # background behind the bars
        paper_bgcolor='#121212',  # background of the whole figure, including margins
        font_color='#f0f0f0'      # text color, needed for readability on a dark background
    )

    return dashboard.fig

if __name__ == '__main__':
    app.run(debug=True)
