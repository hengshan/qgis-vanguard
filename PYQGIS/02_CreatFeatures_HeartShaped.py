import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import time

# create memory layer with two attributes
vlayer = QgsVectorLayer('Point?crs=EPSG:3414 - SVY21 / Singapore TM - Projected', 'point', 'memory')
provider = vlayer.dataProvider()
provider.addAttributes([QgsField('name', QVariant.String),QgsField('name2', QVariant.String),])
vlayer.updateFields()

# create points using numpy
t = np.arange(0, 2* np.pi, 0.1)
xhrt =16*np.power(np.sin(t),3)
yhrt = 13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)
xhrt = xhrt *2300 + 27223
yhrt = yhrt *2300 + 37158 

# add points to layer
for i in range(0,len(t)):
    f = QgsFeature()
    f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(xhrt[i], yhrt[i])))
    f.setAttributes(['Happy Birthday','Singapore'])
    provider.addFeature(f)
    
vlayer.updateExtents()
QgsProject.instance().addMapLayer(vlayer)

# change layer symbol
# change size
vlayer.renderer().symbol().symbolLayer(0).setSize(2)
vlayer.triggerRepaint()

# change color

vlayer.renderer().symbol().symbolLayer(0).setColor(QColor.fromRgb(255,0,0))
vlayer.triggerRepaint()

# animate
import threading

times = 0
def f(f_stop, lyr):
    # do something here ...
    lyr.renderer().symbol().symbolLayer(0).setColor(QColor.fromRgb(*np.random.randint(255, size=3)))
    lyr.triggerRepaint()

    if not f_stop.is_set():
        threading.Timer(1, f, [f_stop,lyr]).start()

    global times
    times+=1
    if times>50:
        f_stop.set()

f_stop = threading.Event()

# start calling f now and every sec thereafter
f(f_stop,vlayer)
