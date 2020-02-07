import pandas as pd
import numpy as np
import requests
import os

import re

class Weather_Stations_Data():

    def __init__(self):
        ''' Constructor for this class. '''
        return

    def get_state_weather_station_info(self,state):
        filename='coop-stations.txt'

        with open(filename) as f:
            content = f.readlines()
        # Remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]

        station_re=re.compile(r'[A-Z]{3}[0-9]{8}')
        ma_re = re.compile('\s{}\s'.format(state))

        united_re=re.compile(r'\sUNITED\s')
        states_re=re.compile(r'\sSTATES\s')
        geo_code_re=re.compile(r'\s[0-9]{2}\s')
        lat_re=re.compile(r'\s[0-9]{2,3}\.[0-9]{0,5}\s')
        lon_re=re.compile(r'\s-[0-9]{2,3}\.[0-9]{0,5}\s')
        stations_list=[]
        for c in content:
            tmp=station_re.findall(c)
            tmp1=ma_re.findall(c)
            if tmp:
                if tmp1:

                    station_pos=station_re.search(c)
                    united_pos=united_re.search(c)
                    loc_str=c[station_pos.end():united_pos.start()].strip()
                    loc_str=' '.join([x for x in loc_str.split() if x!=''])

                    state_pos=ma_re.search(c)
                    gc_pos=geo_code_re.search(c)
                    county_str=c[state_pos.end():gc_pos.start()].strip()
                    county_str=' '.join([x for x in county_str.split() if x!=''])
                    gc_pos=geo_code_re.search(c)

                    station_info=[station_re.findall(c)[0],
                                        loc_str,
                                        county_str,
                                        state,
                                        geo_code_re.findall(c)[0],
                                        lat_re.findall(c)[0],lon_re.findall(c)[0]
                                        ]
                    if len(station_info)==7:
                        stations_list.append(station_info)

        df=pd.DataFrame(columns=['Station','Location','County','State',
            'Geo_Code','Latitude','Longitude'],data=stations_list)

        return df

    def get_weather_station_data(self,dataset='daily-summaries',
        units='standard',stations='USW00014739',startDate='1937-01-01',
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
            print('Data for {} found.\n'.format(params['stations']))
            df=pd.DataFrame(r.json())
            df.to_csv(params['stations']+'.csv')
            return df

        else:
            print('Problem accessing ncei.noaa.gov.  Status code: {} '.format(r.status_code))
            print('Reason: {}'.format(r.reason))
            print('string sent: {}'.format(r.url))
            empty=[stations,r.status_code,r.reason,r.url]
            return empty

    def assemble_state_df(self, state_abb, dat_dir):
        '''Accept string describing directory where weather files are kept,
        assemble and state abbreviation.  Find all files of the form:
        XX_USxxx.csv, assemble and return DF.'''

        file_list=[x for x in os.listdir(dat_dir) if x.find(state_abb+'_US')>=0]

        df=pd.DataFrame()
        for f in file_list:
            try:
                tmp=pd.read_csv(dat_dir+f,index_col=0,low_memory=False)
                df=df.append(tmp)
            except:
                print('problem with {}'.format(f))

        def split_name(n):
            try:
                return n.split(',')[0]
            except:
                return n

        df['NAME']=df.NAME.apply(split_name)
        df['STATE']=state_abb
        df['COUNTRY']='US'
        df=df[['STATION','NAME','STATE','LATITUDE','LONGITUDE','DATE','TMIN',
            'TMAX','COUNTRY']]
        return df

    def make_ws_info(self,df):
        '''df is state df with all data.  return list of dicts in form:
        [{'label':name,'value':ws_name},....], as well as a list for markers
        in the map'''
        df['tmp']=df.apply(lambda x: (x.NAME,x.STATION,x.LATITUDE,x.LONGITUDE),
            axis=1)
        ws_list=sorted(df.tmp.unique())
        dr_dn_options=[{'label':x[0],'value':x[1]} for x in ws_list]

        del df['tmp']
        return ws_list,dr_dn_options
