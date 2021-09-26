import geopandas as gpd
import matplotlib.pyplot as plt
import os

os.chdir(r"C:\Users\user\Desktop\Projects\qgis-vanguard")

sz = gpd.read_file('Data/MP14_Subzone_SE_2017.shp')

# use pyqgis to add map
sz_qgis = QgsVectorLayer(sz.to_json(),"MP14_Subzone_SE_2017","ogr")
projectCrs = QgsCoordinateReferenceSystem.fromEpsgId(3414)
sz_qgis.setCrs(projectCrs)
QgsProject.instance().addMapLayer(sz_qgis)
sz_qgis.triggerRepaint()

# Pandas option
# pd.set_option("display.max_columns", 3)

# sort and get the 10 largest area polygons
sz['area'] = sz.geometry.area
selected = sz.nlargest(10,'area')

values = ','.join("\'"+str(x)+"\'" for x in selected['SUBZONE_N'])
iface.activeLayer().selectByExpression('\"SUBZONE_N\" IN (' + values + ')', QgsVectorLayer.SetSelection)

# spatial
list_select = ['RAFFLES PLACE','BUKIT MERAH', 'CHINATOWN']
sz.query('SUBZONE_N == @list_select')

# geocoding
schools_latlong = pd.read_csv("Data/CentralRegion_schools_latlong.csv")
schools_geoms = gpd.points_from_xy(x=schools_latlong["longitude"],
                                    y=schools_latlong["latitude"],
                                    crs="epsg:4326")
schools = gpd.GeoDataFrame(schools_latlong, geometry=schools_geoms)
central_schools_sf=schools.to_crs("epsg:3414")


# get centroid
sz['centroid'] = sz.geometry.centroid
sz.set_geometry('centroid').plot('PLN_AREA_N', markersize=5)

# spatial join
