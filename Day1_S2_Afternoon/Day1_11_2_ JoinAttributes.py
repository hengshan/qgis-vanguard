import os
import geopandas as gpd
import pandas as pd

pd.set_option('display.max_columns', 20)

# change your current work directory
os.chdir("/Users/hs/Projects/pyqgis")

# attribute join and spatial join
subzone = gpd.read_file('Data/MP14_Subzone_Central.shp')
central_schools_sf = gpd.read_file('Data/central_schools_sf/central_schools_sf.shp')

# ensure that the two layers have the same crs
# here we have to transform the crs instead of set a new
central_schools_sf=central_schools_sf.to_crs("epsg:3414")

central_schools =  pd.read_csv('Data/CentralRegion_schools_latlong.csv')
# print(central_schools_sf.head())

# attribute join
central_schools_sf_latlong = central_schools_sf.merge(central_schools, on='BUILDING_N')
# print(central_schools_sf_latlong.head())

# spatial join
# print(subzone.head())
print(central_schools_sf.crs)
print(subzone.crs)

Taxi_Ride_Origin=gpd.read_file('Data/Taxi_Ride_Origin.shp')

joined= gpd.sjoin(central_schools_sf,subzone, how="inner", op='intersects')
print(joined.head())

joined2= gpd.sjoin(Taxi_Ride_Origin,subzone, how="inner", op='intersects')
print(joined2.head())
# add this spatial joined layer to map
# vl = QgsVectorLayer(joined.to_json(),"joined","ogr")
# QgsProject.instance().addMapLayer(vl)

