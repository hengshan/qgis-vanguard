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

# create a row of 63 points
xline = np.linspace(27226-50000, 27226+50000, 63)
yline = np.full(
  shape=63,
  fill_value=-1922,
  dtype=np.float64
)

def findYPoint(xa,xb,ya,yb,xc):
    m = (ya - yb) / (xa - xb)
    yc = (xc - xb) * m + yb
    return yc

INTER = 20 
xc_inters=[]
yc_inters=[]
for i in range(0,63):
    # create 50 points between the heart point and the line point
    xc_inter = np.linspace(xline[i], xhrt[i], INTER)
    yc_inter=[findYPoint(xline[i],xhrt[i],yline[i],yhrt[i],j) for j in xc_inter]
    xc_inters.append(xc_inter)
    yc_inters.append(yc_inter)

xc_inters_pd= pd.DataFrame(xc_inters)
yc_inters_pd= pd.DataFrame(yc_inters)

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
    if times>=INTER:
        f_stop.set()
    elif times>0:
        ptx_inter = xc_inters_pd.iloc[:,times]
        pty_inter = yc_inters_pd.iloc[:,times]
        with edit(lyr):   
            for feat in lyr.getFeatures():
                lyr.deleteFeature(feat.id())
        for i in range(0,len(ptx_inter)):
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(ptx_inter[i], pty_inter[i])))
            feat.setAttributes(['Happy Birthday','Singapore'])
            provider.addFeature(feat)

f_stop = threading.Event()

# start calling f now and every sec thereafter
f(f_stop,vlayer)
