import re

project = QgsProject.instance()
root = project.layerTreeRoot()

# print all layers
def getGroupLayers(group):
    # print('- group:' + group.name())
    for child in group.children():
        if isinstance(child, QgsLayerTreeGroup):
            getGroupLayers(child)
        else:
        	pass
            # print('  - layer:' + child.name())


for child in root.children():
    if isinstance(child, QgsLayerTreeGroup):
        getGroupLayers(child)
    elif isinstance(child, QgsLayerTreeLayer):
    	pass
        # print ("- layer: " + child.name())

# search layer from layer tree root
# QgsProject.instance().layerTreeRoot().findLayer(vl1.id()).setItemVisibilityChecked(False)

# change all layer names
contain_str = QInputDialog().getText(None, "Input", "If Layer Name contains:")
replace_str = QInputDialog().getText(None, "Input", f"Replace {contain_str[0]} with:")
prefix = QInputDialog().getText(None, "Input", "Add prefix:")
suffix = QInputDialog().getText(None, "Input", "Add suffix:")

print(prefix, suffix)
# print only tree layer names which contain _
for child in root.children():
    if (re.search(contain_str[0],child.name())):
       layer = project.mapLayersByName(child.name())[0]
       layer.setName(prefix[0] + layer.name().replace(contain_str[0], replace_str[0])+suffix[0])
       
# project.mapLayersByName("countries")[0]

# for layer in QgsProject.instance().mapLayers().values():
#     layer.setName('QGIS_' + layer.name())

# change selected layers' names
# for layer in iface.layerTreeView().selectedLayers():
#     layer.setName(layer.name()+"_Vanguard")

