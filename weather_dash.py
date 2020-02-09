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

data_dir=os.getcwd()+'\\data\\'
weather =Weather_Utils()
make_plot=Plot_Utils()

app = dash.Dash()

weather_station='Boston'
xaxis_title='1 Reading per Week'
yaxis_title='Degrees F'

all_state_df=weather.open_all_state_data(data_dir+'ma_weather_stations.csv')

#all_days_df=all_state_df.loc[all_state_df.STATION=='USW00014739',:].copy()
#raw_all_days_df=all_days_df.copy()

#day_per_wk_df=weather.one_day_per_week(all_days_df)
#years_df=weather.calculate_yearly_data(all_days_df)
#year_count,yr_avg_dec_df,htcld_years=\
#    weather.calculate_yearly_summaries(years_df)

#warmest_day,warmest_day_temp,coldest_day,coldest_day_temp=\
#    weather.get_hot_cold_days(all_days_df)
#hottest_year,hottest_year_temp,coldest_year,coldest_year_temp=\
#    weather.get_hot_cold_years(all_days_df)

#bf_intercept,bf_slope,bf=make_plot.best_fit(years_df[['YEAR','T_avg']])

#table_df=weather.make_summary_table(all_days_df,bf_slope)

all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
year_count,yr_avg_dec_df,htcld_years,warmest_day,\
warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
bf_slope,bf,table_df=weather.set_all_dfs(all_state_df)

app.layout = html.Div([

    # First Row
    html.Div(children = [

    # Data Table
    html.Div(id='summary_table',children = [

            html.H1('Boston',style={'vertical-align': 'top',
            'margin-top': '0px',}),

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
                'width':'10%'
            },
            {
                'if': {'column_id': 'Dates'},
                'textAlign': 'center',
                'fontWeight': 'bold',
                'width':'8%'
            },
            {
                'if': {'column_id': 'Temp'},
                'textAlign': 'right',
                'fontWeight': 'bold',
                'width':'7%',
            }
            ]),

        html.Div(children=[dcc.RangeSlider(id='range_slider',
            min=1940,max=2020,step=10,
            marks={i: i for i in range(1940,2030,20)},
            value=[1940,2020],
            updatemode='drag')],
        style={'display':'inline-block','margin-top':'15px',
        'vertical-align':'bottom',
        'width':'20vw','horizontal-align':'left'}),

        html.Div(children=[html.Button(id='update-plots',
        children='Sync',n_clicks=0,
        style={'margin-top':'15px',
        'display':'inline-block',
        'color':'white','bg':'white',})],style={
        'align-horizontal':'right',
        'display':'inline-block',
        'margin-left': '10px'}),

        ],#end Data Table Children
        style={'display':'inline-block',
            'vertical-align': 'top',
            'height':'300','width': '25vw',
            'margin-right': '20px',
            'margin-left': '10px',
            'background-color':'white'}),#End Data Table

    html.Div(id='bar-div',children = [\
    dcc.Graph(id='bar-graph', figure=make_plot.get_htcld_bar_data(htcld_years),
        config={'modeBarButtonsToRemove': ['toggleSpikelines',
        "select2d", "lasso2d","hoverCompareCartesian"]},
        style={'vertical-align': 'bottom',
        'width': '100%','height':'90%','margin-top': '10px',}),],
        style={'display':'inline-block',
        'vertical-align': 'middle',
        'width': '45%','height':'45vh','margin-right': '20px',
        'margin-bottom': '10px',}),

    html.Div(children = [
        html.Iframe(id='map',
        srcDoc=open('my_cape_house.html','r').read(),
        height='250vh', width='95%')],style={'display':'inline-block',
        'margin-right': '0px',
        'margin-top': '30px',
        'backgroundColor':'white',
        'vertical-align': 'top',
        'horizontal-align': 'center'})],

    # set the sizing of the first row parent div
    style = {'display': 'inline-block',
    'height': '50vh',
    'width': '100%',
    'vertical-align': 'bottom',
    'backgroundColor':'white'}),#<--End First Row
    html.Hr(),

    #4 Readings per year
    html.Div(id='yearly-div',children = [\
    dcc.Graph(id='yearly-scatter',figure=make_plot.get_annual_hilo_trend_data(years_df),
                config={'modeBarButtonsToRemove': ['toggleSpikelines',
                "select2d", "lasso2d","hoverCompareCartesian"]},
                 style={
                    'margin':{'l':2,'r':2,'b':2},
                    'float':'left',
                    'hovermode':'closest',
                    'width':'95vw',
                    'height':'45vh'

                    })])#End second Row

    ])
@app.callback(Output('tablea','data'),
                [Input('range_slider','value')])
def update_value(slider_range):

    print(raw_all_days_df.head(2))
    table_df=weather.slider_input_to_table(raw_all_days_df,
                slider_range[0],slider_range[1])
    data=table_df.to_dict('records')
    return data#child

@app.callback(Output('bar-graph','figure'),
                [Input('range_slider','value')])
def update_bar(slider_range):

    all_days_df=raw_all_days_df.copy()
    all_days_df['year']=all_days_df.YEAR.apply(int)
    all_days_df=all_days_df.loc[(all_days_df['year']>=slider_range[0])&\
                                (all_days_df['year']<slider_range[1]),:].copy()

    day_per_wk_df=weather.one_day_per_week(all_days_df)
    years_df=weather.calculate_yearly_data(all_days_df)
    year_count,yr_avg_dec_df,htcld_years=\
        weather.calculate_yearly_summaries(years_df)
    htcld_years['dec']=htcld_years['Decade'].str.strip("'s").apply(int)

    htcld_years=htcld_years.loc[((htcld_years.dec>=slider_range[0])&\
                                (htcld_years.dec<=slider_range[1])),:]
    htcld_years=htcld_years.drop('dec',axis=1)
    print('htcld post drop\n',htcld_years.head(2))

    figure=make_plot.get_htcld_bar_data(htcld_years)
    return figure


@app.callback(Output('yearly-scatter','figure'),
                [Input('range_slider','value')])
def update_all_time(slider_range):

    all_days_df=raw_all_days_df.copy()

    all_days_df['year']=all_days_df.YEAR.apply(int)
    all_days_df=all_days_df.loc[(all_days_df['year']>=slider_range[0])&\
                                (all_days_df['year']<slider_range[1]),:].copy()

    years_df=weather.calculate_yearly_data(all_days_df)
    years_df['YEAR']=years_df['YEAR'].apply(int)
    print('Liam\n',years_df.head(4))

    years_df=years_df.loc[((years_df.YEAR>=slider_range[0])&\
                                (years_df.YEAR<=slider_range[1])),:]


    figure=make_plot.get_annual_trend_data(years_df)
    return figure

if __name__ == '__main__':
    app.run_server()
