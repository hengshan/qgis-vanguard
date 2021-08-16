# as QgsProject is Singleton class, we need to get the instance of it
project = QgsProject.instance()

# open the project
project_name = 'Data/QgsProject.qgs'
project.read(project_name)

# list of layer names using list comprehension
layers = project.mapLayers()
l=[layer.name() for layer in layers.values()]

# dictionary with key = layer name and value = layer object
layers_list = {}
for l in layers.values():
  layers_list[l.name()] = l

print(layers_list)

# find layers by name
#project.mapLayersByName('MP14_Subzone_SE_2017')[0]