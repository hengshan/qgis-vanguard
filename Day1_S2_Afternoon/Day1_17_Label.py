# use QgsInterface global variable iface to get active layer
layer = iface.activeLayer()

# Check if a layer is selected
if not layer:
    iface.messageBar().pushMessage('Please select a layer',  level=Qgis.Critical) 

# Check if the selected layer is a vector layer
if layer.type() != QgsMapLayer.VectorLayer:
    iface.messageBar().pushMessage('Please select a vector layer',  level=Qgis.Critical)

########## label setting
label_settings = QgsPalLayerSettings()
#label_settings.drawBackground = True
label_settings.fieldName = 'BUILDING_N'

text_format = QgsTextFormat()
background_color = QgsTextBackgroundSettings()
background_color.setFillColor(QColor('red'))
background_color.setEnabled(True)
text_format.setBackground(background_color)
label_settings.setFormat(text_format)

layer.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
layer.setLabelsEnabled(True)
layer.triggerRepaint()