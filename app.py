import datetime
from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
# These imports only needed due to temp. code in get_value function
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

points = 0
points2 = 0


def test():
    global points
    global points2
    points += 1
    points2 += 1


def get_value(n_intervals):
    date_today = datetime.now()
    days = pd.date_range(date_today, date_today + timedelta(points), freq='D')
    np.random.seed(seed=111 * n_intervals)
    data = np.random.randint(1, high=100, size=len(days))
    data2 = np.random.randint(100000, high=2000000, size=len(days))
    data3 = np.random.randint(10, high=93000, size=len(days))
    df = pd.DataFrame(data={'Hora': days, 'x': data, 'y': data2, 'z': data3})
    print(df)
    return df


def get_value2(n_intervals2):
    date_today = datetime.now()
    days = pd.date_range(date_today, date_today + timedelta(points2), freq='D')
    np.random.seed(seed=200 * n_intervals2)
    data = np.random.randint(1, high=100, size=len(days))
    data2 = np.random.randint(60000, high=90000, size=len(days))
    data3 = np.random.randint(60000, high=90000, size=len(days))
    df2 = pd.DataFrame(data={'Hora': days, 'x': data, 'y': data2, 'z': data3})
    print("df2")
    print(df2)
    return df2


def serve_layout():
    return \
        html.Div(children=[
            html.H3(children='Monitoramento dos Eventos do Banco de Dados: ' + str(datetime.now())),
            html.Div(dcc.Graph(id='example-graph', animate=True, responsive=True), ),
            html.Div(dcc.Graph(id='example-graph1', animate=True, responsive=True), ),
            dcc.Interval(
                id='interval-component',
                interval=5 * 1000,
                n_intervals=0, )],
            style={'width': '100%', 'display': 'inline-block', 'background-color': 'White', 'color': 'black'})


app.layout = serve_layout


@app.callback(
    Output('example-graph', 'figure'),
    [Input('interval-component', 'n_intervals')])
def update_graph1(n_intervals):
    df = get_value(n_intervals)
    test()
    return \
        {
            'data': [
                {'x': df.Hora, 'y': df.y, 'type': 'line', 'name': 'second'},
                {'x': df.Hora, 'y': df.z, 'type': 'line', 'name': 'thirdline'},
                {'x': df.Hora, 'y': df.x, 'type': 'line', 'name': 'first'},
            ],
            'layout': go.Layout(
                # height=700,
                xaxis=dict(zeroline=True, range=[min(df.Hora), max(df.Hora)]),
                yaxis=dict(side='right', range=[
                    df.loc[:, ['x', 'y', 'z']].values.min(),
                    df.loc[:, ['x', 'y', 'z']].values.max()]),
                margin=dict(l=75, r=75, b=75, t=75, pad=10),
                paper_bgcolor="white",

                title="Eventos de Login",
            )
        }


@app.callback(
    Output('example-graph1', 'figure'),
    [Input('interval-component', 'n_intervals')])
def update_graph2(n_intervals2):
    df2 = get_value2(n_intervals2)
    print(df2)
    test()
    return \
        {
            'data': [
                {'x': df.Hora, 'y': df.y, 'type': 'line', 'name': 'second'},
                {'x': df.Hora, 'y': df.z, 'type': 'line', 'name': 'thirdline'},
                {'x': df.Hora, 'y': df.x, 'type': 'line', 'name': 'first'},
            ],
            'layout': go.Layout(
                xaxis=dict(zeroline=True, range=[min(df2.Hora), max(df2.Hora)]),
                yaxis=dict(zeroline=True, side='right', range=[
                    df2.loc[:, ['x', 'y', 'z']].values.min(),
                    df2.loc[:, ['x', 'y', 'z']].values.max()]),
                title="Status de Processamento"
            )
        }


if __name__ == '__main__':
    app.run_server(debug=True)
