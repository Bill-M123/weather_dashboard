import dash
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
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

all_days_df=weather.open_existing_weather_station_data('USW00014739')
raw_all_days_df=all_days_df.copy()

day_per_wk_df=weather.one_day_per_week(all_days_df)
years_df=weather.calculate_yearly_data(all_days_df)
year_count,yr_avg_dec_df,htcld_years=\
    weather.calculate_yearly_summaries(years_df)

warmest_day,warmest_day_temp,coldest_day,coldest_day_temp=\
    weather.get_hot_cold_days(all_days_df)
hottest_year,hottest_year_temp,coldest_year,coldest_year_temp=\
    weather.get_hot_cold_years(all_days_df)

bf_intercept,bf_slope,bf=make_plot.best_fit(years_df[['YEAR','T_avg']])

table_df=weather.make_summary_table(all_days_df,bf_slope)

app.layout = html.Div([

    # First Row
    html.Div(children = [
    # Map

    # Data Table
    html.Div(id='summary_table',children = [
            html.H1('Boston',style={'vertical-align': 'top',
            'margin-top': '0px',}),
            dash_table.DataTable(id='table',
            columns=[{"name": i, "id": i} for i in table_df.columns],
            data=table_df.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'},
            style_as_list_view=True,
            style_cell_conditional=[
            {
                'if': {'column_id': 'Parameters'},
                'textAlign': 'left',
                'fontWeight': 'bold',
                'width':'10%'
            },
            {
                'if': {'column_id': 'Dates'},
                'textAlign': 'center',
                'width':'8%'
            },
            {
                'if': {'column_id': 'Temp'},
                'textAlign': 'right',
                'width':'7%',
            }
            ]),

        html.Div(children=[dcc.RangeSlider(id='range_slider',
            min=1940,max=2020,step=10,
            marks={i: i for i in range(1940,2030,20)},
            value=[1940,2020],
            updatemode='drag')],
        style={'margin-top':'15px','vertical-align':'bottom'}),

            ],style={'display':'inline-block',
            'vertical-align': 'top',
            'height':'300','width': '25vw',
            'margin-right': '20px',
            'margin-left': '10px',
            'backgroundColor':'white'}),

    dcc.Graph(figure=make_plot.get_htcld_bar_data(htcld_years),
        config={'modeBarButtonsToRemove': ['toggleSpikelines', "select2d", "lasso2d"]},
        style={'display':'inline-block','vertical-align': 'top',
        'width': '45vw','height':'50vh','margin-right': '20px',}),

        html.Div(children = [
                    html.Iframe(id='map',srcDoc=open('my_cape_house.html','r').read(),
                    height='300')],style={'display':'inline-block',
                    'margin-right': '0px',
                    'backgroundColor':'white',
                    'vertical-align': 'top',
                    'horizontal-align': 'right'}),],
    #dcc.Graph(make_plot.get_htcld_bar_fig(htcld_years))

    # set the sizing of the parent div
    style = {'display': 'inline-block',
    'height': '50vh',
    'width': '100vw',
    'vertical-align': 'bottom',
    'backgroundColor':'white'}),#<--End First Row


    #4 Readings per year
    dcc.Graph(figure=make_plot.get_annual_hilo_trend_data(years_df),
                #'data': make_plot.scatter_just_data(day_per_wk_df),
                #'layout':{#'title': 'Boston',
                #'xaxis':{'title':xaxis_title},
                #        'yaxis':{'title':yaxis_title},
                #        'marker_color':['crimson','cornflowerblue'],
                #        'legend':{'x':0,'y':110,'orientation':'h'},
                #        'margin': {'l':40, 't':60, 'r':25, 'b':60},
                #            }},

                 style={
                    'margin':{'l':2,'r':2},
                    'float':'left',
                    'hovermode':'closest',
                    'width':'100vw',
                    'height':'45vh'

                    })#End second Row

    ])
@app.callback(Output('summary_table','children'),
                [Input('range_slider','value')])
def update_value(slider_range):
    print('slider_range',slider_range)
    print(raw_all_days_df.head(2))
    all_days_df=raw_all_days_df.copy()
    all_days_df['year']=all_days_df.YEAR.apply(int)
    all_days_df=all_days_df.loc[(all_days_df['year']>=slider_range[0])&\
                                (all_days_df['year']<=slider_range[1]),:].copy()
    day_per_wk_df=weather.one_day_per_week(all_days_df)
    years_df=weather.calculate_yearly_data(all_days_df)
    year_count,yr_avg_dec_df,htcld_years=\
        weather.calculate_yearly_summaries(years_df)
    warmest_day,warmest_day_temp,coldest_day,coldest_day_temp=\
        weather.get_hot_cold_days(all_days_df)
    hottest_year,hottest_year_temp,coldest_year,coldest_year_temp=\
        weather.get_hot_cold_years(all_days_df)

    bf_intercept,bf_slope,bf=make_plot.best_fit(years_df[['YEAR','T_avg']])

    table_df=weather.make_summary_table(all_days_df,bf_slope)
    print(table_df.head(10))
    child=[
            html.H1('Boston',style={'vertical-align': 'top',
            'margin-top': '0px',}),
            dash_table.DataTable(id='table',
            columns=[{"name": i, "id": i} for i in table_df.columns],
            data=table_df.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'},
            style_as_list_view=True,
            style_cell_conditional=[
            {
                'if': {'column_id': 'Parameters'},
                'textAlign': 'left',
                'fontWeight': 'bold',
                'width':'10%'
            },
            {
                'if': {'column_id': 'Dates'},
                'textAlign': 'center',
                'width':'8%'
            },
            {
                'if': {'column_id': 'Temp'},
                'textAlign': 'right',
                'width':'7%',
            }
            ]),

        html.Div(children=[dcc.RangeSlider(id='range_slider',
            min=1940,max=2020,step=10,
            marks={i: i for i in range(1940,2030,20)},
            updatemode='drag',
            value=[slider_range[0],slider_range[1]])],
        style={'margin-top':'15px','vertical-align':'bottom'}),

            ]
    return child


if __name__ == '__main__':
    app.run_server()
