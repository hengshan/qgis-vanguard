import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm

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

# change layer symbol
# change size
vlayer.renderer().symbol().symbolLayer(0).setSize(3)
vlayer.triggerRepaint()

# change color
vlayer.renderer().symbol().symbolLayer(0).setColor(QColor.fromRgb(255,0,0))
vlayer.triggerRepaint()

