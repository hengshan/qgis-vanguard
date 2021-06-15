root = QgsProject.instance().layerTreeRoot()

import re

# list of all the checked layers in the TOC 
checked_layers = root.checkedLayers() 
print(checked_layers)

# create two tree groups
group1 = root.addGroup("group1")
group2 = root.addGroup("group2")

# get a QgsVectorLayer
vl1 = QgsProject.instance().mapLayersByName("MP14_Subzone_Central")[0]
vl2 = QgsProject.instance().mapLayersByName("MP14_REGION_NO_SEA_PL")[0]

# create a QgsLayerTreeLayer object from vl by its id
myvl1 = root.findLayer(vl1.id())
myvl2 = root.findLayer(vl2.id())

# clone the myvl QgsLayerTreeLayer object
myvl1clone = myvl1.clone()
myvl2clone = myvl2.clone()

# get the parent. If None (layer is not in group) returns ''
parent = myvl1.parent()
parent2 = myvl2.parent()

# move the cloned layer to the top (0)
group1.insertChildNode(0, myvl1clone)
group2.insertChildNode(0, myvl2clone)

# remove the QgsLayerTreeLayer from its parent
parent.removeChildNode(myvl1)
parent2.removeChildNode(myvl2)

# print only tree layer names which contain _
for child in root.children():
    if (re.search("_",child.name())):
       print(child.name())

# print all layers
# def getGroupLayers(group):
#     print('- group:' + group.name())
#     for child in group.children():
#         if isinstance(child, QgsLayerTreeGroup):
#             getGroupLayers(child)
#         else:
#             print('  - layer:' + child.name())


# root = QgsProject.instance().layerTreeRoot()
# for child in root.children():
#     if isinstance(child, QgsLayerTreeGroup):
#         getGroupLayers(child)
#     elif isinstance(child, QgsLayerTreeLayer):
#         print ("- layer: " + child.name())

# search layer from layer tree root
# QgsProject.instance().layerTreeRoot().findLayer(vl1.id()).setItemVisibilityChecked(False)

# change all layer names
# for layer in QgsProject.instance().mapLayers().values():
#     layer.setName('QGIS_' + layer.name())

# change selected layers' names
# for layer in iface.layerTreeView().selectedLayers():
#     layer.setName(layer.name()+"_Vanguard")


