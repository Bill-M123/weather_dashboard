import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from numpy import random

import datetime as dt

from weather_utilities.weather_utilities import Weather_Utils
from weather_utilities.plot_utilities import Plot_Utils

weather =Weather_Utils()
make_plot=Plot_Utils()

app = dash.Dash()

weather_station='Boston'
xaxis_title='1 Reading per Week'
yaxis_title='Degrees F'

df=weather.open_existing_weather_station_data('USW00014739')
df=weather.one_day_per_week(df)

app.layout = html.Div([
    # Top Row
    html.Div([
        html.Div(style={'height': '50vh','width': '40vw','display':'inline-block'}, children=dcc.Graph(
            figure={
                    'data': make_plot.scatter_just_data(df),
                    'layout':{'title': 'Boston',
                            'xaxis':{'title':xaxis_title},
                            'yaxis':{'title':yaxis_title},
                            'legend':{'x':0,'y':110,'orientation':'h'},

                                }},
                     style={'height': 'inherit',
                        'width:':'inherit',
                        'margin':{'l':2,'r':2},
                        'float':'left',
                        'hovermode':'closest',
                        'display':'inline-block',
                        })),

    html.Div(style={'height': '50vh',
                    'width': '30vw',
                    'display':'inline-block',
                    }, children=dcc.Graph(figure={
        'data': [{
            'x': [1, 2, 3],
            'y': [3, 1, 2]
        }],
    }, style={'height': 'inherit',
                'width': 'inherit',
                'backgroundColor':'navy',
                })),]),#End Top Row
    # Second Row
    html.Div(style={'height': '50vh',
                    'width': '100vw',
                    'display':'inline-block'}, children=dcc.Graph(
        figure={
                'data': make_plot.scatter_just_data(df),
                'layout':{'title': 'Boston',
                        'xaxis':{'title':xaxis_title},
                        'yaxis':{'title':yaxis_title},
                        'legend':{'x':0,'y':110,'orientation':'h'},
                        'height': 'inherit',
                        'width:':'100vw',

                            }},
                 style={'height': 'inherit',
                    'width:':'inherit',
                    'margin':{'l':2,'r':2},
                    'float':'left',
                    'hovermode':'closest',
                    'display':'inline-block',
                    }))#End second Row

    ])

if __name__ == '__main__':
    app.run_server()
