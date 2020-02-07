import pandas as pd
import numpy as np
import os

import re

from weather_utilities.weather_stations_data import Weather_Stations_Data

def get_state_weather_station_info(state):
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

#print(get_state_weather_station_info('NH'))

state_abbrev='MA'
data_dir=os.getcwd()+'\\data\\'
get_wsd=Weather_Stations_Data()
df=get_wsd.assemble_state_df('MA',data_dir)

df.to_csv('ma_weather_stations.csv')
ws_list,dr_dn_options=get_wsd.make_ws_info(df)
print(df.tail(3))
print(ws_list)
print(dr_dn_options)
