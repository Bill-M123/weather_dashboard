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
old_sliders=[1940,2020]
current_state=[]

all_state_df=weather.open_all_state_data(data_dir+'ma_weather_stations.csv')

# Set up weather station dr_dn_options
ws_list,dr_dn_options=get_wsd.make_ws_info(all_state_df)


# Set up all dfs and individual notable dates
all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
year_count,yr_avg_dec_df,htcld_years,warmest_day,\
warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
bf_slope,bf,table_df=weather.set_all_dfs(all_state_df)

current_state=make_plot.get_full_layout(table_df=table_df,
htcld_years=htcld_years, map_html='my_cape_house.html',
years_df=years_df,dr_dn_options=dr_dn_options,
station_id=old_ws,slide_low=1940, slide_high=2020,)

app.layout = html.Div(id='full_layout',children=current_state)

@app.callback(Output('full_layout','children'),
                [Input('range_slider','value'),
                Input('ws-drop-down','value')])
def update_value(slider_range,ws_id):
    global old_ws,old_sliders
    print('bob',slider_range,ws_id)
    print('jim',old_sliders,old_ws)


    ctx=dash.callback_context
    #ctx_msg = json.dumps({
    #    'states': ctx.states,
    #    'triggered': ctx.triggered,
    #    'inputs': ctx.inputs
    #}, indent=2)
    #print(ctx_msg)

    if not ctx.triggered:
        old_ws=ws_id
        old_sliders=slider_range
        print('Setting old_ws:',old_ws)
        return no_update

    elif (old_ws==ws_id) & (old_sliders==slider_range):
        print('WS and Sliders equal')
        return no_update

    elif old_sliders!=slider_range:
        print('Sliders changed')
        print(weather.set_all_dfs(all_state_df,station_id=ws_id,
        slider_low=slider_range[0], slider_high=slider_range[1]))

        all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
        year_count,yr_avg_dec_df,htcld_years,warmest_day,\
        warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
        bf_slope,bf,table_df=weather.set_all_dfs(all_state_df,station_id=ws_id,\
        slider_low=slider_range[0], slider_high=slider_range[1]),

        print('table_df after\n',table_df.head(10))
        print('\nall_days_df\n',all_days_df.head(2))
        print('htcld_years\n',htcld_years.head(2))


        children=make_plot.get_full_layout(table_df=table_df,
        htcld_years=htcld_years, map_html='my_cape_house.html',
        years_df=years_df,dr_dn_options=dr_dn_options,
        station_id=ws_id,
        slide_low=slider_range[0], slide_high=slider_range[1],)
        old_ws=ws_id
        return children


    else:
        print('Weather Station Changed')

        all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
        year_count,yr_avg_dec_df,htcld_years,warmest_day,\
        warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
        bf_slope,bf,table_df=weather.set_all_dfs(all_state_df,station_id=ws_id)

        print('table_df after\n',table_df.head(10))
        print('\nall_days_df\n',all_days_df.head(2))

        children=make_plot.get_full_layout(table_df=table_df,
        htcld_years=htcld_years, map_html='my_cape_house.html',
        years_df=years_df,dr_dn_options=dr_dn_options,
        station_id=ws_id,
        slide_low=1940, slide_high=2020,)
        old_ws=ws_id
        return children



if __name__ == '__main__':
    app.run_server()
