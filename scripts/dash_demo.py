"""
Instructions:
- Simply run python3 dash_demo.py
- You need to generate a maxbox token and save it in a file called .mapbox_token
(https://docs.mapbox.com/help/getting-started/access-tokens/)

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
temp_style = {'textAlign': 'center',
                           "background-color": "green",
                           'color': colors['text']}


# read airbnb data for Athens:
csv_data = pd.read_csv("listings.csv")
nei = csv_data["neighbourhood"].dropna().unique()
nei_list = [{'label': c, 'value': c} for c in nei if c != "nan"]
#for n in nei:
#    print(n, len(csv_data[csv_data["neighbourhood"]==n]))

global min_price
global max_price
global min_rating
global max_rating

min_price = 0
max_price = 500
min_rating = 0
max_rating = 5


data = {'lon': np.array(csv_data['longitude']),
        'lat': np.array(csv_data['latitude']),
        'price': np.array([float(i[1:].replace(',', ''))
                           for i in csv_data['price']])}


data['price'][data['price']>500] = 0


def draw_data():
    # filtering:
    global min_price
    global max_price

    data_new = {'lon': [], 'lat': [], 'price': []}
    for i in range(len(data['lon'])):
        if data['price'][i] >= min_price and data['price'][i] <= max_price:
            data_new['lon'].append(data['lon'][i])
            data_new['lat'].append(data['lat'][i])
            data_new['price'].append(data['price'][i])

    print(min_price, max_price, len(data_new['lon']))

    figure = {'data': [go.Scattermapbox(lat=data_new['lat'],
                                        lon=data_new['lon'],
                                        mode='markers',  marker_size=4,
                                        marker_color='rgba(22, 182, 255, .9)'),
                       ],
              'layout': go.Layout(
                  hovermode='closest',
                  mapbox=dict(accesstoken=open("mapbox_token").read(),
                              style='light', bearing=0,
                              center=go.layout.mapbox.Center(
                                  lat=np.mean(data_new['lat']),
                                  lon=np.mean(data_new['lon'])),
                              pitch=0, zoom=12))}

    h, h_bins = np.histogram(data_new['price'], bins=30)
    h_bins = (h_bins[0:-1] + h_bins[1:]) / 2
    figure_2 = {'data': [go.Scatter(x=h_bins, y=h,
                                    marker_color='rgba(22, 182, 255, .9)'),],
                'layout': go.Layout(hovermode='closest',)}

    return dcc.Graph(figure=figure), dcc.Graph(figure=figure_2)


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
                        dcc.Slider(id='slider_price_min',
                                   min=0, max=500, step=1, value=0),
                        dcc.Slider(id='slider_price_max',
                                   min=0, max=500, step=1, value=500),
                        html.Div(id='slider_price_container')]),
                    style=temp_style,
                    width=2,
                ),

                dbc.Col(
                    html.Div([
                        dcc.Slider(id='slider_rating_min',
                                   min=0, max=5, step=1, value=0),
                        dcc.Slider(id='slider_rating_max',
                                   min=0, max=5, step=1, value=5),
                        html.Div(id='slider_rating_container')]),
                    style=temp_style,
                    width=2,
                ),

                    dbc.Col(html.Button('Run', id='btn-next'), width=2),
            ], className="h-25"),
    ])

    return layout


if __name__ == '__main__':
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = get_layout()

    @app.callback(
        [dash.dependencies.Output('slider_price_container', 'children'),
         dash.dependencies.Output('slider_rating_container', 'children'),
         dash.dependencies.Output('main_graph', 'children'),
         dash.dependencies.Output('main_graph_2', 'children')],
        [dash.dependencies.Input('slider_price_min', 'value'),
         dash.dependencies.Input('slider_price_max', 'value'),
         dash.dependencies.Input('slider_rating_min', 'value'),
         dash.dependencies.Input('slider_rating_max', 'value'),
         dash.dependencies.Input('btn-next', 'n_clicks')])
    def update_output(val1, val2, val3, val4, val5):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'slider_price_min' in changed_id:
            global min_price
            min_price = int(val1)
        elif 'slider_price_max' in changed_id:
            global max_price
            max_price = int(val2)
        if 'slider_rating_min' in changed_id:
            global min_rating
            min_rating = int(val3)
        elif 'slider_rating_max' in changed_id:
            global max_rating
            max_rating = int(val4)
        elif 'btn-next' in changed_id:
            print("TODO")
        g1, g2 = draw_data()
        return f'Price {min_price} - {max_price} Euros', \
               f'Rating {min_rating} - {max_rating} Stars', \
               g1, g2


    app.run_server(debug=True)
