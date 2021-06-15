# use QgsInterface global variable iface to get active layer
layer = iface.activeLayer()

# Check if a layer is selected
if not layer:
    iface.messageBar().pushMessage('Please select a layer',  level=Qgis.Critical) 

# Check if the selected layer is a vector layer
if layer.type() != QgsMapLayer.VectorLayer:
    iface.messageBar().pushMessage('Please select a vector layer',  level=Qgis.Critical)


index = QgsSpatialIndex(layer.getFeatures())

# returns array of feature IDs of five nearest features
nearest = index.nearestNeighbor(QgsPointXY(27404, 28986), 5)

# returns array of IDs of features which intersect the rectangle
intersect = index.intersects(QgsRectangle(27189, 29180, 27878, 28642))