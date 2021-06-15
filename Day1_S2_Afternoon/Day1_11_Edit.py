# use QgsInterface global variable iface to get active layer
layer = iface.activeLayer()

# Check if a layer is selected
if not layer:
    iface.messageBar().pushMessage('Please select a layer',  level=Qgis.Critical) 

# Check if the selected layer is a vector layer
if layer.type() != QgsMapLayer.VectorLayer:
    iface.messageBar().pushMessage('Please select a vector layer',  level=Qgis.Critical)


# first change whether layer data provider can delete features
caps = layer.dataProvider().capabilities()
# Check if a particular capability is supported:
if caps & QgsVectorDataProvider.DeleteFeatures:
    print('The layer supports DeleteFeatures')
    res = layer.dataProvider().deleteFeatures([5, 10])

# add features
if caps & QgsVectorDataProvider.AddFeatures:
    feat = QgsFeature(layer.fields())
    feat.setAttributes([10010, 12333,"12345","Hello","World","!"])
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(32146, 30273)))
    (res, outFeats) = layer.dataProvider().addFeatures([feat])


# modify feature attributes
fid = 100   # ID of the feature we will modify
if caps & QgsVectorDataProvider.ChangeAttributeValues:
    attrs = { 0 : "32000", 1 : "30000" }
    layer.dataProvider().changeAttributeValues({ fid : attrs })

# modefy feature geometry
if caps & QgsVectorDataProvider.ChangeGeometries:
    geom = QgsGeometry.fromPointXY(QgsPointXY(32000,30000))
    layer.dataProvider().changeGeometryValues({ fid : geom })


######### edit features without undo redo
# use layer directly to add, delete and modify features
feat1 = feat2 = QgsFeature(layer.fields())
fid = 99
feat1.setId(fid)

# add two features (QgsFeature instances)
layer.addFeatures([feat1,feat2])

# delete a feature with specified ID
layer.deleteFeature(fid)

# set new geometry (QgsGeometry instance) for a feature
geometry = QgsGeometry.fromWkt("POINT(7 45)")
layer.changeGeometry(fid, geometry)

# update an attribute with given field index (int) to a given value
fieldIndex =1
value ='My new name'
layer.changeAttributeValue(fid, fieldIndex, value)

# add new field
layer.addAttribute(QgsField("mytext", QVariant.String))

# remove a field
layer.deleteAttribute(fieldIndex)

######### edit with redo undo
with edit(layer):
  feat = next(layer.getFeatures())
  feat[0] = 5
  layer.updateFeature(feat)




