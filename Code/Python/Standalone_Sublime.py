import sys
import os

sys.path.append(r'C:\Program Files\QGIS 3.20.3\apps\qgis\python') #this is important for loading qgis library
sys.path.append(r'C:\Program Files\QGIS 3.20.3\apps\qgis\python\plugins') #this is important for loading processing library 
sys.path.append(r'c:\program files\qgis 3.20.3\apps\python39\lib\site-packages') #this is important for loading processing library 
sys.path.append(r'C:\Users\user\AppData\Roaming\python\Python39\site-packages') #this is important for loading processing library 

import qgis
from qgis.gui import *
from qgis.core import *
from qgis.utils import plugins
from PyQt5.QtCore import *
from qgis.analysis import QgsNativeAlgorithms

import numpy as np
import geopandas as gpd
import pandas as pd

test = pd.DataFrame({'hi':[1,2],'hello':[3,4]})

if __name__ == '__main__':
	mypd= gpd.GeoDataFrame(test)
	print(mypd)