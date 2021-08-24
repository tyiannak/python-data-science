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


# read airbnb data for Athens:
csv_data = pd.read_csv("listings.csv")
nei = csv_data["neighbourhood"].dropna().unique()
nei_list = [{'label': c, 'value': c} for c in nei if c != "nan"]
#for n in nei:
#    print(n, len(csv_data[csv_data["neighbourhood"]==n]))
data = {'lon': np.array(csv_data['longitude']),
        'lat': np.array(csv_data['latitude'])}


def draw_data():
    figure = {'data': [go.Scattermapbox(lat=data['lat'],  lon=data['lon'],
                                        mode='markers',  marker_size=10,
                                        marker_color='rgba(22, 182, 255, .9)'),
                       ],
              'layout': go.Layout(
                  hovermode='closest',
                  mapbox=dict(accesstoken=open("mapbox_token").read(),
                              style='light', bearing=0,
                              center=go.layout.mapbox.Center(
                                  lat=np.mean(data['lat']),
                                  lon=np.mean(data['lon'])),
                              pitch=0, zoom=12))}
    return dcc.Graph(figure=figure, style={'width': '80vh', 'height': '80vh'})


def get_layout():
    """
    Initialize the UI layout
    """
    global data

    layout = dbc.Container([
        # Title
        dbc.Row(dbc.Col(html.H2("Airbnb Data Visualization Example",
                                style={'textAlign': 'center',
                                       "background-color": "red",
                                       'color': colors['text']}))),

        # Main Graph
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure={'data': [go.Scatter(x=[1], y=[1])]}),
                    width=8,
                    style={'textAlign': 'center',
                           "background-color": "red",
                           'color': colors['text']},
                    id="main_graph"),
                dbc.Col(
                    dcc.Graph(figure={'data': [go.Scatter(x=[1], y=[1])]}),
                    width=4,
                    style={'textAlign': 'center',
                           "background-color": "red",
                           'color': colors['text']},
                    id="main_graph_2"),

            ], className="h-75"),

        # Controls
        dbc.Row(
            [
                dbc.Col(
                html.Div([
                    dcc.Dropdown(id='demo-dropdown', options=nei_list,
                                 value=nei[0]),
                    html.Div(id='dd-output-container')
                ]),
                    style={'textAlign': 'center',
                           "background-color": "green",
                           'color': colors['text']},
                ),
                dbc.Col(html.Button('Run', id='btn-next', n_clicks=0)),
            ], className="h-25"),
    ])

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
