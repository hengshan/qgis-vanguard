# Get the active layer (must be a vector layer)
layer = iface.activeLayer()

# Check if a layer is selected
if not layer:
    iface.messageBar().pushMessage('Please select a layer',  level=Qgis.Critical) 
# Check if the selected layer is a vector layer
if layer.type() != QgsMapLayer.VectorLayer:
    iface.messageBar().pushMessage('Please select a vector layer',  level=Qgis.Critical)

# zoom to selected layer extent
mc = iface.mapCanvas()
mc.setExtent(layer.extent())
mc.refresh()

# select by expression
# layer.selectByExpression('"ROAD_CODE"=\'TOP06M\'', QgsVectorLayer.SetSelection)
# iface.mapCanvas().setSelectionColor( QColor("red") )
# layer.removeSelection()

# select features by extent
# areaOfInterest = QgsRectangle(22033,35100, 25100,33410)
# request = QgsFeatureRequest().setFilterRect(areaOfInterest)\
#                              .setFlags(QgsFeatureRequest.ExactIntersect)

# selected_fid = []
# for feature in layer.getFeatures(request):
#     selected_fid.append(feature.id())

# # Add these features to the selected list
# layer.select(selected_fid)

#simply select all features
layer.selectAll()
# iface.mapCanvas().setSelectionColor( QColor("red") )

output_name = 'Output/FeatAttr.csv'

# Using*with* statement which takes care of closing the files and handling errors
with open(output_name, 'w') as output_file:
    fieldnames = [field.name() for field in layer.fields()]

    ## write header
    line = ','.join(name for name in fieldnames) + '\n'
    output_file.write(line)
    
    # write feature attributes
    for f in layer.getFeatures():
        line = ','.join(str(f[name]) for name in fieldnames) + '\n'
        output_file.write(line)

iface.messageBar().pushMessage(
    'Success:', 'Output file written at ' + output_name, level=Qgis.Success)






