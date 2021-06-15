from qgis.PyQt.QtCore import QVariant

vl = QgsVectorLayer("Point?crs=epsg:3414", "Companies", "memory")
pr = vl.dataProvider()
pr.addAttributes([QgsField("Name", QVariant.String),
                  QgsField("Employees",  QVariant.Int),
                  QgsField("Revenue", QVariant.Double),
                  QgsField("Rev. per employee", QVariant.Double),
                  QgsField("Sum", QVariant.Double),
                  QgsField("Fun", QVariant.Double)])
vl.updateFields()
my_data = [
    {'x': 30000, 'y': 30000, 'name': 'ABC', 'emp': 10, 'rev': 100.1},
    {'x': 31000, 'y': 32000, 'name': 'DEF', 'emp': 2, 'rev': 50.5},
    {'x': 32000, 'y': 33000, 'name': 'GHI', 'emp': 100, 'rev': 725.9}]

for rec in my_data:
    f = QgsFeature()
    pt = QgsPointXY(rec['x'], rec['y'])
    f.setGeometry(QgsGeometry.fromPointXY(pt))
    f.setAttributes([rec['name'], rec['emp'], rec['rev']])
    pr.addFeature(f)

vl.updateExtents()
QgsProject.instance().addMapLayer(vl)
vl.triggerRepaint()

# add three expresssions
expression1 = QgsExpression('"Revenue"/"Employees"')
expression2 = QgsExpression('sum("Revenue")')
expression3 = QgsExpression('area(buffer($geometry,"Employees"))')
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(vl))

with edit(vl):
    for f in vl.getFeatures():
        context.setFeature(f)
        f['Rev. per employee'] = expression1.evaluate(context)
        f['Sum'] = expression2.evaluate(context)
        f['Fun'] = expression3.evaluate(context)
        vl.updateFeature(f)

print(f['Sum'])

# filter a layer with expression
layer = QgsVectorLayer("Point?field=Test:integer","addfeat", "memory")
QgsProject.instance().addMapLayer(layer)
layer.startEditing()
for i in range(10):
    feature = QgsFeature()
    feature.setAttributes([i])
    assert(layer.addFeature(feature))
layer.commitChanges()
layer.updateExtents()

expression = 'Test >= 3'
request = QgsFeatureRequest().setFilterExpression(expression)
matches = 0
for f in layer.getFeatures(request):
   matches += 1
print(matches)




