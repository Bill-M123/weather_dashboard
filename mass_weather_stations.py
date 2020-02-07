import pandas as pd
import numpy as np
import os

from weather_utilities.weather_stations_data import Weather_Stations_Data

state_abbrev='MA'
data_dir=os.getcwd()+'\\data\\'
print(os.listdir(data_dir))

get_wsd=Weather_Stations_Data()

mass_stations_df=get_wsd.get_state_weather_station_info('MA')

station_list=list(mass_stations_df.Station.unique())

valid_stations=[]
invalid_stations=[]

for s in station_list:
    print(s)
    tmp=get_wsd.get_weather_station_data(stations=s)

    if isinstance(tmp,list):
        print('Found invalid station',tmp)
        invalid_stations.append(tmp)

    if isinstance(tmp,pd.DataFrame):
        print('Found dataframe. {} {}'.format(state_abbrev,s))
        valid_stations.append([state_abbrev,s])
        tmp.to_csv(data_dir+state_abbrev+'_'+str(s)+'.csv')



if invalid_stations:
    invalid_df=pd.DataFrame(columns=['WS','Code','Reason','url'],data=invalid_stations)
    invalid_df.to_csv(data_dir+'invalid.csv')
    print('\n\nInvalid Stations',invalid_df.head(3))

if valid_stations:
    valid_df=pd.DataFrame(columns=['State','WS'],data=valid_stations)
    print('\n\nValid Stations\n',valid_df.head(3))


#bob=get_wsd.get_weather_station_data()
#print(bob.head())
