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
fonts_histogram = dict(family="Courier New, monospace", size=8,
                      color="RebeccaPurple")

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
min_price, max_price = 0, 1000
min_rating, max_rating = 3, 5

print(len(csv_data))
csv_data = csv_data[csv_data.review_scores_rating.notnull()]
print(len(csv_data))
csv_data.price = csv_data.price.str.replace('$', '', regex=True)
csv_data.price = csv_data.price.str.replace(',', '', regex=True)
csv_data.price = csv_data.price.astype("float")
csv_data = csv_data[csv_data["price"] <= 1000]
print(len(csv_data))


def get_statistics(d):
    df = pd.DataFrame(d.groupby('neighbourhood_cleansed').agg(
        {
            'id': 'count',
            'price': 'median',
            'review_scores_rating': 'median',
         }
    )).round(2)
    data_t = df.reset_index().to_dict('records')
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
                                        mode='markers',  marker_size=7,
                                        marker_color='rgba(22, 182, 255, .9)'),
                       ],
              'layout': go.Layout(
                  height=500,
                  hovermode='closest',
                  autosize=False,
                  margin={"l": 0, "r": 0, "b": 0, "t": 0, "pad": 0},
                  mapbox=dict(accesstoken=open("mapbox_token").read(),
                              style='outdoors', bearing=0,
                              center=go.layout.mapbox.Center(
                                  lat=np.mean(csv_data_temp['latitude']),
                                  lon=np.mean(csv_data_temp['longitude'])),
                              pitch=0, zoom=13))}

    h, h_bins = np.histogram(csv_data_temp['price'], bins=30)
    h_bins = (h_bins[0:-1] + h_bins[1:]) / 2
    figure_2 = {'data': [go.Scatter(x=h_bins, y=h,
                                    marker_color='rgba(22, 182, 255, .9)'),],
                'layout': go.Layout(
                    title="Prices Distribution",
                    xaxis_title="Price ($)",
                    yaxis_title="Counts",
                    font=fonts_histogram,
                    hovermode='closest',
                    autosize=False,
                    height=200,
                    margin={"l": 40, "r": 15, "b": 30, "t": 30, "pad": 0},
                )}

    nbeds = csv_data_temp['beds'].dropna()
    h, h_bins = np.histogram(nbeds, bins=range(int(nbeds.min()),
                                               int(nbeds.max())))
    h_bins = np.array(list(range(int(nbeds.min()), int(nbeds.max()))))
    figure_3 = {'data': [go.Scatter(x=h_bins, y=h,
                                    marker_color='rgba(22, 182, 255, .9)'),],
                'layout': go.Layout(
                    title="#Beds Distribution",
                    xaxis_title="#Beds",
                    yaxis_title="Counts",
                    font=fonts_histogram,
                    hovermode='closest',
                    autosize=False,
                    height=200,
                    margin={"l": 40, "r": 15, "b": 30, "t": 30, "pad": 0},
                )}

    nbedrooms = csv_data_temp['bedrooms'].dropna()
    h, h_bins = np.histogram(nbedrooms, bins=range(1, 7))
    h_bins = np.array(list(range(1, 7)))
    figure_4 = {'data': [go.Scatter(x=h_bins, y=h,
                                    marker_color='rgba(22, 182, 255, .9)'),],
                'layout': go.Layout(
                    title="#Bedrooms Distribution",
                    xaxis_title="#Bedrooms",
                    yaxis_title="Counts",
                    font=fonts_histogram,
                    hovermode='closest',
                    autosize=False,
                    height=200,
                    margin={"l": 40, "r": 15, "b": 30, "t": 30, "pad": 0},
                )}


    price_table = get_statistics(csv_data_temp)

    return dcc.Graph(figure=figure,
                     config={'displayModeBar': False}), \
           dcc.Graph(figure=figure_2,
                     config={'displayModeBar': False}), \
           dcc.Graph(figure=figure_3,
                     config={'displayModeBar': False}), \
           dcc.Graph(figure=figure_4,
                     config={'displayModeBar': False}), \
           price_table


def get_layout():
    """
    Initialize the UI layout
    """
    global data
    cols = [{"name": "neighbourhood_cleansed", "id": "neighbourhood_cleansed"}]
    cols.append({"name": "count", "id": "id"})
    cols += [{"name": "avg " + i, "id": i, }
             for i in
             ["price", "review_scores_rating"]]


    layout = dbc.Container([
        # Title
        dbc.Row(dbc.Col(html.H2("Airbnb Data Visualization Example",
                                style={'textAlign': 'center',
                                       'color': colors['text']}))),

        # Main Graph
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure={'data': [go.Scatter(x=[1], y=[1])],},
                              config=dict(displayModeBar=False)),
                    width=9, id="map_graph"),

                dbc.Col(
                    dash_table.DataTable(
                        id='dataframe_output',
                        fixed_rows={'headers': True},
                        style_cell={'fontSize': 8, 'font-family': 'sans-serif',
                                    'minWidth': 10,
                                    'width': 40,
                                    'maxWidth': 95},
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable="single",
                        selected_columns=[],
                        selected_rows=[],
                        style_table={'height': 700},
                        virtualization=True,
                        #page_size=20,
                        columns=cols,
                        style_header={
                            'font-family': 'sans-serif',
                            'fontWeight': 'bold',
                            'font_size': '9px',
                            'color': 'white',
                            'backgroundColor': 'black'
                        },
                    ),
                    width=3
                ),
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
                        html.Div(id='slider_price_container'),]
                    ),
                    width=2,
                ),

                dbc.Col(
                    html.Div([
                        dcc.Slider(id='slider_rating_min',
                                   min=3, max=5, step=0.1, value=3),
                        dcc.Slider(id='slider_rating_max',
                                   min=3, max=5, step=0.1, value=5),
                        html.Div(id='slider_rating_container')]),
                    width=2,
                ),

                dbc.Col(
                    dcc.Graph(figure={'data': [go.Scatter(x=[1], y=[1])]}),
                    width=2, id="hist_graph_1"),

                dbc.Col(
                    dcc.Graph(figure={'data': [go.Scatter(x=[1], y=[1])]}),
                    width=2, id="hist_graph_2"),

                dbc.Col(
                    dcc.Graph(figure={'data': [go.Scatter(x=[1], y=[1])]}),
                    width=2, id="hist_graph_3"),

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
         dash.dependencies.Output('map_graph', 'children'),
         dash.dependencies.Output('hist_graph_1', 'children'),
         dash.dependencies.Output('hist_graph_2', 'children'),
         dash.dependencies.Output('hist_graph_3', 'children'),
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
        g1, g2, g3, g4, t = draw_data()
        return f'Price {min_price} - {max_price} $', \
               f'Rating {min_rating} - {max_rating} Stars', \
               g1, g2, g3, g4, t


    app.run_server(debug=True)
