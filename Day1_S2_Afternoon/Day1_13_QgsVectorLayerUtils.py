# use QgsInterface global variable iface to get active layer
layer = iface.activeLayer()

# Check if a layer is selected
if not layer:
    iface.messageBar().pushMessage('Please select a layer',  level=Qgis.Critical) 

# Check if the selected layer is a vector layer
if layer.type() != QgsMapLayer.VectorLayer:
    iface.messageBar().pushMessage('Please select a vector layer',  level=Qgis.Critical)

# create feature
# feat = QgsVectorLayerUtils.createFeature(layer)

# select only the first feature to make the output shorter
# layer.selectByIds([1])

val = QgsVectorLayerUtils.getValues(layer, "POSTCODE", selectedOnly=True)
print(val)