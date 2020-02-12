import dash
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import os

from numpy import random

import datetime as dt

from weather_utilities.weather_utilities import Weather_Utils
from weather_utilities.plot_utilities import Plot_Utils
from weather_utilities.weather_stations_data import Weather_Stations_Data

data_dir=os.getcwd()+'\\data\\'
weather =Weather_Utils()
make_plot=Plot_Utils()
get_wsd=Weather_Stations_Data()

app = dash.Dash()

weather_station='Boston'
xaxis_title='1 Reading per Week'
yaxis_title='Degrees F'

initial_ws='USW00014739'
old_ws=initial_ws

all_state_df=weather.open_all_state_data(data_dir+'ma_weather_stations.csv')

# Set up weather station dr_dn_options
ws_list,dr_dn_options=get_wsd.make_ws_info(all_state_df)


# Set up all dfs and individual notable dates
all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
year_count,yr_avg_dec_df,htcld_years,warmest_day,\
warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
bf_slope,bf,table_df=weather.set_all_dfs(all_state_df)

app.layout = html.Div(id='full_layout',children=[

    # First Row
    html.Div(id='first-row',
        className="first_row",
        children = [

    # Data Table
    html.Div(id='summary-table',
        className="summary_table",
        children = [

            dcc.Dropdown(id='ws-drop-down',
                className="dr_down",
                options=dr_dn_options,
                value='USW00014739',),

            dash_table.DataTable(id='tablea',
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
            },
            {
                'if': {'column_id': 'Dates'},
                'textAlign': 'center',
                'fontWeight': 'bold',
            },
            {
                'if': {'column_id': 'Temp'},
                'textAlign': 'right',
                'fontWeight': 'bold',
            }
            ]),

        html.Div(id='slider_div',
            className="slider-st",
            children=[make_plot.initialize_slider()],),],#end Data Table Children
        ),#End Data Table

    html.Div(id='bar-div',
        className='bar_div',
        children = [dcc.Graph(id='bar-graph',
            figure=make_plot.get_htcld_bar_data(htcld_years),
            config={'modeBarButtonsToRemove': ['toggleSpikelines',
                "select2d", "lasso2d","hoverCompareCartesian"]},
            style={'vertical-align': 'top',
            'width': '70%', 'height':'250px','margin-top': '10px',}),]), #End bar-div

    html.Div(id='map=div',
        className="map_style",
        children = [html.Iframe(id='map',
        srcDoc=open('my_cape_house.html','r').read(),
        height='250vh', width='95%')],)],

    ),#<--End First Row
    html.Hr(),

    #4 Readings per year
    html.Div(id='second-row',
        className="second_row",
        children = [dcc.Graph(id='yearly-scatter',
                figure=make_plot.get_annual_hilo_trend_data(years_df),
                config={'modeBarButtonsToRemove': ['toggleSpikelines',
                "select2d", "lasso2d","hoverCompareCartesian"]},
                style={'vertical-align': 'top',
                'width': '95%', 'height':'250px','margin-top': '10px',}
                 )])#End second Row

    ])

#@app.callback(Output('tablea','data'),
#                [Input('range_slider','value'),
#                Input('ws-drop-down','value')])
#def update_value(slider_range,ws_id):

#    print('bob',slider_range,ws_id)
#    print(old_ws,ws_id)
#    if old_ws==ws_id:
#        print('Same Weather Station')

#        all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
#        year_count,yr_avg_dec_df,htcld_years,warmest_day,\
#        warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
#        bf_slope,bf,table_df=weather.set_all_dfs(all_state_df,station_id=ws_id)

#        print(raw_all_days_df.head(2))
#        table_df=weather.slider_input_to_table(raw_all_days_df,
#                    slider_range[0],slider_range[1])
#        data=table_df.to_dict('records')

#        i_slide=make_plot.initialize_slider()

        #data for table, initialized slider
#        return data#,islide



#    else:
#        print('Weather Station Changed')

#        all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
#        year_count,yr_avg_dec_df,htcld_years,warmest_day,\
#        warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
#        bf_slope,bf,table_df=weather.set_all_dfs(all_state_df,station_id=ws_id)

#        print(raw_all_days_df.head(2))
#        table_df=weather.slider_input_to_table(raw_all_days_df,
#                    slider_range[0],slider_range[1])
#        data=table_df.to_dict('records')
#    return data#child



if __name__ == '__main__':
    app.run_server()
