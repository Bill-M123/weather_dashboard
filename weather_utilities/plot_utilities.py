import pandas as pd

import dash
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import plotly.offline as pyo
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html



class Plot_Utils():

    def __init__(self):
        ''' Constructor for this class. '''
        return

    def plotly_scatter(self,df,filename='tmp.html',title='Title',
    xaxis_title='Xaxis Title',yaxis_title='Yaxis Title'):
        '''df is dataframe where col0 are xs followed by columns of ys.
        column names are used as trace labels.'''

        data=[]
        step=0

        for col in range(1,len(df.columns)):
            xs=df[df.columns[0]].values
            #xs=list(range(len(xs)))
            ys=df[df.columns[col]].values
            data.append(go.Scatter(x=xs,
                                    y=ys,
                                    mode='markers',
                                    name=df.columns[col]
                                    ))
            step+=1

        layout=go.Layout(title=title,
                        xaxis={'title':xaxis_title},
                        yaxis={'title':yaxis_title},
                        hovermode='closest'
                        )

        fig=go.Figure(data=data,layout=layout)
        pyo.plot(fig)

    def plotly_scatter_serv(self,df,filename='tmp.html',title='Title',
        xaxis_title='Xaxis Title',yaxis_title='Yaxis Title',width='50%',
        height='50%'):
        '''df is dataframe where col0 are xs followed by columns of ys.
        column names are used as trace labels.'''

        data=[]
        step=0

        for col in range(1,len(df.columns)):
            xs=df[df.columns[0]].values
            #xs=list(range(len(xs)))
            ys=df[df.columns[col]].values
            data.append(go.Scatter(x=xs,
                                    y=ys,
                                    mode='markers',
                                    name=df.columns[col]
                                    ))

        layout=go.Layout(title=title,
                        xaxis={'title':xaxis_title},
                        yaxis={'title':yaxis_title},
                        hovermode='closest',
                        height=height,
                        width=width
                        )

        fig=go.Figure(data=data,layout=layout)
        return fig

    def scatter_just_data(self,df,colors=['crimson','cornflowerblue']):
        '''df is dataframe where col0 are xs followed by columns of ys.
        column names are used as trace labels. Data is returned as a list
        of go objects'''

        data=[]
        step=0

        for col in range(1,len(df.columns)):
            xs=df[df.columns[0]].values
            ys=df[df.columns[col]].values
            data.append(go.Scatter(x=xs,
                                    y=ys,
                                    mode='markers',
                                    marker=dict(
                                    color=colors[col-1]),
                                    name=df.columns[col]
                                    ))

        return data

    def best_fit(self,df):
        X=df[df.columns[0]].apply(int).values
        Y=df[df.columns[1]].apply(float).values
        xbar = sum(X)/len(X)
        ybar = sum(Y)/len(Y)
        n = len(X) # or len(Y)

        numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
        denum = sum([xi**2 for xi in X]) - n * xbar**2

        b = numer / denum
        a = ybar - b * xbar

        bf_line=pd.DataFrame()
        bf_line['YEAR']=X
        bf_line['BF']=a+b*bf_line['YEAR']

        return a, b, bf_line

    def get_htcld_bar_data(self,htcld_years):
        data=[go.Bar(name='Hot 1-10', x=htcld_years.Decade.values, y=htcld_years.T10.values,
            marker_color='red'),
            go.Bar(name='Hot 11-20', x=htcld_years.Decade.values, y=htcld_years.T20.values,
            marker_color='crimson'),

            go.Bar(name='Cold 11-20', x=htcld_years.Decade.values, y=htcld_years.B20.values,
            marker_color='cornflowerblue'),
            go.Bar(name='Cold 1-10', x=htcld_years.Decade.values, y=htcld_years.B10.values,
            marker_color='blue')]

        layout={'title': {'text':'Number of hot and cold years', 'y':1.0},
                'barmode':'stack',
                'legend':{'y':-0.10,'orientation':'h'},
                'margin': {'l':40, 't':20, 'r':15, 'b':10},
                }

        fig={'data':data,'layout':layout}
        return fig

    def get_annual_hilo_trend_data(self,years_df):

        # Calculate best fit line
        bf_slope,bf_intercept,bf=self.best_fit(years_df[['YEAR','T_avg']])

        data=[go.Scatter(x=years_df.YEAR, y=years_df.TMAX_max,
            fill=None,mode='lines',line_color='crimson',
            name='Yearly Max'),

            go.Scatter(x=years_df.YEAR, y=years_df.TMIN_max,
                fill='tonexty', # fill area between trace0 and trace1
                mode='lines',line_color='crimson',line={'dash': 'dash'},
                name='Warmest cooling'),

            go.Scatter(x=years_df.YEAR, y=years_df.TMAX_min,
                fill=None,mode='lines',line_color='cornflowerblue',
                line={'dash': 'dash'},name='Coolest Warming'
                ),

            go.Scatter(
                x=years_df.YEAR, y=years_df.TMIN_min,
                fill='tonexty', # fill area between trace0 and trace1
                mode='lines',line_color='cornflowerblue',
                name='Yearly min'),

            go.Scatter(x=years_df.YEAR, y=years_df.T_avg,
                fill=None,mode='lines',line_color='gray',
                line={'width':5},name='Annual Avg Temp'
                ),

            go.Scatter(x=bf.YEAR, y=bf.BF,
                fill=None,mode='lines',line={'dash': 'dash','width':3},
                line_color='black',line_width=3,
                name='Best Fit Annual Temp'),] #End Data

        layout={'title': 'Annual Highs, Lows, Averages, and Trend',
                'legend':{'y':-.20,'orientation':'h'},

                }

        fig={'data':data,'layout':layout}
        return fig

    def get_annual_trend_data(self,years_df):

        # Calculate best fit line
        bf_slope,bf_intercept,bf=self.best_fit(years_df[['YEAR','T_avg']])

        data=[go.Scatter(x=years_df.YEAR, y=years_df.T_avg,
                fill=None,mode='lines',line_color='gray',
                line={'width':5},name='Annual Avg Temp'
                ),

            go.Scatter(x=bf.YEAR, y=bf.BF,
                fill=None,mode='lines',line={'dash': 'dash','width':3},
                line_color='black',line_width=3,
                name='Best Fit Annual Temp'),] #End Data

        layout={'title': 'Annual Averages, and Trend',
                'legend':{'y':-.15,'orientation':'h'},
                'yaxis':{'range':[47, 55]}
                }

        fig={'data':data,'layout':layout}
        return fig

    def initialize_slider(self,min=1940,max=2020,value=[1940,2020]):
        return dcc.RangeSlider(id='range_slider',
            min=min,max=max,step=10,
            marks={i: i for i in range(1940,2030,20)},
            #value=[min,max],
            updatemode='drag')

    def get_full_layout(self, table_df,
    htcld_years,  years_df,dr_dn_options, map_html='my_cape_house.html',
    station_id='USW00014739',slide_low=1940, slide_high=2020, ):

        child=[html.Div(id='first-row',
            className="first_row",
            children = [

        # Data Table
        html.Div(id='summary-table',
            className="summary_table",
            children = [

                dcc.Dropdown(id='ws-drop-down',
                    className="dr_down",
                    options=dr_dn_options,
                    value=station_id,),

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
                children=[self.initialize_slider(value=[slide_low,slide_high])],),],#end Data Table Children
            ),#End Data Table

        html.Div(id='bar-div',
            className='bar_div',
            children = [dcc.Graph(id='bar-graph',
                figure=self.get_htcld_bar_data(htcld_years),
                config={'modeBarButtonsToRemove': ['toggleSpikelines',
                    "select2d", "lasso2d","hoverCompareCartesian"]},
                style={'vertical-align': 'top',
                'width': '70%', 'height':'250px','margin-top': '10px',}),]), #End bar-div

        html.Div(id='map=div',
            className="map_style",
            children = [html.Iframe(id='map',
            srcDoc=open(map_html,'r').read(),
            height='250vh', width='95%')],)],

        ),#<--End First Row
        html.Hr(),

        #4 Readings per year
        html.Div(id='second-row',
            className="second_row",
            children = [dcc.Graph(id='yearly-scatter',
                    figure=self.get_annual_trend_data(years_df),
                    config={'modeBarButtonsToRemove': ['toggleSpikelines',
                    "select2d", "lasso2d","hoverCompareCartesian"]},
                    style={'vertical-align': 'top',
                    'width': '95%', 'height':'250px','margin-top': '10px',}
                     )])#End second Row

        ]
        return child
