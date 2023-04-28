"""@author artfed Artem Fedorchenko"""
import pandas as pd
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs

"""parsed both csv files grouped them by same name"""

df_world_airports = pd.read_csv('airports_data.csv')
df_world_airports = df_world_airports[['City', 'Longitude', 'Latitude', 'IATA']]
df_tallinn_airport = pd.read_csv('otselennud20(2).csv', delimiter=';')
grouped_world_airports = df_world_airports.groupby('City')
grouped_tallinn_airport = df_tallinn_airport.groupby('City')

"""initialized the map"""
fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())


for city, group_world in grouped_world_airports:
    if city in grouped_tallinn_airport.groups:
        group_tallinn = grouped_tallinn_airport.get_group(city)
        merged_data = pd.merge(group_world, group_tallinn, on='IATA') # merged data based on the same IATA
        merged_data['Latitude'], merged_data['Longitude'] = merged_data['Latitude'].apply(lambda elem: float(elem)), \
            merged_data['Longitude'].apply(lambda elem: float(elem))
        green_destinations = ['SVO', 'KUT', 'CDG', 'DUB', 'EDI', 'VIE', 'NCE', 'GRO', 'NCE', 'MLA', 'ATE', 'PFO', 'TXL',
                              'SZG', 'ZRH', 'VNO']
        for x, y, z in zip(merged_data['Latitude'], merged_data['Longitude'], merged_data['IATA']):
            ax.plot([y, 24.7586], [x, 59.4369], color='red', linewidth='1', marker='o', transform=ccrs.Geodetic())
            if z in green_destinations:
                ax.plot([y, 24.7586], [x, 59.4369], color='green', linewidth='1', marker='o', transform=ccrs.Geodetic())
            ax.text(y, x, z, horizontalalignment='left', transform=ccrs.Geodetic())

ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=1)
ax.coastlines(resolution='110m')
ax.add_feature(cartopy.feature.OCEAN, facecolor=(0.5, 0.5, 0.5))
ax.gridlines()
ax.set_extent((-13, 45, 30, 70), crs=ccrs.PlateCarree())
plt.text(10, 72, 'Tallinn Airport 2020-2021\n'
                 'Author: Artem Fedorchenko',
         horizontalalignment='left',
         transform=ccrs.Geodetic())
plt.savefig('Europe.svg')
plt.show()
