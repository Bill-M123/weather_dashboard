import pandas as pd
import requests
import os

from weather_utilities.plot_utilities import Plot_Utils


class Weather_Utils():

    def __init__(self,initial_ws='USW00014739',old_sliders=[1940,2020],
                startDate='1937-01-01',endDate='2019-12-31'):
        ''' Constructor for this class. '''
        #self.weather =Weather_Utils()

        self.make_plot=Plot_Utils()
        self.initial_ws=initial_ws
        self.old_sliders=old_sliders
        self.data_dir=os.getcwd()+'/Data/'
        self.all_state_df=\
            self.open_all_state_data(self.data_dir+'ma_weather_stations.csv')

        self.all_state_df['year']=\
                    self.all_state_df.DATE.apply(lambda x: int(x.split('-')[0]))
        self.all_days_df=\
            self.all_state_df.loc[self.all_state_df.STATION==initial_ws,:]


        self.raw_all_days_df=self.all_days_df.copy()
        self.day_per_wk_df=self.one_day_per_week(self.all_days_df)

        self.years_df=self.calculate_yearly_data(self.all_days_df)

        self.year_count=len(self.all_days_df.YEAR.unique())
        self.year_count,self.yearly_summary_df,self.htcld_years=\
            self.calculate_yearly_summaries(self.years_df)

        self.yr_avg_dec_df=self.yearly_summary_df.copy()
        self.warmest_day,self.warmest_day_temp,self.coldest_day,\
            self.coldest_day_temp=self.get_hot_cold_days(self.all_days_df)

        self.bf_intercept,self.bf_slope,self.bf=\
            self.make_plot.best_fit(self.years_df[['YEAR','T_avg']])
        self.table_df=self.make_summary_table(self.all_days_df,self.bf_slope)

        self.bf_line_df=self.bf.copy()


        # Some flags
        self.old_ws=self.initial_ws
        self.current_state=[]
        self.baseline_slope_df=self.bf_line_df
        print('In init, all_days_df\n',self.all_days_df.head(6))
        return

    def get_weather_station_data(self,dataset='daily-summaries',
        units='standard',stations= 'USW00014739',startDate='1937-01-01',
        endDate='2019-12-31'):
        '''Gets weather data from: https://www.ncei.noaa.gov using V1 of
        the latest API as of 1/26/2020.

        Accepts inputs of stations (weather station id), startDate (string
        in the format of yyyy-mm-dd), endDate, and units (standard or metric).

        Defaults are: Boston, standard units, '1937-01-01', '2019-12-31' and
        daily-summaries which contains most of the daily data for a particular
        weather station (US dominated.)'''

        params={'dataset':dataset,
                'units':units,
                'stations':stations,
                'startDate':startDate,
                'endDate':endDate,
                'includeStationName':'true',
                'includeStationLocation':'1',
                'includeAttributes':'true',
                'format':'json'
               }
        base_url='https://www.ncei.noaa.gov/access/services/data/v1?'

        r = requests.get(base_url,params=params)
        if r.status_code == 200:
            df=pd.DataFrame(r.json())
            df.to_csv(params['stations']+'.csv')
            return df

        else:
            print('Problem accessing ncei.noaa.gov.  Status code: {} '.format(r.status_code))
            print('Reason: {}'.format(r.reason))
            empty=[]
            return empty

    def open_existing_weather_station_data(self,ws):
        '''WS is a weather station with name in the form of:
        "USW00014739".  Returns df with hemisphere, year, and season added.'''
        weather_station_path=os.getcwd()+'\\Data\\'+ws+'_temp.csv'
        print('Weather_path {}'.format(weather_station_path))
        p_df2=pd.read_csv(weather_station_path)
        p_df2=p_df2[['DATE','TMAX','TMIN']]
        p_df2['YEAR']=p_df2['DATE'].apply(lambda x: x.split('-')[0])
        return p_df2

    def open_all_state_data(self,file_name):
        '''Open all data df process as existing ws.'''
        weather_station_path=file_name
        p_df2=pd.read_csv(file_name,index_col=0)
        p_df2=p_df2[['NAME','STATE','STATION','DATE','LATITUDE',
            'LONGITUDE','TMAX','TMIN']]
        p_df2['YEAR']=p_df2['DATE'].apply(lambda x: x.split('-')[0])
        return p_df2


    def one_day_per_week(self,df):
        '''Slice dataframe to one day per week on column DATE'''

        bob=df[['DATE','TMAX','TMIN']].copy()
        bob['TMAX']=bob['TMAX'].apply(float)
        bob['TMIN']=bob['TMIN'].apply(float)
        bob.reset_index(inplace=True,drop=True)
        bob=bob.loc[(bob.DATE.str.contains('-07'))|(bob.DATE.str.contains('-14'))|\
                    (bob.DATE.str.contains('-21'))|(bob.DATE.str.contains('-28')),:]
        return bob

    def summarize_key_readings(self,df,key_readings=['STATION','NAME','LONGITUDE',
    'LATITUDE','TMIN','TMAX','TAVG','PRCP','SNOW']):
        '''Checks df for the items in key_readings (list).'''
        measurements=df.columns
        df2=df.copy().reset_index(drop=True)

        for k in key_readings:
            if k in df2.columns:
                print('{}: {}'.format(k,df2[k][0]))
                if (k=='LATITUDE'):
                    hem=self.get_hemisphere(df2[k][0])
        return

    def get_hemisphere(self,x):
        if float(x) > 0:
            return 'NORTHERN'

        elif float(x) < 0:
            return 'SOUTHERN'

        elif float(x) == 0:
            return 'EQUATOR'

        else:
            return 'Problem with latitude'

    def get_season(self,t_date,hem='NORTHERN'):
        '''For simplicity sake, assume seasons change on 21st (Dec, March,
        June, Sept), and exact equitorial coordinates default to Northern hemisphere.'''

        tmp=t_date.split('-')
        month=int(tmp[1])
        day=int(tmp[2])

        if (month == 12 and day>=21) | (month in[1,2]) | (month == 3 and day <22):
            if hem in ['NORTHERN','EQUATOR']:
                return 'WINTER'
            else:
                return 'SUMMER'

        if (month == 3 and day>=22) | (month in[4,5]) | (month == 6 and day <21):
            if hem in ['NORTHERN','EQUATOR']:
                return 'SPRING'
            else:
                return 'FALL'

        if (month == 6 and day>=21) | (month in[7,8]) | (month == 9 and day <21):
            if hem in ['NORTHERN','EQUATOR']:
                return 'SUMMER'
            else:
                return 'WINTER'

        if (month == 9 and day>=21) | (month in[10,11]) | (month == 12 and day <21):
            if hem in ['NORTHERN','EQUATOR']:
                return 'FALL'
            else:
                return 'SPRING'

    def get_hot_cold_days(self,df):
        warmest_day_temp=df.TMAX.max()
        warmest_day=df.loc[df.TMAX==warmest_day_temp,
            'DATE'].sort_values().reset_index(drop=True)[0]

        coldest_day_temp=df.TMIN.min()
        coldest_day=df.loc[df.TMIN==coldest_day_temp,
            'DATE'].sort_values().reset_index(drop=True)[0]

        return warmest_day,warmest_day_temp,coldest_day,coldest_day_temp

    def get_hot_cold_years(self,df):
        '''df must have DATE,TMIN,TMAX'''
        df['AVG']=df['TMAX']/2.0+df['TMIN']/2.0
        df['year']=df.DATE.apply(lambda x: x.split('-')[0])

        hot=pd.DataFrame(df.groupby('year')['AVG'].mean())
        hot=hot.sort_values(['AVG','year'],ascending=[False,True]).reset_index(drop=False)
        hotest_year=hot['year'][0]
        hotest_year_temp=hot['AVG'][0]

        cold=pd.DataFrame(df.groupby('year')['AVG'].mean())
        cold=hot.sort_values(['AVG','year'],ascending=[True,True]).reset_index(drop=False)
        coldest_year=cold['year'][0]
        coldest_year_temp=cold['AVG'][0]
        return hotest_year,hotest_year_temp,coldest_year,coldest_year_temp

    def calculate_yearly_data(self,df):
        '''Accepts daily df with YEAR,TMAX, and TMIN
        Returns TMAX_max which is the hottest point of the year, TMIN_min,
        which is the year,TMAX_min which is essentially the hottest day in,
        but technically could be in spring or fall, etc.'''
        df['T_avg']=df['TMAX']/2.0+df['TMIN']/2.0
        years_df=df.groupby('YEAR')['T_avg'].mean().reset_index(drop=False)
        tmp1=df.groupby('YEAR')['T_avg'].max().reset_index(drop=False)
        tmp1.rename(columns={'T_avg':'T_avg_max'},inplace=True)
        tmp2=df.groupby('YEAR')['T_avg'].min().reset_index(drop=False)
        tmp2.rename(columns={'T_avg':'T_avg_min'},inplace=True)
        years_df=pd.merge(years_df,tmp1,how='left',on='YEAR')
        years_df=pd.merge(years_df,tmp2,how='left',on='YEAR')

        years_df_max=df.groupby('YEAR')['TMAX','TMIN'].max().reset_index(drop=False)
        years_df_max.rename(columns={'TMAX':'TMAX_max','TMIN':'TMIN_max'},inplace=True)

        years_df_min=df.groupby('YEAR')['TMAX','TMIN'].min().reset_index(drop=False)
        years_df_min.rename(columns={'TMAX':'TMAX_min','TMIN':'TMIN_min'},inplace=True)

        years_df=pd.merge(years_df,years_df_max,how='left',on='YEAR')
        years_df=pd.merge(years_df,years_df_min,how='left',on='YEAR')
        del tmp1,tmp2,years_df_min,years_df_max

        return years_df

    def calculate_yearly_summaries(self,yearly_df):
        '''Accept daily data, add decade info, convert to year, return as decade summary'''
        yearly_summary=yearly_df[['YEAR','T_avg']].copy()
        yearly_summary['Decade']=(yearly_summary['YEAR'].astype(int)/10).apply(int).apply(str)+"0's"

        yearly_summary=yearly_summary.sort_values('T_avg',
                        ascending=False).reset_index(drop=True)

        year_count=len(yearly_summary)
        print('# Years: {}'.format(year_count),'\nyearly_summary\n',yearly_summary.head(2))

        top_ten=yearly_summary.loc[yearly_summary.index<=9,['Decade','T_avg']]
        top_ten=pd.DataFrame(top_ten.groupby('Decade')\
        ['T_avg'].count()).reset_index(drop=False).rename(columns={'T_avg':'T10'})

        top_twenty=yearly_summary.loc[(yearly_summary.index>9)&(yearly_summary.index<=19),['Decade','T_avg']]
        top_twenty=pd.DataFrame(top_twenty.groupby('Decade')\
        ['T_avg'].count()).reset_index(drop=False).rename(columns={'T_avg':'T20'})

        bottom_ten=yearly_summary.loc[yearly_summary.index>=(year_count-11),['Decade','T_avg']]
        bottom_ten=pd.DataFrame(bottom_ten.groupby('Decade')\
        ['T_avg'].count()).reset_index(drop=False).rename(columns={'T_avg':'B10'})

        bottom_twenty=yearly_summary.loc[(yearly_summary.index>(year_count-21))&(yearly_summary.index<=(year_count-11)),['Decade','T_avg']]
        bottom_twenty=pd.DataFrame(bottom_twenty.groupby('Decade')\
        ['T_avg'].count()).reset_index(drop=False).rename(columns={'T_avg':'B20'})

        htcld_years=pd.DataFrame()
        htcld_years['Decade']=sorted(yearly_summary.Decade.unique())
        htcld_years=pd.merge(htcld_years,bottom_ten,how='left',on='Decade')
        htcld_years=pd.merge(htcld_years,bottom_twenty,how='left',on='Decade')
        htcld_years=pd.merge(htcld_years,top_ten,how='left',on='Decade')
        htcld_years=pd.merge(htcld_years,top_twenty,how='left',on='Decade')
        htcld_years=htcld_years.fillna(0)

        return year_count,yearly_summary,htcld_years

    def make_summary_table(self,all_days_df,slope):

        warmest_day,warmest_day_temp,coldest_day,coldest_day_temp=\
            self.get_hot_cold_days(all_days_df)
        hottest_year,hottest_year_temp,coldest_year,coldest_year_temp=\
            self.get_hot_cold_years(all_days_df)

        table_df=pd.DataFrame()
        table_df['Parameters']=['Hottest Day','Hottest Year',
        'Coldest Day','Coldest Year']
        table_df['Dates']=[warmest_day,hottest_year,coldest_day,coldest_year]
        table_df['Temp']=[warmest_day_temp,hottest_year_temp,
            coldest_day_temp,coldest_year_temp]
        table_df['Temp']=table_df['Temp'].apply(lambda x: '{:0.1f} F'.format(x))
        sl_str='{} F/yr'.format(round(slope,2))
        tmp=pd.DataFrame(columns=['Parameters','Dates','Temp'],
            data=[['Avg. Temp. Change','',sl_str]])

        table_df=table_df.append(tmp)
        del tmp
        return table_df

    def slider_input_to_table(self,raw_all_days_df,slide_low,slide_high):

        all_days_df=raw_all_days_df.copy()
        all_days_df['year']=all_days_df.YEAR.apply(int)
        all_days_df=all_days_df.loc[(all_days_df['year']>=slide_low)&\
                                    (all_days_df['year']<slide_high),:].copy()
        day_per_wk_df=self.one_day_per_week(all_days_df)
        years_df=self.calculate_yearly_data(all_days_df)
        year_count,yr_avg_dec_df,htcld_years=\
            self.calculate_yearly_summaries(years_df)
        warmest_day,warmest_day_temp,coldest_day,coldest_day_temp=\
            self.get_hot_cold_days(all_days_df)
        hottest_year,hottest_year_temp,coldest_year,coldest_year_temp=\
            self.get_hot_cold_years(all_days_df)

        bf_intercept,bf_slope,bf=self.make_plot.best_fit(years_df[['YEAR','T_avg']])

        table_df=self.make_summary_table(all_days_df,bf_slope)
        return table_df

    def set_all_dfs(self,all_state_df,station_id='USW00014739',
        slider_low=1940,slider_high=2020):
        print('Slider_low: {} Slider_high {}'.format(slider_low,slider_high))

        all_days_df=all_state_df.loc[all_state_df.STATION==station_id,:].copy()
        raw_all_days_df=all_days_df.copy()
        all_days_df['year']=all_days_df.YEAR.apply(int)
        all_days_df=all_days_df.loc[(all_days_df['year']>=slider_low)&\
                                    (all_days_df['year']<slider_high),:]

        day_per_wk_df=self.one_day_per_week(all_days_df)
        years_df=self.calculate_yearly_data(all_days_df)
        year_count,yr_avg_dec_df,htcld_years=\
            self.calculate_yearly_summaries(years_df)

        warmest_day,warmest_day_temp,coldest_day,coldest_day_temp=\
            self.get_hot_cold_days(all_days_df)
        hottest_year,hottest_year_temp,coldest_year,coldest_year_temp=\
            self.get_hot_cold_years(all_days_df)
        print('hottest',hottest_year,hottest_year_temp,
            coldest_year,coldest_year_temp)
        bf_intercept,bf_slope,bf=\
            self.make_plot.best_fit(years_df[['YEAR','T_avg']])

        table_df=self.make_summary_table(all_days_df,bf_slope)
        print('table_df in function\n',table_df.head(5) )
        return all_days_df, raw_all_days_df,day_per_wk_df,years_df,\
            year_count,yr_avg_dec_df,htcld_years,warmest_day,\
            warmest_day_temp,coldest_day,coldest_day_temp,bf_intercept,\
            bf_slope,bf,table_df

    def update_weather_station_change(self,new_ws):
            '''Accept new ws, update data to reflect change.'''

            self.initial_ws=new_ws
            self.old_sliders=[1940,2020]

            self.all_days_df=\
                self.all_state_df.loc[self.all_state_df.STATION==new_ws,:]
            self.raw_all_days_df=self.all_days_df.copy()
            self.day_per_wk_df=self.one_day_per_week(self.all_days_df)

            self.years_df=self.calculate_yearly_data(self.all_days_df)

            self.year_count=len(self.all_days_df.YEAR.unique())
            self.year_count,self.yearly_summary_df,self.htcld_years=\
                self.calculate_yearly_summaries(self.years_df)

            self.yr_avg_dec_df=self.yearly_summary_df.copy()
            self.warmest_day,self.warmest_day_temp,self.coldest_day,\
                self.coldest_day_temp=self.get_hot_cold_days(self.all_days_df)

            self.bf_intercept,self.bf_slope,self.bf=\
                self.make_plot.best_fit(self.years_df[['YEAR','T_avg']])
            self.table_df=self.make_summary_table(self.all_days_df,self.bf_slope)

            self.bf_line_df=self.bf.copy()


            # Some flags
            self.old_ws=self.initial_ws
            self.baseline_slope_df=self.bf_line_df
            print('In init, all_days_df\n',self.all_days_df.head(6))
            return

    def update_slider_change(self,new_slider_range):
            '''Accept new ws, update data to reflect change.'''


            self.old_sliders=new_slider_range

            print('Raw:\n',self.raw_all_days_df.head(2))
            self.all_days_df=self.raw_all_days_df.copy()
            self.all_days_df=\
                self.all_days_df.loc[(self.all_days_df.year>=new_slider_range[0])&\
                (self.all_days_df.year<new_slider_range[1]),:]
            self.day_per_wk_df=self.one_day_per_week(self.all_days_df)

            self.years_df=self.calculate_yearly_data(self.all_days_df)

            self.year_count=len(self.all_days_df.YEAR.unique())
            self.year_count,self.yearly_summary_df,tmp=\
                self.calculate_yearly_summaries(self.years_df)

            self.yr_avg_dec_df=self.yearly_summary_df.copy()
            self.warmest_day,self.warmest_day_temp,self.coldest_day,\
                self.coldest_day_temp=self.get_hot_cold_days(self.all_days_df)

            self.bf_intercept,self.bf_slope,self.bf=\
                self.make_plot.best_fit(self.years_df[['YEAR','T_avg']])
            self.table_df=self.make_summary_table(self.all_days_df,self.bf_slope)

            self.bf_line_df=self.bf.copy()

            print('In function, all_days_df head:\n',self.all_days_df.head(3))
            print('In function, all_days_df tail:\n',self.all_days_df.tail(3))
            return
