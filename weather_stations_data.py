
import pandas as pd
import numpy as np
from numpy import random

import datetime as dt

from weather_utilities.weather_utilities import Weather_Utils
from weather_utilities.plot_utilities import Plot_Utils

weather =Weather_Utils()
make_plot=Plot_Utils()

station_file='coop-stations.txt'

with open(station_file) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

cities=[]
for c in content:
    line=c.split()
    line=[x for x in line if x!='']
    if ('UNITED' in line) and ('STATES' in line) and ('MA' in line):
        cities.append(line)
df=pd.DataFrame(cities)
df=df.rename(columns={0:'Num_0',1:'Num_1',2:'String_2',3:'Station_ID'})
for c in df.columns:
    print(c,df[c][0])

print(df[8].unique())
