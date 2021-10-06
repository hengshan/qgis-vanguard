import pandas as pd
import numpy as np
import random

myVectorLayer = iface.activeLayer()

myTargetField = 'Age_0to6' 

groups = 8
# the range of the field
size = QgsVectorLayerUtils.getValues(myVectorLayer, myTargetField)
size[0] # is the list of values

size_cut = pd.cut(size[0], bins=np.linspace(np.min(size[0]), np.max(size[0]), groups+1))

myRangeList = []
# Make a list of symbols and ranges...
for i in range(1,groups+1):
     myMin = size_cut.unique()[i].left
     myMax = size_cut.unique()[i].right
     myLabel = 'Group '+str(i)
     myColour = QColor("#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])) # generate a random color
     mySymbol = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
     mySymbol.setColor(myColour)
     myRange = QgsRendererRange(myMin, myMax, mySymbol, myLabel)
     myRangeList.append(myRange)

myRenderer = QgsGraduatedSymbolRenderer(myTargetField, myRangeList)  
myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)   
myVectorLayer.setRenderer(myRenderer)
myVectorLayer.triggerRepaint()