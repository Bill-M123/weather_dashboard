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

print('Starting weather_utilities.....All-state.....\n',weather.all_state_df.head(7))
print(weather.htcld_years.head(4))
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

#all_state_df=weather.open_all_state_data(data_dir+'ma_weather_stations.csv')

# Set up weather station dr_dn_options
ws_list,dr_dn_options=get_wsd.make_ws_info(weather.all_state_df)


# Set up all dfs and individual notable dates
#all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
#year_count,yr_avg_dec_df,htcld_years,warmest_day,\
#warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
#bf_slope,bf,table_df=weather.set_all_dfs(all_state_df)

print('1st no_weather.htcld_years\n',weather.htcld_years.head(3))
print('1st weather.yearly_summary\n',weather.yearly_summary_df.head(4))

weather.current_state=make_plot.get_full_layout(table_df=weather.table_df,
            htcld_years=weather.htcld_years,
            map_html='my_cape_house.html',
            years_df=weather.years_df,
            dr_dn_options=dr_dn_options,
            station_id=weather.old_ws,
            slide_low=weather.old_sliders[0],
            slide_high=weather.old_sliders[1],)

app.layout = html.Div(id='full_layout',children=weather.current_state)

@app.callback(Output('full_layout','children'),
                [Input('range_slider','value'),
                Input('ws-drop-down','value')])
def update_value(slider_range,ws_id):

    print('\n\nPassed Values',slider_range,ws_id)
    print('Existing Values {} {}\n\n'.format(weather.old_sliders,weather.old_ws))


    ctx=dash.callback_context
    #ctx_msg = json.dumps({
    #    'states': ctx.states,
    #    'triggered': ctx.triggered,
    #    'inputs': ctx.inputs
    #}, indent=2)
    #print(ctx_msg)

    if not ctx.triggered:
        #old_ws=ws_id
        #old_sliders=slider_range
        print('No tigger yet.  Setting old_ws:',weather.old_ws,'sending no update\n\n')
        return no_update

    elif (weather.old_ws==ws_id) & (weather.old_sliders==slider_range):
        print('WS and Sliders equal to existing values.  Sending no update')
        return no_update

    elif weather.old_sliders!=slider_range:
        print('Sliders changed\n\n')
        print('Old: {}  New: {}'.format(weather.old_sliders,slider_range))

        weather.update_slider_change(slider_range)

        weather.bf_intercept,weather.bf_slope,weather.bf_line_df=\
            weather.make_plot.best_fit(weather.years_df[['YEAR','T_avg']])

        weather.table_df=weather.make_summary_table(weather.all_days_df,weather.bf_slope)
        print('table_df after\n',weather.table_df.head(10))
        print('weather.htcld_years\n',weather.htcld_years.head(3))

        #Caclulate Decades for hot_cold subset
        decade_list=[str(x)+"'s" for x in range(slider_range[0],slider_range[1]+10,10)]

        #htcld_tmp=weather.htcld_years.loc[(weather.htcld_years.Decade>=slider_range[0])&\
        #    (weather.htcld_years.year>=slider_range[1]),:].copy()
        htcld_tmp=\
            weather.htcld_years.loc[weather.htcld_years.Decade.isin(decade_list),:].copy()
        print('Decades: ',decade_list)
        print('htcld_years\n',htcld_tmp.head(2))


        children=make_plot.get_full_layout(table_df=weather.table_df,
        htcld_years=htcld_tmp, map_html='my_cape_house.html',
        years_df=weather.years_df,dr_dn_options=dr_dn_options,
        station_id=ws_id,
        slide_low=slider_range[0], slide_high=slider_range[1],)
        weather.old_sliders=slider_range
        print('tried to update slider info\n\n')
        return children


    else:
        print('Weather Station Changed')

        weather.update_weather_station_change(ws_id)

        print('table_df after\n',weather.table_df.head(10))

        children=make_plot.get_full_layout(table_df=weather.table_df,
        htcld_years=weather.htcld_years, map_html='my_cape_house.html',
        years_df=weather.years_df,dr_dn_options=dr_dn_options,
        station_id=ws_id,
        slide_low=1940, slide_high=2020,)
        weather.old_ws=ws_id
        return children



if __name__ == '__main__':
    app.run_server()
