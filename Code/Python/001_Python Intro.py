# programming = Data (Structure) + Algorithm (Processing)
# Python built-in data structure
# list [1,2,3,4]
# dict {"a":1,"b":2}
 
# array in numpy
# Series and Dataframe in Pandas
# GeoSereis and GeoDataframe in GeoPandas

# If we only have 10 mins to learn python
# create a list
listx = [1,2,3,4,5,6,7]
print(listx)

# list comprehension
listz = [i +10 for i in listx]
print(listz)

# numpy
import numpy as np
arr_a = np.array(listx)
print(arr_a)

# it is inconvenient to index and subsetting
import pandas as pd
sr_a = pd.Series(arr_a,index=list('abcdefg'))
print(sr_a)

# dictionary
dict_a = {'a':1,'b':2,'c':3,'d':4}
print(dict_a['a'])

list_ab = list('abcdefg')
dict_b = dict(zip(list_ab,arr_a))

# dictionary comprehension
dict_c = {list_ab[i]:arr_a[i] for i in range(len(arr_a))}
#print(dict_b)
#print(dict_c)
#
# multiple columns
sr_b = pd.Series(arr_a*10,index=list('abcdefg'))
#print(sr_b)

df_a = pd.DataFrame({'Column1':sr_b, 'Column2':sr_b})
#print(df_a)

################################ Example ###################
from shapely.geometry import Polygon
import geopandas as gpd
import matplotlib.pyplot as plt

# Get points in a grid
l = np.arange(4)
xs, ys = np.meshgrid(l, l)

## Set up store
#polys = []
## Generate polygons
#for x, y in zip(xs.flatten(), ys.flatten()):
#    poly = Polygon([(x, y), (x+1, y), (x+1, y+1), (x, y+1)])
#    polys.append(poly)

polys = [Polygon([(x, y), (x+1, y), (x+1, y+1), (x, y+1)]) for x, y in zip(xs.flatten(), ys.flatten())]

# Convert to GeoSeries
polys = gpd.GeoSeries(polys)
gdf = gpd.GeoDataFrame({'geometry': polys, 
                        'id': ['P-%s'%str(i).zfill(2) for i in range(len(polys))]})

ax = gdf.plot(facecolor='w', edgecolor='k')
[plt.text(x, y, t, 
          verticalalignment='center',
          horizontalalignment='center') for x, y, t in zip(
         [p.centroid.x-.25 for p in polys],
         [p.centroid.y-.25 for p in polys],
         [i for i in gdf['id']])]
ax.set_axis_off()
plt.show()

############### generate polygon using rubber band
# Create rubber bands
rbDict=[]
for x, y in zip(xs.flatten(), ys.flatten()):
    rb = QgsRubberBand(iface.mapCanvas(), True)
    rb.setColor(QColor(0,255,0,255))
    rb.setWidth(1)
    pts = [QgsPointXY(x, y),QgsPointXY(x+1, y),QgsPointXY(x+1, y+1),QgsPointXY(x, y+1),QgsPointXY(x, y)]
    rb.addGeometry(QgsGeometry.fromPolylineXY(pts))
    rbDict.append(rb)

### remove items
#for i,_ in enumerate(rbDict):
#    iface.mapCanvas().scene().removeItem(rbDict[i])
  
################ generate polygon features ################
#vlayer = QgsVectorLayer('polygon?crs=EPSG:3414 - SVY21 / Singapore TM - Projected', 'Grid', 'memory')
#provider = vlayer.dataProvider()
#provider.addAttributes([QgsField('id', QVariant.String)])
#vlayer.updateFields()
#i = 1
#for x, y in zip(xs.flatten(), ys.flatten()):
#    f = QgsFeature()
#    pts = [QgsPointXY(x, y),QgsPointXY(x+1, y),QgsPointXY(x+1, y+1),QgsPointXY(x, y+1),QgsPointXY(x, y)]
#    f.setGeometry(QgsGeometry.fromPolygonXY([pts])) #important, here is [pts] not pts
#    f.setAttributes([i])
#    provider.addFeature(f)
#    i+=1
#
#QgsProject.instance().addMapLayer(vlayer)
#





