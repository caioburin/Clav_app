import dash
import dash_core_components as dcc
import dash_html_components as html

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
from pandas_datareader.data import DataReader
import time

app = dash.Dash('stock-tickers')
server = app.server

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

colorscale = cl.scales['9']['qual']['Paired']

df_symbol = pd.read_csv('artistas.csv')

app.layout = html.Div([
    html.Div([
        html.H2('Clav Music Business Intelligence',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'margin-left': '7px',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       }),
        html.Img(src="https://instagram.fcgh9-1.fna.fbcdn.net/vp/49e0d2504950d8583e5416cfae3b9ea1/5B77FDDD/t51.2885-19/s150x150/26872969_1494428430668046_2492219739179319296_n.jpg",
                style={
                    'height': '100px',
                    'float': 'right'
                },
        ),
    ]),

    dcc.Dropdown(
        id='stock-ticker-input',
        options=[{'label': s[0], 'value': str(s[1])}
                 for s in zip(df_symbol.Company, df_symbol.Symbol)],
        value=['iCasei', 'Clav'],
        multi=True
    ),
    dcc.RadioItems(
                id = 'charts_radio',
                options=[
                    dict( label='Instagram', value='insta' ),
                    dict( label='Youtube', value='youtube' ),
                    dict( label='Facebook', value='face' ),
                ],
                labelStyle = dict(display='inline'),
                value='insta'
    ),
    
    html.Div(id='graphs')
], className="container")



def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value'),
     dash.dependencies.Input('charts_radio', 'value')])

def update_graph(tickers, midia):
    graphs = []
    if midia == 'insta':
        for i, ticker in enumerate(tickers):
            try:
                total = pd.read_excel('/home/caio/Documentos/mbi/insta_artistas_clav.xlsx')
                df = total[total.Artista == '{}'.format(ticker)]
            except:
                graphs.append(html.H3(
                    'Data is not available for {}'.format(ticker),
                    style={'marginTop': 20, 'marginBottom': 20}
                ))
                continue

            candlestick = {
                'x': df['Data'],
                'Seguidores': df['Seguidores'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = df.Seguidores
            bollinger_traces = [{
                'x': df['Data'], 'y': df['Seguidores'],
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 2.5, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
               'showlegend': True if i == 0 else False,
                'name': '{}'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(dcc.Graph(
                id=ticker,
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))
            
    if midia == 'face':
        for i, ticker in enumerate(tickers):
            try:
                total = pd.read_excel('/home/caio/Documentos/mbi/face_artistas_clav.xlsx')
                df = total[total.Artista == '{}'.format(ticker)]
            except:
                graphs.append(html.H3(
                    'Data is not available for {}'.format(ticker),
                    style={'marginTop': 20, 'marginBottom': 20}
                ))
                continue

            candlestick = {
                'x': df['Data'],
                'Likes': df['Likes'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = df.Likes
            bollinger_traces = [{
                'x': df['Data'], 'y': df['Likes'],
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 2.5, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
               'showlegend': True if i == 0 else False,
                'name': '{}'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(dcc.Graph(
                id=ticker,
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))

    if midia == 'youtube':
        for i, ticker in enumerate(tickers):
            try:
                total = pd.read_excel('/home/caio/Documentos/mbi/youtube_artistas_clav.xlsx')
                df = total[total.Artista == '{}'.format(ticker)]
            except:
                graphs.append(html.H3(
                    'Data is not available for {}'.format(ticker),
                    style={'marginTop': 20, 'marginBottom': 20}
                ))
                continue

            candlestick = {
                'x': df['Data'],
                'Visualizações': df['Visualizações'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = df['Visualizações']
            bollinger_traces = [{
                'x': df['Data'], 'y': df['Visualizações'],
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 2.5, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
               'showlegend': True if i == 0 else False,
                'name': '{}'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(dcc.Graph(
                id=ticker,
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))            

    return graphs


external_css = ["https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


if __name__ == '__main__':
    app.run_server(debug=True)
