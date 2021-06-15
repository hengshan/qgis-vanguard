import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
pd.set_option('display.max_columns', 20)

# change work directory
import os
os.chdir("/Users/hs/Projects/pyqgis")

# open shape file
sz = gpd.read_file('Data/MP14_Subzone_SocioEconIndicators_2017.shp')
print(type(sz))
print(sz.head())

# plot the subzone polygons
sz.plot()

# some cmap codes 
# viridis, plasma, inferno, magma, cividis
# Greys, Purples, Blues, Greens, Oranges, Reds
# YlOrBr, OrRd, PuRd, RdPu, BuPu, GnBu, PuBu, YlGnBu, PuBuGn, BuGn, YlGn
# PiYg, PRGn, BrBG, PuOr, RdGy, RdBu, RdYlBu, Spectral, coolwarm, bwr, seismic
# twilight, twilight_shifted, hsv
# Pastel1, Pastel2, PAired, Accent, Dark2, Set1, Set2, Set3, tab10, tab20, tab20b, tab20c
sz.plot(cmap='magma', figsize=(12, 6))
# We can also plot the  polygons with no fill color by using GeoDataFrame.boundary.plot()
# sz.boundary.plot()

# we can choose one subzone to plot
# sz[sz['SUBZONE_N'] == 'CENTRAL WATER CATCHMENT'].plot(figsize=(12, 6))

# we can choose a series of subzones to plot
sz_bm =sz[sz['PLN_AREA_C']=='BM']
sz_bm.plot(figsize=(12, 6))
# sz[sz['PLN_AREA_C'].isin(['BM','SB'])].plot(figsize=(12, 6))

# add label
fig = plt.figure(1, figsize=(25,15)) 
ax = fig.add_subplot()
sz_bm.apply(lambda x: ax.annotate(s=x.SUBZONE_N, xy=x.geometry.centroid.coords[0], ha='center', fontsize=2),axis=1);
sz_bm.boundary.plot(ax=ax, figsize=(25, 14), color='Black', linewidth=.4)
sz_bm.plot(ax=ax, cmap='Pastel2')
# ax.text(-0.05, 0.5, 'QGIS Vanguard', transform=ax.transAxes,
#         fontsize=5, color='gray', alpha=0.5,
#         ha='center', va='center', rotation='90')

# # how about we combine the three plots into one canvas
# fig, axs = plt.subplots(ncols=2, nrows=2)
# sz.plot(ax=axs[0,0])
# sz.plot(cmap='magma',ax=axs[1,0])
# sz[sz['SUBZONE_N'] == 'CENTRAL WATER CATCHMENT'].plot(ax=axs[0,1])


plt.show()