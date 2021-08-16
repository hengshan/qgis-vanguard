import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

# iternate all features to get feature id and geometry type
# features = layer.getFeatures()
# for feature in features:
#     # retrieve every feature id
#     print("Feature ID: ", feature.id())

#     # fetch geometry
#     # show some information about the feature geometry
#     geom = feature.geometry()
#     geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
#     if geom.type() == QgsWkbTypes.PointGeometry:
#         # the geometry type can be of single or multi type
#         if geomSingleType:
#             x = geom.asPoint()
#             print("Point: ", x)
#         else:
#             x = geom.asMultiPoint()
#             print("MultiPoint: ", x)
#     elif geom.type() == QgsWkbTypes.LineGeometry:
#         if geomSingleType:
#             x = geom.asPolyline()
#             print("Line: ", x, "length: ", geom.length())
#         else:
#             x = geom.asMultiPolyline()
#             print("MultiLine: ", x, "length: ", geom.length())
#     elif geom.type() == QgsWkbTypes.PolygonGeometry:
#         if geomSingleType:
#             x = geom.asPolygon()
#             print("Polygon: ", x, "Area: ", geom.area())
#         else:
#             x = geom.asMultiPolygon()
#             print("MultiPolygon: ", x, "Area: ", geom.area())
#     else:
#         print("Unknown or invalid geometry")

#     # for this test only print the first feature
#     # break

# create memory polyline layer 
vlayer_polyline = QgsVectorLayer('LineString?crs=EPSG:3414 - SVY21 / Singapore TM - Projected', 'Polyline', 'memory')
provider = vlayer_polyline.dataProvider()
provider.addAttributes([QgsField('name', QVariant.String),QgsField('name2', QVariant.String),QgsField('size', QVariant.Int)])
vlayer_polyline.updateFields()

# add points to layer
for i in range(0,len(t)):
    f = QgsFeature()
    if i ==(len(t)-1):
        f.setGeometry(QgsGeometry.fromPolyline([QgsPoint(xhrt[i], yhrt[i]),QgsPoint(xhrt[0], yhrt[0])]))
    else:
        f.setGeometry(QgsGeometry.fromPolyline([QgsPoint(xhrt[i], yhrt[i]),QgsPoint(xhrt[i+1], yhrt[i+1])]))
    f.setAttributes(['Happy Birthday','Singapore', i])
    provider.addFeature(f)


vlayer_polyline.updateExtents()
QgsProject.instance().addMapLayer(vlayer_polyline)

vlayer_polyline.renderer().symbol().symbolLayer(0).setWidth(1)
vlayer_polyline.renderer().symbol().symbolLayer(0).setColor(QColor.fromRgb(255, 0, 0))
vlayer_polyline.triggerRepaint()

# # Construct Geometry from coordinates
# gPnt = QgsGeometry.fromPointXY(QgsPointXY(1,1)) 
# print(gPnt) 
# print(gPnt.wkbType())

# gLine = QgsGeometry.fromPolyline([QgsPoint(1, 1), QgsPoint(2, 2)]) 
# print(gLine) 
# print(gLine.wkbType())

# gPolygon = QgsGeometry.fromPolygonXY([[QgsPointXY(1, 1), QgsPointXY(2, 2), QgsPointXY(2, 1)]]) 
# print(gPolygon)
# print(gPolygon.wkbType())

# # Construct Geometry from well known text
# geom = QgsGeometry.fromWkt("POINT(3 4)")
# print(geom)
