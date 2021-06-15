# Get the active layer (must be a vector layer)
layer = iface.activeLayer()

# Check if a layer is selected
if not layer:
    iface.messageBar().pushMessage('Please select a layer',  level=Qgis.Critical) 
# Check if the selected layer is a vector layer
if layer.type() != QgsMapLayer.VectorLayer:
    iface.messageBar().pushMessage('Please select a vector layer',  level=Qgis.Critical)

layer.selectAll()
# iface.mapCanvas().setSelectionColor( QColor("red") )

# zoom to selected layer extent
mc = iface.mapCanvas()
mc.setExtent(layer.extent())
mc.refresh()

# select by expression
# layer.selectByExpression('"ROAD_CODE"=\'TOP06M\'', QgsVectorLayer.SetSelection)
# iface.mapCanvas().setSelectionColor( QColor("red") )
# layer.removeSelection()

# access attributes
features=layer.getFeatures()
for feature in features:
    # retrieve every feature with its geometry and attributes
    print("Feature ID: ", feature.id())
	
	# retrieve only one attribte 
	print(feature['ROAD_CODE'])
	print(feature[1])

    # fetch attributes
    attrs = feature.attributes()

    # attrs is a list. It contains all the attribute values of this feature
    print(attrs)

# select features by extent
areaOfInterest = QgsRectangle(22033,35100, 25100,33410)
request = QgsFeatureRequest().setFilterRect(areaOfInterest)\
                             .setFlags(QgsFeatureRequest.ExactIntersect)

selected_fid = []
for feature in layer.getFeatures(request):
    selected_fid.append(feature.id())
    print(feature.id())

# Add these features to the selected list
layer.select(selected_fid)


# Only return selected fields to increase the "speed" of the request
# Don't return geometry objects to increase the "speed" of the request
# Fetch only the feature with id 45
# request.setFilterRect(areaOfInterest).setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes([0,2])









