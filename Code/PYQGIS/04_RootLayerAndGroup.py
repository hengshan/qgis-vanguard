project = QgsProject.instance()
root = project.layerTreeRoot()

# list of all the checked layers in the TOC 
checked_layers = root.checkedLayers()

# find all selected layers
checked_layers_nodes = [root.findLayer(lyr.id()) for lyr in checked_layers]
checked_layers_nodes_clone = [root.findLayer(lyr.id()).clone() for lyr in checked_layers]
checked_layers_nodes_parent = [root.findLayer(lyr.id()).parent() for lyr in checked_layers]

# create a new group
group = root.addGroup("group")

[group.insertChildNode(0, node) for node in reversed(checked_layers_nodes_clone)]
[parent.removeChildNode(node) for parent,node in zip(checked_layers_nodes_parent,checked_layers_nodes)]