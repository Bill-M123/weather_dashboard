# weather_dashboard

This dashboard forms the beginnings of a larger weather app that will access the NOAA api, download weather data for a particular weather station, and plot known data.  The temperature focus will be on deriving all data from daily TMAX and TMIN as that data is more prevalent than TAVG.

This implementation focuses only on Boston data, but this will be expanded over time.

Currently available:

1) Map showing longitude and latitude for chosen weather station (currently Boston)

2)  Summary table with hottest and coldest days and years, as well as a caluclated slope (simple linear regression on annual avg temperature)

3)  Bar chart showing hottest and coldest 20 years in data.  This chart corresponds to many articles that reference which decades are hottest.

4)  Larger chart that shows ranges of hot and cold temperatures, average annual temp, and complete best fit line.
