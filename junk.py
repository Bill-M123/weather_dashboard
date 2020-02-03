import pandas as pd
import numpy as np

from weather_utilities.weather_utilities import Weather_Utils
from weather_utilities.plot_utilities import Plot_Utils

weather =Weather_Utils()
make_plot=Plot_Utils()

weather_station='Boston'
xaxis_title='1 Reading per Week'
yaxis_title='Degrees F'

#yearly graph
df=weather.open_existing_weather_station_data('USW00014739')
years_df=weather.calculate_yearly_data(df)
print('years_df\n',years_df.head(1))
###
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=years_df.YEAR, y=years_df.TMAX_max,
    fill=None,
    mode='lines',
    line_color='crimson',
    name='Yearly Max'
    ))
fig.add_trace(go.Scatter(
    x=years_df.YEAR, y=years_df.TMIN_max,
    fill='tonexty', # fill area between trace0 and trace1
    mode='lines',
    line_color='crimson',
    line={'dash': 'dash'},
    name='Warmest cooling'))

fig.add_trace(go.Scatter(x=years_df.YEAR, y=years_df.TMAX_min,
    fill=None,
    mode='lines',
    line_color='cornflowerblue',
    line={'dash': 'dash'},
    name='Coolest Warming'
    ))
fig.add_trace(go.Scatter(
    x=years_df.YEAR, y=years_df.TMIN_min,
    fill='tonexty', # fill area between trace0 and trace1
    mode='lines',
    line_color='cornflowerblue',
    name='Yearly min'))

fig.add_trace(go.Scatter(x=years_df.YEAR, y=years_df.T_avg,
    fill=None,
    mode='lines',
    line_color='gray',
    line={'width':5},
    name='Annual Avg Temp'
    ))

bf_slope,bf_intercept,bf=make_plot.best_fit(years_df[['YEAR','T_avg']])
fig.add_trace(go.Scatter(x=bf.YEAR, y=bf.BF,
    fill=None,
    mode='lines',
    line={'dash': 'dash','width':3},
    line_color='black',
    line_width=3,
    name='Best Fit Annual Temp'
    ))

fig.show()

year_count,yr_avg_dec_df,htcld_years=\
    weather.calculate_yearly_summaries(years_df)

print('year_count: {}'.format(year_count))
print('decade yr_avg_dec_df:\n',yr_avg_dec_df.head(3),'\n')
print('htcld_years summary:\n',htcld_years.head(3),'\n')

fig = go.Figure(data=[
    go.Bar(name='Hottest 10', x=htcld_years.Decade.values, y=htcld_years.T10.values,
    marker_color='red'),
    go.Bar(name='2nd Hottest 10', x=htcld_years.Decade.values, y=htcld_years.T20.values,
    marker_color='crimson'),

    go.Bar(name='2nd Coldest 10', x=htcld_years.Decade.values, y=htcld_years.B10.values,
    marker_color='cornflowerblue'),
    go.Bar(name='Coldest 10', x=htcld_years.Decade.values, y=htcld_years.B20.values,
    marker_color='blue')
])
# Change the bar mode
fig.update_layout(barmode='stack')
fig.show()

fig=make_plot.get_htcld_bar_fig(htcld_years)
fig.show()
