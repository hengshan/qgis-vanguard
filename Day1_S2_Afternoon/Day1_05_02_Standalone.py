from qgis.core import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm

# Supply path to qgis install location
QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/MacOS", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

# Write your code here to load some layers, use processing
# algorithms, etc.
vl = QgsVectorLayer("Point?crs=epsg:3414", "temporary_points", "memory")
pr = vl.dataProvider()

# create memory layer with two attributes
vlayer = QgsVectorLayer('Point?crs=EPSG:3414 - SVY21 / Singapore TM - Projected', 'point', 'memory')
provider = vlayer.dataProvider()
provider.addAttributes([QgsField('name', QVariant.String),QgsField('name2', QVariant.String),])
vlayer.updateFields()

# create points using numpy
t = np.arange(0, 2* np.pi, 0.1)
xhrt =16*np.power(np.sin(t),3)
yhrt = 13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)

# add points to layer
for i in range(0,len(t)):
    f = QgsFeature()
    f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(xhrt[i], yhrt[i])))
    f.setAttributes(['Somewhere ' + str(i),'Hello World'])
    provider.addFeature(f)
    
vlayer.updateExtents()
QgsProject.instance().addMapLayer(vlayer)
print("Hello World")
# change layer symbol
# change size
vlayer.renderer().symbol().symbolLayer(0).setSize(3)
vlayer.triggerRepaint()

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()