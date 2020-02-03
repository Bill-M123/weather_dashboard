import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go


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
            print(col,len(xs),len(ys))
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
            print(col,len(xs),len(ys))
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

        #print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))
        #print('Slope(b): {:.2f}'.format(b))

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

        layout={#'title': 'Boston',
                'barmode':'stack',
                'legend':{'y':1.05,'orientation':'h'},
                'margin': {'l':40, 't':40, 'r':25, 'b':40},
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
                'legend':{'y':-.15,'orientation':'h'},
                'margin': {'l':40, 't':60, 'r':25, 'b':60},
                }

        fig={'data':data,'layout':layout}
        return fig
