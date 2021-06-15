# find out currently available renderers:
# print(QgsApplication.rendererRegistry().renderersList())

# use QgsInterface global variable iface to get active layer
layer = iface.activeLayer()

# Check if a layer is selected
if not layer:
    iface.messageBar().pushMessage('Please select a layer',  level=Qgis.Critical) 

# Check if the selected layer is a vector layer
if layer.type() != QgsMapLayer.VectorLayer:
    iface.messageBar().pushMessage('Please select a vector layer',  level=Qgis.Critical)

# choose a point layer
if layer.geometryType()!=QgsWkbTypes.PointGeometry:
    iface.messageBar().pushMessage('Please select a point layer',  level=Qgis.Critical)

# create a simple symbol with red square 
# circle, square, cross, rectangle, diamond, pentagon, 
# triangle, equilateral_triangle, star, regular_star, arrow, filled_arrowhead, x
symbol = QgsMarkerSymbol.createSimple({'name': 'x', 'color': 'red'})
layer.renderer().setSymbol(symbol)

# show the change
layer.triggerRepaint()

# get the full list of properties for the first symbol layer
# print(layer.renderer().symbol().symbolLayers()[0].properties())
# layer.renderer().symbol().symbolLayer(0).setSize(3)
# props = layer.renderer().symbol().symbolLayer(0).properties()
# props['color'] = 'yellow'
# props['name'] = 'square'
# layer.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))

########### create a categorized render
categorized_renderer = QgsCategorizedSymbolRenderer()

# Add a few categories
cat1 = QgsRendererCategory('1', QgsMarkerSymbol(), 'category 1')
cat2 = QgsRendererCategory('2', QgsMarkerSymbol(), 'category 2')
categorized_renderer.addCategory(cat1)
categorized_renderer.addCategory(cat2)

# Where value() is the value used for discrimination between categories
# label() is a text used for category description and symbol() method returns the assigned symbol.
for cat in categorized_renderer.categories():
    print("{}: {} :: {}".format(cat.value(), cat.label(), cat.symbol()))

########## create a graduated render
graduated_renderer = QgsGraduatedSymbolRenderer()
# Add a few categories
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('class 0-100', 0, 100), QgsMarkerSymbol()))
graduated_renderer.addClassRange(QgsRendererRange(QgsClassificationRange('class 101-200', 101, 200), QgsMarkerSymbol()))

for ran in graduated_renderer.ranges():
    print("{} - {}: {} {}".format(
        ran.lowerValue(),
        ran.upperValue(),
        ran.label(),
        ran.symbol()
      ))




















