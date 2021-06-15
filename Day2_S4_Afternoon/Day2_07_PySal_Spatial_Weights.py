import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import geopandas as gpd
import pandas as pd
from libpysal.weights import Queen, Rook, KNN

import os
os.chdir("/Users/hs/Projects/pyqgis")

gdf = gpd.read_file('Data/MP14_Subzone_SocioEconIndicators_2017.shp')
print(type(gdf))
print(gdf.head())

# Rook neighbors are those states that share an edge on their respective borders
w_rook = Rook.from_dataframe(gdf)

ax1 = gdf.plot(edgecolor='grey', facecolor='w')
ax1.set_title("Rook neighbors")
f,ax = w_rook.plot(gdf, ax=ax1,
        edge_kws=dict(color='r', linestyle=':', linewidth=1),
        node_kws=dict(marker=''))
ax.set_axis_off()

print(w_rook.n)
print(w_rook.neighbors[0]) # the first subzone has three neighbors at 2, 11, 42
print(gdf['SUBZONE_N'][[0,2, 11,42]])

# Queen neighbors are based on a more inclusive condition that requires only a shared vertex between two states:
w_queen = Queen.from_dataframe(gdf)
ax2 = gdf.plot(edgecolor='grey', facecolor='w')
ax2.set_title("Queen neighbors")
f,ax = w_queen.plot(gdf, ax=ax2,
        edge_kws=dict(color='r', linestyle=':', linewidth=1),
        node_kws=dict(marker=''))
ax.set_axis_off()
# plt.show()

# show histogram of the number of neighbours
print(w_rook.histogram)
print(w_queen.histogram)

# find the subzone with 9 queen neighbours
# cardinalities: Number of neighbors for each observation.
c9 = [idx for idx,c in w_queen.cardinalities.items() if c==9]
print(c9)
print(gdf['SUBZONE_N'][c9])
print(w_queen.neighbors[11])












