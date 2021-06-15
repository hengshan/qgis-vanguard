import numpy as np
rng = np.random.default_rng(12345)
rints = rng.integers(low=100, high=1000, size=100)
rints2 = rng.integers(low=100, high=1000, size=100)

rdb=np.random.random_sample((100,))*100
rdb_round = ['%.2f' % elem for elem in rdb]

# create layer
vl = QgsVectorLayer("Point?crs=epsg:3414", "temporary_points", "memory")
pr = vl.dataProvider()

# add fields
pr.addAttributes([QgsField("name", QVariant.String),
                    QgsField("size", QVariant.Double)])
vl.updateFields() # tell the vector layer to fetch changes from the provider


# add a feature
for i in range(100):
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(27400+rints[i], 29000+rints2[i])))
    fet.setAttributes(["Johny"+str(rints[i]), rdb_round[i]])
    pr.addFeatures([fet])

# update layer's extent when new features have been added
# because change of extent in provider is not propagated to the layer
vl.updateExtents()

# add vl to treeview and map
QgsProject.instance().addMapLayer(vl)

