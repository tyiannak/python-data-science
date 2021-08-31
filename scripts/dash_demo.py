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
import dash_table
import numpy as np


colors = {'background': '#111111', 'text': '#7FDBDD'}
def_font = dict(family="Courier New, Monospace", size=10, color='#000000')
temp_style = {'textAlign': 'center', "background-color": "green",
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
global csv_data_temp

min_price = 0
max_price = 1000
min_rating = 3
max_rating = 5

print(len(csv_data))
csv_data = csv_data[csv_data.review_scores_rating.notnull()]
print(len(csv_data))
csv_data.price = csv_data.price.str.replace('$', '', regex=True)
csv_data.price = csv_data.price.str.replace(',', '', regex=True)
csv_data.price = csv_data.price.astype("float")
csv_data = csv_data[csv_data["price"] <= 1000]
print(len(csv_data))


def get_statistics(d):
    data_t = pd.DataFrame(d.groupby('neighbourhood_cleansed').
                          agg({'price': 'median',
                               'review_scores_rating': 'median',
                               'id': 'count'})).reset_index().to_dict('records')
    print(data_t)
    return data_t


def draw_data():
    # filtering:
    global min_price
    global max_price
    global min_rating
    global max_rating
    global csv_data_temp
    csv_data_temp = csv_data[(csv_data['price'] <= max_price) &
                             (csv_data['price'] >= min_price) &
                             (csv_data['review_scores_rating'] <= max_rating) &
                             (csv_data['review_scores_rating'] >= min_rating)
                             ]

    print(f'value:{min_price}-{max_price}, '
          f'rating:{min_rating}-{max_rating}, '
          f'data_samples={len(csv_data_temp)}')

    figure = {'data': [go.Scattermapbox(lat=csv_data_temp['latitude'],
                                        lon=csv_data_temp['longitude'],
                                        text=csv_data_temp['neighbourhood_cleansed'],
                                        mode='markers',  marker_size=4,
                                        marker_color='rgba(22, 182, 255, .9)'),
                       ],
              'layout': go.Layout(
                  hovermode='closest',
                  mapbox=dict(accesstoken=open("mapbox_token").read(),
                              style='light', bearing=0,
                              center=go.layout.mapbox.Center(
                                  lat=np.mean(csv_data_temp['latitude']),
                                  lon=np.mean(csv_data_temp['longitude'])),
                              pitch=0, zoom=12))}

    h, h_bins = np.histogram(csv_data_temp['price'], bins=30)
    h_bins = (h_bins[0:-1] + h_bins[1:]) / 2
    figure_2 = {'data': [go.Scatter(x=h_bins, y=h,
                                    marker_color='rgba(22, 182, 255, .9)'),],
                'layout': go.Layout(hovermode='closest',)}

    price_table = get_statistics(csv_data_temp)

    return dcc.Graph(figure=figure), dcc.Graph(figure=figure_2), price_table


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
                                   min=3, max=5, step=0.1, value=3),
                        dcc.Slider(id='slider_rating_max',
                                   min=3, max=5, step=0.1, value=5),
                        html.Div(id='slider_rating_container')]),
                    style=temp_style,
                    width=2,
                ),

                dbc.Col(html.Button('Run', id='btn-next'), width=2),

                dbc.Col(
                    dash_table.DataTable(
                        id='dataframe_output',
                        sort_mode='single',
                        columns=[{"name": "avg " + i, "id": i, } for i in
                                 ["neighbourhood_cleansed",
                                  "price",
                                  "review_scores_rating"]], ),
                    width=2
                )

                #dbc.Col(dash_table.DataTable(id='dataframe_output'),
                #        width=4)

                #html.Div(id='dataframe_output'),

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
         dash.dependencies.Output('main_graph_2', 'children'),
         dash.dependencies.Output('dataframe_output', 'data')],
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
        elif 'slider_rating_min' in changed_id:
            global min_rating
            min_rating = float(val3)
        elif 'slider_rating_max' in changed_id:
            global max_rating
            max_rating = float(val4)
        elif 'btn-next' in changed_id:
            print("TODO")
        g1, g2, t = draw_data()
        return f'Price {min_price} - {max_price} Euros', \
               f'Rating {min_rating} - {max_rating} Stars', \
               g1, g2, t


    app.run_server(debug=True)
