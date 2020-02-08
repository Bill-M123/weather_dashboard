import pandas as pd
import numpy as np
import os

import re

from weather_utilities.weather_stations_data import Weather_Stations_Data

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
