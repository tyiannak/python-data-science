"""

Instructions:

Maintainer: Theodoros Giannakopoulos {tyiannak@gmail.com}
"""

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
global data
import numpy as np


colors = {'background': '#111111', 'text': '#7FDBDD'}
def_font = dict(family="Courier New, Monospace", size=10, color='#000000')

csv_data = pd.read_csv("listings.csv")
nei = csv_data["neighbourhood"].dropna().unique()
nei_list = [{'label': c, 'value': c} for c in nei if c != "nan"]

for n in nei:
    print(n, len(csv_data[csv_data["neighbourhood"]==n]))

data = {'x': np.array(csv_data['longitude']),
        'y': np.array(csv_data['latitude'])}

def draw_data():
    print(data)
    figure = {'data': [
                        go.Scatter(x=data['x'],
                                   y=data['y'],
                                   mode='markers', name='y = -1',
                                   marker_size=10,
                                   marker_color='rgba(22, 182, 255, .9)'
                                   ),
                   ],
        'layout': go.Layout(
            xaxis=dict(range=[min(data['x']) - np.mean(np.abs(data['x'])),
                              max(data['x']) + np.mean(np.abs(data['x']))
                    ]),
            yaxis=dict(range=[min(data['x']) - np.mean(np.abs(data['x'])),
                              max(data['x']) + np.mean(np.abs(data['x']))
                                              ]))}

    return dcc.Graph(figure=figure)


def get_layout():
    """
    Initialize the UI layout
    """
    global data

    layout = dbc.Container([
        # Title
        dbc.Row(dbc.Col(html.H2("Basic Classification Training Simulations",
                                style={'textAlign': 'center',
                                       'color': colors['text']}))),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure={'data': [go.Scatter(x=[1], y=[1], name='F')]}),
                    id="main_graph"),

            ], className="h-1"),

        dbc.Row(
            [
                html.Div([
                    dcc.Dropdown(
                        id='demo-dropdown',
                        options=nei_list,
                        value=nei[0]
                    ),
                    html.Div(id='dd-output-container')
                ]),
                dbc.Col(html.Button('Perceptron Step', id='btn-next',
                                    n_clicks=0)),
                html.Div(id='container-button-timestamp')
            ], className="h-1"),

    ], style={"height": "100vh"})

    return layout


if __name__ == '__main__':
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = get_layout()


    @app.callback(
        dash.dependencies.Output('dd-output-container', 'children'),
        [dash.dependencies.Input('demo-dropdown', 'value')])
    def update_output(value):
        return 'You have selected "{}"'.format(value)

    @app.callback(dash.dependencies.Output('main_graph', 'children'),
                  dash.dependencies.Input('btn-next', 'n_clicks'))
    def displayClick(btn1):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'btn-next' in changed_id:
            print("AAA")

        return draw_data()

    app.run_server(debug=True)
