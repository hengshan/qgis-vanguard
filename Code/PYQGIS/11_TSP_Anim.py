import time

layer =iface.activeLayer()
feat = layer.getFeatures()

points = []
for feature in feat:
    vertices = feature.geometry().asPolyline()
    for v in vertices:
        points.append(v)

# create memory layer with two attributes
vlayer = QgsVectorLayer('Point?crs=EPSG:3414 - SVY21 / Singapore TM - Projected', 'point', 'memory')

# add a point to the new layer
f = QgsFeature()
f.setGeometry(QgsPoint(points[0]))
provider = vlayer.dataProvider()
provider.addFeature(f)

vlayer.updateExtents()
QgsProject.instance().addMapLayer(vlayer)

# change layer symbol
# change size
vlayer.renderer().symbol().symbolLayer(0).setSize(4)
vlayer.triggerRepaint()

# change color
vlayer.renderer().symbol().symbolLayer(0).setColor(QColor.fromRgb(255,0,0))
vlayer.triggerRepaint()

# animate
import threading

INTER = len(points)-1 
times = 0
speed_rec = 0.1
def f(f_stop, lyr):
    # do something here ...

    if not f_stop.is_set():
        threading.Timer(speed_rec, f, [f_stop,lyr]).start()

    global times
    times+=1
    if times>=INTER:
        f_stop.set()
    elif times>0:
        # delete the point
        with edit(lyr):
            for feat in lyr.getFeatures():
                lyr.deleteFeature(feat.id())
        
        feat = QgsFeature()
        feat.setGeometry(QgsPoint(points[times]))
        provider.addFeature(feat)

f_stop = threading.Event()

# start calling f now and every sec thereafter
f(f_stop,vlayer)
